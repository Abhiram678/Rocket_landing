"""
Gymnasium-compatible Rocket Landing Environment for SAC
Continuous action space version
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import cv2
import utils
import os
import random


class RocketLandingEnv(gym.Env):
    """
    Continuous action space rocket landing environment for SAC.
    
    Action Space:
        - thrust: [0.2*g, 2.0*g] - Continuous thrust control
        - nozzle_angle_velocity: [-30°/s, +30°/s] - Continuous nozzle control
    
    Observation Space:
        - x, y: position
        - vx, vy: velocity
        - theta, vtheta: angle and angular velocity
        - t: timestep
        - phi: nozzle angle
    """
    
    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 20}
    
    def __init__(self, max_steps=1000, task='landing', rocket_type='starship',
                 viewport_h=768, path_to_bg_img=None, render_mode=None):
        super().__init__()
        
        self.task = task
        self.rocket_type = rocket_type
        self.render_mode = render_mode
        
        self.g = 9.8
        self.H = 50  # rocket height (meters)
        self.I = 1/12*self.H*self.H  # Moment of inertia
        self.dt = 0.05
        
        self.world_x_min = -300  # meters
        self.world_x_max = 300
        self.world_y_min = -30
        self.world_y_max = 570
        
        # target point
        if self.task == 'hover':
            self.target_x, self.target_y, self.target_r = 0, 200, 50
        elif self.task == 'landing':
            self.target_x, self.target_y, self.target_r = 0, self.H/2.0, 50
        
        self.already_landing = False
        self.already_crash = False
        self.max_steps = max_steps
        
        # viewport height x width (pixels)
        self.viewport_h = int(viewport_h)
        self.viewport_w = int(viewport_h * (self.world_x_max-self.world_x_min) \
                          / (self.world_y_max - self.world_y_min))
        self.step_id = 0
        
        # Load background image
        if path_to_bg_img is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            path_to_bg_img = os.path.join(script_dir, task+'.jpg')
        self.bg_img = utils.load_bg_img(path_to_bg_img, w=self.viewport_w, h=self.viewport_h)
        
        self.state_buffer = []
        
        # Define action and observation spaces for Gymnasium
        # Action: [thrust, nozzle_angle_velocity]
        self.action_space = spaces.Box(
            low=np.array([0.2 * self.g, -30/180*np.pi]),
            high=np.array([2.0 * self.g, 30/180*np.pi]),
            dtype=np.float32
        )
        
        # Observation: [x, y, vx, vy, theta, vtheta, t, phi]
        self.observation_space = spaces.Box(
            low=np.array([-300, -30, -100, -100, -np.pi, -2*np.pi, 0, -20/180*np.pi]),
            high=np.array([300, 570, 100, 100, np.pi, 2*np.pi, max_steps, 20/180*np.pi]),
            dtype=np.float32
        )
        
        self.state = None
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        self.state = self.create_random_state()
        self.state_buffer = []
        self.step_id = 0
        self.already_landing = False
        self.already_crash = False
        
        observation = self.flatten(self.state)
        info = {}
        
        return observation, info
    
    def step(self, action):
        # Extract continuous actions
        f = np.clip(action[0], 0.2 * self.g, 2.0 * self.g)  # thrust
        vphi = np.clip(action[1], -30/180*np.pi, 30/180*np.pi)  # nozzle angular velocity
        
        # Current state
        x, y = self.state['x'], self.state['y']
        vx, vy = self.state['vx'], self.state['vy']
        theta, vtheta = self.state['theta'], self.state['vtheta']
        phi = self.state['phi']
        
        # Physics simulation
        ft, fr = -f*np.sin(phi), f*np.cos(phi)
        fx = ft*np.cos(theta) - fr*np.sin(theta)
        fy = ft*np.sin(theta) + fr*np.cos(theta)
        
        rho = 1 / (125/(self.g/2.0))**0.5
        ax, ay = fx-rho*vx, fy-self.g-rho*vy
        atheta = ft*self.H/2 / self.I
        
        # Update state
        if self.already_landing:
            vx, vy, ax, ay, theta, vtheta, atheta = 0, 0, 0, 0, 0, 0, 0
            phi, f = 0, 0
        
        self.step_id += 1
        x_new = x + vx*self.dt + 0.5 * ax * (self.dt**2)
        y_new = y + vy*self.dt + 0.5 * ay * (self.dt**2)
        vx_new, vy_new = vx + ax * self.dt, vy + ay * self.dt
        theta_new = theta + vtheta*self.dt + 0.5 * atheta * (self.dt**2)
        vtheta_new = vtheta + atheta * self.dt
        phi_new = phi + self.dt*vphi
        
        # Clip nozzle angle
        phi_new = max(phi_new, -20/180*np.pi)
        phi_new = min(phi_new, 20/180*np.pi)
        
        # Update state dictionary
        self.state = {
            'x': x_new, 'y': y_new, 'vx': vx_new, 'vy': vy_new,
            'theta': theta_new, 'vtheta': vtheta_new,
            'phi': phi_new, 'f': f,
            't': self.step_id, 'action_': 0
        }
        self.state_buffer.append(self.state)
        
        # Check terminal conditions
        self.already_landing = self.check_landing_success(self.state)
        self.already_crash = self.check_crash(self.state)
        reward = self.calculate_reward(self.state)
        
        done = self.already_crash or self.already_landing or self.step_id >= self.max_steps
        truncated = self.step_id >= self.max_steps
        
        observation = self.flatten(self.state)
        info = {
            'landed': self.already_landing,
            'crashed': self.already_crash,
            'x': x_new,
            'y': y_new,
            'velocity': (vx_new**2 + vy_new**2)**0.5
        }
        
        return observation, reward, done, truncated, info
    
    def create_random_state(self):
        x = np.random.uniform(-self.target_r, self.target_r)
        y = np.random.uniform(self.world_y_max * 0.5, self.world_y_max * 0.9)
        vx = np.random.uniform(-5, 5)
        vy = np.random.uniform(-10, 0)
        theta = np.random.uniform(-10/180*np.pi, 10/180*np.pi)
        vtheta = np.random.uniform(-5/180*np.pi, 5/180*np.pi)
        
        state_dict = {
            'x': x, 'y': y, 'vx': vx, 'vy': vy,
            'theta': theta, 'vtheta': vtheta,
            'phi': 0, 'f': 0,
            't': 0, 'action_': 0
        }
        return state_dict
    
    def flatten(self, state):
        x = np.array([
            state['x'], state['y'], state['vx'], state['vy'],
            state['theta'], state['vtheta'], state['t'],
            state['phi']
        ], dtype=np.float32) / 100.
        return x
    
    def check_crash(self, state):
        if self.task == 'hover':
            x, y = state['x'], state['y']
            if x < self.world_x_min or x > self.world_x_max:
                return True
            if y < self.world_y_min or y > self.world_y_max:
                return True
            return False
        
        elif self.task == 'landing':
            x, y = state['x'], state['y']
            vx, vy = state['vx'], state['vy']
            theta = state['theta']
            vtheta = state['vtheta']
            v = (vx**2 + vy**2)**0.5
            
            crash = False
            if y >= self.world_y_max - self.H / 2.0:
                crash = True
            if y <= 0 + self.H / 2.0 and v >= 15.0:
                crash = True
            if y <= 0 + self.H / 2.0 and abs(x) >= self.target_r:
                crash = True
            if y <= 0 + self.H / 2.0 and abs(theta) >= 10/180*np.pi:
                crash = True
            if y <= 0 + self.H / 2.0 and abs(vtheta) >= 10/180*np.pi:
                crash = True
            return crash
    
    def check_landing_success(self, state):
        if self.task == 'hover':
            return False
        elif self.task == 'landing':
            x, y = state['x'], state['y']
            vx, vy = state['vx'], state['vy']
            theta = state['theta']
            vtheta = state['vtheta']
            v = (vx**2 + vy**2)**0.5
            return True if y <= 0 + self.H / 2.0 and v < 15.0 and abs(x) < self.target_r \
                           and abs(theta) < 10/180*np.pi and abs(vtheta) < 10/180*np.pi else False
    
    def calculate_reward(self, state):
        x_range = self.world_x_max - self.world_x_min
        y_range = self.world_y_max - self.world_y_min
        
        # Distance reward
        dist_x = abs(state['x'] - self.target_x)
        dist_y = abs(state['y'] - self.target_y)
        dist_norm = dist_x / x_range + dist_y / y_range
        dist_reward = 0.1*(1.0 - dist_norm)
        
        # Pose reward
        if abs(state['theta']) <= np.pi / 6.0:
            pose_reward = 0.1
        else:
            pose_reward = abs(state['theta']) / (0.5*np.pi)
            pose_reward = 0.1 * (1.0 - pose_reward)
        
        reward = dist_reward + pose_reward
        
        # Task-specific rewards
        if self.task == 'hover' and (dist_x**2 + dist_y**2)**0.5 <= 2*self.target_r:
            reward = 0.25
        if self.task == 'hover' and (dist_x**2 + dist_y**2)**0.5 <= 1*self.target_r:
            reward = 0.5
        if self.task == 'hover' and abs(state['theta']) > 90 / 180 * np.pi:
            reward = 0
        
        v = (state['vx'] ** 2 + state['vy'] ** 2) ** 0.5
        if self.task == 'landing' and self.already_crash:
            reward = (reward + 5*np.exp(-1*v/10.)) * (self.max_steps - self.step_id)
        if self.task == 'landing' and self.already_landing:
            reward = (1.0 + 5*np.exp(-1*v/10.))*(self.max_steps - self.step_id)
        
        return reward
    
    def render(self):
        if self.render_mode is None:
            return None
        # Rendering implementation (optional for training)
        return None
    
    def close(self):
        cv2.destroyAllWindows()

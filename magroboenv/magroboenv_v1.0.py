import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import math

def square(x):
    return x*x

def distance(nparray1, nparray2):
    sum = square(nparray1[0] - nparray2[0]) + square(nparray1[1] - nparray2[1]) + square(nparray1[2] - nparray2[2])
    return math.sqrt(sum)

class EnvSpec(object):
    def __init__(self, timestep_limit, id):
        self.timestep_limit = timestep_limit
        self.id = id
        
class MagRoboEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    ACTION = ["w", "a", "s", "z", "q", "x"]

    MAX_SIZE = 10
    
    COMPASS = {
        "w": (0, -1, 0),
        "a": (-1, 0, 0),
        "s": (1, 0, 0),
        "z": (0, 1, 0),
        "q": (0, 0, 1),
        "x": (0, 0, -1)
    }
    
    def __init__(self):

        self.maze_size = (self.MAX_SIZE, self.MAX_SIZE, self.MAX_SIZE)



        timestep_limit = 2500
        self.spec = EnvSpec(timestep_limit = timestep_limit , id=1)

        # observation is the x, y, z coordinate of the grid
        low = np.zeros(len(self.maze_size), dtype=int)
        high = np.array(self.maze_size, dtype=int) - np.ones(len(self.maze_size), dtype=int)

        #fwd or bwd in each direction
        #self.action_space = spaces.Discrete(2*len(self.maze_size))
		
        self.action_space = spaces.Box(low=np.array([0.0,-1]), high=np.array([5.9,1]))
        self.observation_space = spaces.Box(low, high)

        #initial condition
        self.state = None
        self.steps_beyond_done = None

        # simulation related variables
        self.seed()
        self._set_goal()
        self._reset()
        #print(self.robot)

        
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """
        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self._take_action(action)
        #self.status = self.env.step()

        if np.array_equal(self.robot, self.goal):
            done = True
        else:
            #reward = -0.1/(self.maze_size[0]*self.maze_size[1])
            done = False

        self.state = self.robot
        ob = self.robot
        reward = self._get_reward()
        info = {}
        print(self.robot)
        return ob, reward, done, info

    def reset(self):
        self._reset()
        self.seed(0)

        ob=[0, 0, 0]
        return np.array(ob)

    def _reset(self):
        self.robot = np.zeros(3, dtype=int)
        #Distance b/w start & finish
        self.init_dist = distance(self.robot, self.goal)
        self.curr_dist = self.init_dist

    def _set_goal(self):
        self.goal = np.array(self.maze_size) - np.array((1,1,1))

    def render(self, mode='human', close=False):
        pass

    def _take_action(self, action):

        if math.isnan(action[0]):
            self.seed(0)
            return
        
        index = int(action[0])
        #print("action={}, index={}".format(action,index))
        if isinstance(index, int):
            act = self.ACTION[index]

        
            
        if act not in self.COMPASS.keys():
            raise ValueError("wrong action")

        #move robot
        self.robot += np.array(self.COMPASS[act])

        if self.robot[0] < 0:
            self.robot[0] = 0
        elif self.robot[0] == self.MAX_SIZE:
            self.robot[0] = self.MAX_SIZE - 1

        if self.robot[1] < 0:
            self.robot[1] = 0
        elif self.robot[1] == self.MAX_SIZE:
            self.robot[1] = self.MAX_SIZE - 1

        if self.robot[2] < 0:
            self.robot[2] = 0
        elif self.robot[2] == self.MAX_SIZE:
            self.robot[2] = self.MAX_SIZE - 1

            
    def _get_reward(self):

        self.last_dist = self.curr_dist

        self.curr_dist = distance(self.robot, self.goal)
        #print("ld:{} cd:{}".format(self.last_dist, self.curr_dist))
        
        """ Reward is given for XY. """
        if self.last_dist > self.curr_dist:
            return (1)
        elif self.last_dist < self.curr_dist:
            return (0)
        else:
            return 0

    

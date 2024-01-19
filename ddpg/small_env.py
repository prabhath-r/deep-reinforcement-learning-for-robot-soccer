# import numpy as np
# import gym
# from gym import spaces

# class Soccer(gym.Env):
#     def __init__(self):
#         # Action Space:
#         #  magnitude of movement (0 to max_linear_speed)
#         # angle of rotation (-π to π)
#         # For example, [3, π/2] would mean the agent moves with a speed of 3 units/second towards positive y direction.
#         max_linear_speed = 5  # Max forward speed of the agent.
#         max_angular_speed = np.pi  # max rotation speed in radians/second.
#         self.action_space = spaces.Box(low=np.array([0, -max_angular_speed]),
#                                        high=np.array([max_linear_speed, max_angular_speed]), dtype=np.float32)
        
#         # Observation Space:
#         # 1. Agent x-coordinate (-10 to 10)
#         # 2. Agent y-coordinate (-5 to 5)
#         # 3. Agent x-velocity (-10 to 10)
#         # 4. Agent y-velocity (-10 to 10)
#         # 5. Agent angle with respect to the x-axis (-pi to pi) normalized to (-1 to 1)
#         # 6. Ball x-coordinate (-10 to 10)
#         # 7. Ball y-coordinate (-5 to 5)
#         # 8. Ball x-velocity (-5 to 5)
#         # 9. Ball y-velocity (-5 to 5)
#         low = np.array([-10, -5, -10, 10, -1, -10, -5, -3, -3])  
#         high = np.array([10, 5, 10, 10, 1, 10, 5, 3, 3]) 
#         self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

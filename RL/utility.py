import math
import random
import numpy as np
class helper:
    def __init__(self):
        pass
    def find_slope(self, coord1, coord2):
        m=(coord1[1]-coord2[1])/(coord1[0]-coord2[0])
        c=coord1[1]-(m*coord1[0])
        return m, c

    def find_intersection(self, m, b, center, r):
        x_center=center[0]
        y_center=center[1]
        a = 1 + m**2
        b1 = 2 * (m * (b - y_center) - x_center)
        c = x_center**2 + (b - y_center)**2 - r**2
        discriminant = b1**2 - 4 * a * c

        if discriminant < 0:
            
            return None
        else:
            x1 = (-b1 + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b1 - math.sqrt(discriminant)) / (2 * a)

            y1 = m * x1 + b
            y2 = m * x2 + b

            intersection_points = [(x1, y1), (x2, y2)]
            return intersection_points


    def is_point_between(self, p1, p2, p3):
        distance_p1_p2 = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        distance_p1_p3 = math.sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2)
        distance_p2_p3 = math.sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2)
        return math.isclose(distance_p1_p3 + distance_p2_p3, distance_p1_p2)


    def agents_point(self, goal_pole1, goal_pole2, center, radius):
        #print(goal_pole1, goal_pole2, center, radius)
        mid=[(goal_pole1[0]+goal_pole2[0])/2, (goal_pole1[1]+goal_pole2[1])/2]
        m, c=self.find_slope(mid, center)
        points=self.find_intersection(m, c, center, radius)
        return points[1] if self.is_point_between(mid, center, points[0]) else points[0]

    def find_relative_target_coordinates(self, agent, target, ball):
        relative_target_x = target[0] - agent[0]
        relative_target_y = target[1] - agent[1]
        relative_ball_x = ball[0] - agent[0]
        relative_ball_y = ball[1] - agent[1]
        return relative_target_x, relative_target_y, relative_ball_x, relative_ball_y
class contacts:
    def __init__(self):
        pass
    def Is_agent_in_ground(self, agentcoord):
        if -480 <= agentcoord[0] <= 480 and -480 <= agentcoord[1] <= 480:
            return True
        print("out of ground")
        return False
class rewards:
    def __init__(self):
        pass
    def cal_reward(self, relative_target_x, relative_target_y, agentcoord, targetcoord):
        if contacts.Is_agent_in_ground(agentcoord)==False:
            return -1000000, -1, -1
        else:
            initial_distance = np.sqrt(relative_target_x**2 + relative_target_y**2)
            next_relative_target_x, next_relative_target_y=helper.find_relative_target_coordinates(agentcoord, targetcoord)
            new_distance = np.sqrt(next_relative_target_x**2 + next_relative_target_y**2)
            delta_distance = initial_distance - new_distance
            if new_distance < 0.1:  # You can adjust this threshold as needed
                delta_distance += 10.0  # A positive reward for reaching the target

            return delta_distance, next_relative_target_x, next_relative_target_y


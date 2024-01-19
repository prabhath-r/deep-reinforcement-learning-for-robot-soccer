# prev_distance_to_goal = None

# def move_and_rotate(current_coords, angle, forward):
#     forward+=angle
#     angle= angle
#     x, y, z = current_coords
#     x_prime = math.cos(angle)
#     y_prime = math.sin(angle)
#     z_prime = 0
#     return  forward, [x_prime, y_prime, z_prime]

# def Is_ball_touched():
# 	for i in range(len(data.contact.geom1)):
# 		if (data.geom(data.contact.geom1[i]).name == "ball_g" and data.geom(data.contact.geom2[i]).name == "sphero1") or (data.geom(data.contact.geom2[i]).name == "ball_g" and data.geom(data.contact.geom1[i]).name == "sphero1"):
# 			print("Ball touched") 
# 			return 1

# 	return 0

# boundaries = ("Touch lines1", "Touch lines2", "Touch lines3", "Touch lines4", "Touch lines5", "Touch lines6",)

# def Is_boundaries_touched():
# 	for i in range(len(data.contact.geom1)):
# 		if (data.geom(data.contact.geom1[i]).name == "sphero1" and data.geom(data.contact.geom2[i]).name in boundaries) or (data.geom(data.contact.geom2[i]).name == "sphero1" and data.geom(data.contact.geom1[i]).name in boundaries):
# 			print("boundary touched")
# 			return -10

# 	return 0

# Goal = ("Goal lines1", "Goal lines2")

# def Is_goal():
# 	for i in range(len(data.contact.geom1)):
# 		if (data.geom(data.contact.geom1[i]).name == "ball_g" and data.geom(data.contact.geom2[i]).name in Goal) or (data.geom(data.contact.geom2[i]).name == "ball_g" and data.geom(data.contact.geom1[i]).name in Goal):
# 			print("goal scored")
# 			return 10
# 	return 0

# def Is_goal_sphero():
# 	for i in range(len(data.contact.geom1)):
# 		if (data.geom(data.contact.geom1[i]).name == "sphero1" and data.geom(data.contact.geom2[i]).name in Goal) or (data.geom(data.contact.geom2[i]).name == "sphero1" and data.geom(data.contact.geom1[i]).name in Goal):
# 			print("wrong goal")
# 			return -20
# 	return 0

# def distance_bw_ball_n_sphero():
#     distance = np.linalg.norm(data.xpos[8] - data.xpos[9])
#     # print(distance)
#     return distance

# def distance_to_goal(ball_position):
# 	goal_position = np.array([45, 0, 0])
# 	distance = np.linalg.norm(ball_position - goal_position)
# 	# print(distance)	
# 	return distance

# def compute_reward():
#     global prev_distance_to_goal
#     prev_distance_to_goal = distance_to_goal(data.xpos[8])
#     distance_to_ball = distance_bw_ball_n_sphero()
    
#     time_penalty = -0.01
    
#     inverse_distance_reward = -1 / (1 + distance_to_ball) #reward for getting close to ball

    
#     # Fetch rewards and penalties
#     touch_ball_reward = Is_ball_touched()
#     out_of_bound_penalty = Is_boundaries_touched()
#     goal_achieved_reward = Is_goal()
#     own_goal_penalty = Is_goal_sphero()
#     touch_ball_reward *= 100
    
#     # Compute the overall reward
#     reward = (touch_ball_reward + 
#               goal_achieved_reward +
#               time_penalty +
#               out_of_bound_penalty +
#               own_goal_penalty +
#               inverse_distance_reward)
    
#     current_distance_to_goal = distance_to_goal(data.xpos[9])
    
#     if current_distance_to_goal < prev_distance_to_goal:
#         reward += 5 
#     elif current_distance_to_goal > prev_distance_to_goal:
#         reward -= 1
#     prev_distance_to_goal = current_distance_to_goal

#     return reward, goal_achieved_reward != 0.0, out_of_bound_penalty != 0 or own_goal_penalty != 0
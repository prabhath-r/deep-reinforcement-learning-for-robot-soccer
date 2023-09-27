import os
import math
import numpy as np
import mujoco as mj
from mujoco.glfw import glfw

from env import Soccer
from ddpg import DDPG

env = Soccer()

def move_and_rotate(current_coords, angle, forward):
    forward+=angle
    angle= angle
    x, y, z = current_coords
    x_prime = math.cos(angle)
    y_prime = math.sin(angle)
    z_prime = 0
    return  forward, [x_prime, y_prime, z_prime]

def Is_ball_touched():
	for i in range(len(data.contact.geom1)):
		if (data.geom(data.contact.geom1[i]).name == "ball_g" and data.geom(data.contact.geom2[i]).name == "sphero1") or (data.geom(data.contact.geom2[i]).name == "ball_g" and data.geom(data.contact.geom1[i]).name == "sphero1"):
			#print("touched_ball")
			return 100
	return 0
boundaries=( "Touch lines1", "Touch lines2", "Touch lines3", "Touch lines4", "Touch lines5", "Touch lines6",)
def Is_boundaries_touched():
	for i in range(len(data.contact.geom1)):
		if (data.geom(data.contact.geom1[i]).name == "sphero1" and data.geom(data.contact.geom2[i]).name in boundaries) or (data.geom(data.contact.geom2[i]).name == "sphero1" and data.geom(data.contact.geom1[i]).name in boundaries):
			#print("touched_boundary")
			#print(data.xpos[8])
			return -10000
	return 0
Goal=("Goal lines1", "Goal lines2")
def Is_goal():
	for i in range(len(data.contact.geom1)):
		if (data.geom(data.contact.geom1[i]).name == "ball_g" and data.geom(data.contact.geom2[i]).name in Goal) or (data.geom(data.contact.geom2[i]).name == "ball_g" and data.geom(data.contact.geom1[i]).name in Goal):
			#print("Goal!!!")
			return 1000
	return 0
def Is_goal_sphero():
	for i in range(len(data.contact.geom1)):
		if (data.geom(data.contact.geom1[i]).name == "sphero1" and data.geom(data.contact.geom2[i]).name in Goal) or (data.geom(data.contact.geom2[i]).name == "sphero1" and data.geom(data.contact.geom1[i]).name in Goal):
			#print("Sphero Goal!!!")
			return -100
	return 0

def distance_bw_goal1_n_ball():
		# define the line by two points a and b
		a = np.array([45, 5, 0])
		b = np.array([45, -5, 0])
		# define the point p
		p = data.xpos[8]
		# calculate the distance
		distance = np.linalg.norm(np.cross(p - a, p - b)) / np.linalg.norm(b - a)
		return distance
def distance_bw_goal2_n_ball():
		# define the line by two points a and b
		a = np.array([-45, 5, 0])
		b = np.array([-45, -5, 0])
		# define the point p
		p = data.xpos[8]
		# calculate the distance
		distance = np.linalg.norm(np.cross(p - a, p - b)) / np.linalg.norm(b - a)
		return distance
def distance_bw_ball_n_sphero():
    return np.linalg.norm(data.xpos[8] - data.xpos[9])

def compute_reward():
    # Compute the distance to the ball and the goal
    distance_to_ball = distance_bw_ball_n_sphero()
    distance_to_goal = distance_bw_goal1_n_ball()

    # Compute the time penalty
    time_penalty = -0.0001

    # Compute the out-of-bounds penalty
    out_of_bound_penalty = Is_boundaries_touched()
    # Compute the touch ball reward
    touch_ball_reward = Is_ball_touched()
    # Compute the goal achieved reward
    goal_achieved_reward = Is_goal()

    # Compute the distance to the ball and goal coefficients
    distance_to_goal_coeff = - 0.01
    distance_to_ball_coeff = - 0.01
    Sphero_goal_penalty=Is_goal_sphero()
    
    # Compute the overall reward
    reward = (
            touch_ball_reward +
            goal_achieved_reward +
            distance_to_ball_coeff * distance_to_ball +
            distance_to_goal_coeff * distance_to_goal +
            #time_penalty +
	        Sphero_goal_penalty+
            #rotation_penalty +
            out_of_bound_penalty)
    return reward, True if goal_achieved_reward!=0.0 else False, True if out_of_bound_penalty!=0 or Sphero_goal_penalty!=0 else False


epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01

# Configurations
xml_path = 'field.xml' #xml file (assumes this is in the same folder as this file)
simend = 40 #simulation time
print_camera_config = 0 #set to 1 to print camera config
						#this is useful for initializing view of the model)

# For callback functions
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

# get the full path
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "/" + xml_path)
xml_path = abspath

# MuJoCo data structures
model = mj.MjModel.from_xml_path(xml_path)  # MuJoCo model
data = mj.MjData(model)                		# MuJoCo data
cam = mj.MjvCamera()                        # Abstract camera
opt = mj.MjvOption()                        # visualization options
def render_it():
	mj.mj_resetData(model, data)
	# prev_distance_to_goal = distance_to_goal(data.xpos[8])
	mj.mj_forward(model, data)
	# start_agent_x=random.uniform(-45, 45)
	# start_agent_y=random.uniform(-30, 30)
	# start_ball_x=random.uniform(-45, 45)
	# start_ball_y=random.uniform(-30, 30)
	start_agent_x=0
	start_agent_y=0
	start_ball_x=5
	start_ball_y=0
	data.qpos[:2]=[start_agent_x, start_agent_y]
	data.qpos[7:9]=[start_ball_x, start_ball_y]
	# Init GLFW, create window, make OpenGL context current, request v-sync
	glfw.init()
	window = glfw.create_window(1200, 900, 'RL Team - Soccer Game', None, None)
	glfw.make_context_current(window)
	glfw.swap_interval(1)

	state=np.array([start_agent_x, start_agent_y, 0, 0, 0, start_ball_x, start_ball_y, 0, 0])

	# initialize visualization data structures
	mj.mjv_defaultCamera(cam)
	mj.mjv_defaultOption(opt)
	scene = mj.MjvScene(model, maxgeom=10000)
	context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)
    # Callback functions
	def keyboard(window, key, scancode, act, mods):
		if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
			mj.mj_resetData(model, data)
			mj.mj_forward(model, data)

	def mouse_button(window, button, act, mods):
		# update button state
		global button_left
		global button_middle
		global button_right

		button_left = (glfw.get_mouse_button(
			window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
		button_middle = (glfw.get_mouse_button(
			window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
		button_right = (glfw.get_mouse_button(
			window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

		# update mouse position
		glfw.get_cursor_pos(window)

	def mouse_move(window, xpos, ypos):
		# compute mouse displacement, save
		global lastx
		global lasty
		global button_left
		global button_middle
		global button_right

		dx = xpos - lastx
		dy = ypos - lasty
		lastx = xpos
		lasty = ypos


		# no buttons down: nothing to do
		if (not button_left) and (not button_middle) and (not button_right):
			return

		# get current window size
		width, height = glfw.get_window_size(window)

		# get shift key state
		PRESS_LEFT_SHIFT = glfw.get_key(
			window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
		PRESS_RIGHT_SHIFT = glfw.get_key(
			window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
		mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

		# determine action based on mouse button
		if button_right:
			if mod_shift:
				action = mj.mjtMouse.mjMOUSE_MOVE_H
			else:
				action = mj.mjtMouse.mjMOUSE_MOVE_V
		elif button_left:
			if mod_shift:
				action = mj.mjtMouse.mjMOUSE_ROTATE_H
			else:
				action = mj.mjtMouse.mjMOUSE_ROTATE_V
		else:
			action = mj.mjtMouse.mjMOUSE_ZOOM

		mj.mjv_moveCamera(model, action, dx/height,
						dy/height, scene, cam)

	def scroll(window, xoffset, yoffset):
		action = mj.mjtMouse.mjMOUSE_ZOOM
		mj.mjv_moveCamera(model, action, 0.0, -0.05 * yoffset, scene, cam)

	# install GLFW mouse and keyboard callbacks
	glfw.set_key_callback(window, keyboard)
	glfw.set_cursor_pos_callback(window, mouse_move)
	glfw.set_mouse_button_callback(window, mouse_button)
	glfw.set_scroll_callback(window, scroll)

	cam.azimuth = 90.38092929594274
	cam.elevation = -70.15643645584721
	cam.distance =  109.83430075014073
	cam.lookat =np.array([ 0.33268787911150655 , -2.0371257758709908e-17 , -2.6127905178878716 ])
	score=[]
	while not glfw.window_should_close(window):
		time_prev = data.time

		while (data.time - time_prev < 1/60.0):
			forward=state[4]
			mj.mj_step(model, data)
			#angle, speed = env.action_space.sample()
			# Select an action using the agent's policy
			action = agent.act(state)[0]
			#print(action)
			angle, speed= action
			forward, direction=move_and_rotate(data.xpos[8], angle, forward)
			# direction = np.array([1.0,0.0])
			speed_factor = 8
			direction = np.array(direction[:2])
			direction /= np.linalg.norm(direction)  # normalize the velocity vector
			data.qvel[:2] = speed_factor * speed * direction
			reward, goal, foul=compute_reward()
			a_pos, b_pos=data.xpos[8], data.xpos[9]
			agent_x, agent_y, agent_z = a_pos
			ball_x, ball_y, ball_z = b_pos
			#print(data.qvel)
			agent_vx, agent_vy=data.qvel[:2]
			ball_vx, ball_vy=data.qvel[7:9]
			# next_state=np.array([agent_x, agent_y, agent_vx, agent_vy, forward, ball_x, ball_y, ball_vx, ball_vy])
			
			#just a test remove it
			next_state=np.array([agent_x, agent_y, agent_vx, agent_vy, forward, ball_x, ball_y, ball_vx, ball_vy])
			
			agent.update_replay_buffer(state, action, reward, next_state, goal)
			agent.train()
			score.append(reward)
			state=next_state
			if goal or foul:
				break
		
		if goal or foul:
			break

		# End simulation based on time
		if (data.time>=simend):
			break

		# get framebuffer viewport
		viewport_width, viewport_height = glfw.get_framebuffer_size(window)
		viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

		#print camera configuration (help to initialize the view)
		if (print_camera_config==1):
			print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
			print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')

		# Update scene and render
		mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
		mj.mjr_render(viewport, scene, context)

		# swap OpenGL buffers (blocking call due to v-sync)
		glfw.swap_buffers(window)

		# process pending GUI events, call GLFW callbacks
		glfw.poll_events()
	glfw.terminate()
	return sum(score), score


state_size = env.observation_space.shape[0]
action_size = env.action_space.shape[0]
hidden_size = 256
agent = DDPG(state_size, action_size, hidden_size)

for i in range(1000):
    score, s_list = render_it()
    print(f"Episode {i+1} has the score of: {score}")

    # After updating the agent:
    actor_loss_value = agent.actor_loss_value
    critic_loss_value = agent.critic_loss_value
    agent.write_summary(i, score, actor_loss_value, critic_loss_value)

    if i % 50 == 0 and i != 0:
        agent.save(f"checkpoint_{i}")

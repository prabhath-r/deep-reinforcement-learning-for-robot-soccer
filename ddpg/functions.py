import math
import numpy as np
import os
import mujoco as mj
import glfw
import random


boundaries = ("Touch_lines1","Touch_lines2", "Touch_lines3", "Touch_lines4")

def Is_boundaries_touched():
    for i in range(len(data.contact.geom1)):
        if (data.geom(data.contact.geom1[i]).name == "sphero_agent" and data.geom(data.contact.geom2[i]).name in boundaries) or \
           (data.geom(data.contact.geom2[i]).name == "sphero_agent" and data.geom(data.contact.geom1[i]).name in boundaries):
            print("touched_boundary")
            return -10
    return 0

Goal = ("Goal_lines1", "Goal_lines2")

def Is_goal():
    for i in range(len(data.contact.geom1)):
        if (data.geom(data.contact.geom1[i]).name == "sphero_ball" and data.geom(data.contact.geom2[i]).name in Goal) or \
           (data.geom(data.contact.geom2[i]).name == "sphero_ball" and data.geom(data.contact.geom1[i]).name in Goal):
            print("Goal!!!")
            return 10
    return 0

def Is_goal_self():
    for i in range(len(data.contact.geom1)):
        if (data.geom(data.contact.geom1[i]).name == "sphero_agent" and data.geom(data.contact.geom2[i]).name in Goal) or \
           (data.geom(data.contact.geom2[i]).name == "sphero_agent" and data.geom(data.contact.geom1[i]).name in Goal):
            print("Wrong Goal!!!")
            return -10
    return 0

def compute_reward():
        goal_achieved_reward = Is_goal()              
        self_goal_penalty = Is_goal_self()            
        out_of_bound_penalty = Is_boundaries_touched() 

        reward = (
        goal_achieved_reward +
        self_goal_penalty +
        out_of_bound_penalty
        )
        return reward, True if goal_achieved_reward != 0.0 else False, True if out_of_bound_penalty != 0 or self_goal_penalty != 0 else False


xml_path = 'small_field.xml'
simend = 10

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "/" + xml_path)
xml_path = abspath

model = mj.MjModel.from_xml_path(xml_path)
data = mj.MjData(model)
cam = mj.MjvCamera()
opt = mj.MjvOption()

MAX_SPEED = 10  # Maximum speed of the agent
MIN_SPEED = 5   # Minimum speed of the agent
SPEED_SCALE = 0.5 


button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

def render_it():
    mj.mj_resetData(model, data)
    mj.mj_forward(model, data)
    start_ball_x=random.uniform(-9, 9)
    start_ball_y=random.uniform(-4.5, 4.5)
    start_agent_x=random.uniform(-9, 9)
    start_agent_y=random.uniform(-4.5, 4.5)
    
    data.qpos[:2]=[start_agent_x, start_agent_y]
    data.qpos[7:9]=[start_ball_x, start_ball_y]
    
    glfw.init()
    window = glfw.create_window(1200, 900, 'RL Team - Soccer Game', None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    scene = mj.MjvScene(model, maxgeom=10000)
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

    def keyboard(window, key, scancode, act, mods):
        if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            mj.mj_resetData(model, data)
            mj.mj_forward(model, data)

    def mouse_button(window, button, act, mods):
        global button_left, button_middle, button_right
        button_left = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
        button_middle = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
        button_right = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)
        glfw.get_cursor_pos(window)

    def mouse_move(window, xpos, ypos):
        global lastx
        global lasty
        global button_left
        global button_middle 
        global button_right
        
        dx = xpos - lastx
        dy = ypos - lasty
        lastx = xpos
        lasty = ypos

        if not (button_left or button_middle or button_right):
            return

        width, height = glfw.get_window_size(window)
        mod_shift = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS

        if button_right:
            action = mj.mjtMouse.mjMOUSE_MOVE_H if mod_shift else mj.mjtMouse.mjMOUSE_MOVE_V
        elif button_left:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H if mod_shift else mj.mjtMouse.mjMOUSE_ROTATE_V
        else:
            action = mj.mjtMouse.mjMOUSE_ZOOM

        mj.mjv_moveCamera(model, action, dx/height, dy/height, scene, cam)

    def scroll(window, xoffset, yoffset):
        action = mj.mjtMouse.mjMOUSE_ZOOM
        mj.mjv_moveCamera(model, action, 0.0, -0.05 * yoffset, scene, cam)

    glfw.set_key_callback(window, keyboard)
    glfw.set_cursor_pos_callback(window, mouse_move)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_scroll_callback(window, scroll)

    cam.azimuth = 90.38092929594274
    cam.elevation = -70.15643645584721
    cam.distance = 109.83430075014073
    cam.lookat = np.array([0.33268787911150655, -2.0371257758709908e-17, -2.6127905178878716])
    score = []
    episode_done = False

    goal_x, goal_y = 9.5, 0.0

    # Get the accessor objects for the agent and ball
    agent = model.body('agent')
    ball = model.body('ball')

    # Modify the movement section within your main loop:
    while not glfw.window_should_close(window) and not episode_done:
        
        time_prev = data.time
        while (data.time - time_prev < 1/5.0):
            mj.mj_step(model, data)

            agent_pos = data.xpos[agent.id][:2]
            ball_pos = data.xpos[ball.id][:2] # no z-axis

            # direction to the goal
            direction_to_goal = np.array([goal_x, goal_y]) - ball_pos  # Step 1
            direction_to_goal_normalized = direction_to_goal / np.linalg.norm(direction_to_goal)

            # Determine the point from where the agent should approach the ball to push it towards the goal
            some_distance_from_ball = 0.5
            approach_point = ball_pos - (direction_to_goal_normalized * some_distance_from_ball)  

            # If the agent is not close to the approach_point, move there; otherwise, push the ball towards the goal
            some_tolerance = 0.1
            if np.linalg.norm(agent_pos - approach_point) > some_tolerance:
                direction_vector = approach_point - agent_pos
            else:
                direction_vector = ball_pos - agent_pos
            
            # Compute the distance between the agent and the ball
            # distance_to_ball = np.linalg.norm(agent_pos - ball_pos)

            # Compute desired speed based on the distance to the ball
            # desired_speed = MIN_SPEED + SPEED_SCALE * distance_to_ball

            # Clip the desired speed to be within the defined limits
            # desired_speed = np.clip(desired_speed, MIN_SPEED, MAX_SPEED)

            # Update the agent's velocity based on the computed direction
            direction = direction_vector / np.linalg.norm(direction_vector)
            desired_speed = 10
            velocity = desired_speed * direction
            data.qvel[:2] = velocity
      
            touched_boundary = Is_boundaries_touched()
            scored_goal = Is_goal()
            self_goal = Is_goal_self()

            reward, goal, foul = compute_reward()

            if touched_boundary != 0 or scored_goal != 0 or self_goal != 0:
                episode_done = True
                break

            if reward < -10000: 
                episode_done = True
                break

            # Render the current scene
            viewport_width, viewport_height = glfw.get_framebuffer_size(window)
            viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)
            mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
            mj.mjr_render(viewport, scene, context)
            glfw.swap_buffers(window)
            glfw.poll_events()

    glfw.terminate()
    return sum(score), score

if __name__ == "__main__":
    render_it()


    
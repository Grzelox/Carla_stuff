import glob
import os 
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla 
import random 
import time
import numpy as np
import cv2

im_widht = 640
im_height = 480

def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((im_height, im_widht, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0

actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.filter('model3')[0] # model 3 blueprint 
    spawn_point = random.choice(world.get_map().get_spawn_points()) # random spawn point
    vehicle = world.spawn_actor(bp, spawn_point) # spawn vehicle
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0)) # change control
    actor_list.append(vehicle)
    time.sleep(5)

finally:
    #print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    #print('destroyed')
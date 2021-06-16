# Rhino
from compas.robots import Configuration, configuration
from compas_rhino.artists import RobotModelArtist

from compas.datastructures import Mesh
from compas.geometry import Circle
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Translation
from compas.robots import Joint
from compas.robots import RobotModel

import math

# create cylinder in yz plane
radius, length = 0.3, 5
cylinder = Cylinder(Circle(Plane([0, 0, 0], [1, 0, 0]), radius), length)
cylinder.transform(Translation.from_vector([length / 2., 0, 0]))

# create robot
model = RobotModel("robot", links=[], joints=[])

# add first link to robot
link0 = model.add_link("world")

# add second link to robot
mesh = Mesh.from_shape(cylinder)
link1 = model.add_link("link1", visual_mesh=mesh, visual_color=(1, 0, 0.))

# add the joint between the links
axis = (0, 0, 1)
origin = Frame.worldXY()
model.add_joint("joint1", Joint.CONTINUOUS, link0, link1, origin, axis)

# add another link
mesh = Mesh.from_shape(cylinder)  # create a copy!
link2 = model.add_link("link2", visual_mesh=mesh, visual_color=(0, 1., 0.))

# add another joint to 'glue' the link to the chain
axis = (0,1,0)
origin = Frame((length, 0, 0), (1, 0, 0), (0, 1, 0))
model.add_joint("joint2", Joint.CONTINUOUS, link1, link2, origin, axis)

# add another link
mesh = Mesh.from_shape(cylinder)  # create a copy!
link3 = model.add_link("link3", visual_mesh=mesh, visual_color=(0, 0., 1.))

# add another joint to 'glue' the link to the chain
axis = (0,0,1)
origin = Frame((length, 0, 0), (1, 0, 0), (0, 1, 0))
model.add_joint("joint3", Joint.CONTINUOUS, link2, link3, origin, axis)

# Create a configuration object matching the number of joints in your model
# configuration = ....
#config = []
#start_configuration = Configuration.from_revolute_values([ math.pi/2, math.pi/2], ['joint1', 'joint2'])
#end_configuration = Configuration.from_revolute_values([ 0., 0.], ['joint1', 'joint2'])

config = []
#config.append(start_configuration)
for i in range(0,16):
    config.append(Configuration.from_revolute_values([ i*math.pi/8, i*math.pi/8, i*math.pi/8], ['joint1', 'joint2', 'joint3']))
#config.append(end_configuration)

#print(start_configuration._joint_values)
#print(end_configuration._joint_values)

# Update the model using the artist
artist = RobotModelArtist(model)
# artist.update ...
for j in range(0,len(config)):
    artist.update(config[j], visual=True, collision=True)
    # Render everything
    artist.draw_visual()
    artist.redraw()

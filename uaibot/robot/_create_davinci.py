import robot as rb
from utils import Utils

from graphics.meshmaterial import MeshMaterial
from graphics.model3d import Model3D

from simobjects.ball import Ball
from simobjects.box import Box
from simobjects.cylinder import Cylinder
from simobjects.rigidobject import RigidObject
from simobjects.group import Group
from robot.links import Link
from robot._create_davinci_arm1 import _create_davinci_arm1
from robot._create_davinci_arm2 import _create_davinci_arm2
from robot._create_davinci_chest import _create_davinci_chest
import numpy as np

#from .links import *

#from robot._create_darwin_mini_arm import _create_darwin_mini_arm
#from robot._create_darwin_mini_leg_left import _create_darwin_mini_leg_left
#from robot._create_darwin_mini_leg_right import _create_darwin_mini_leg_right

import pickle


def _create_davinci(htm, name, color='#3e3f42', opacity=1, eef_frame_visible=True, joint_limits=None):

    if not Utils.is_a_matrix(htm, 4, 4):
        raise Exception(
            "The parameter 'htm' should be a 4x4 homogeneous transformation matrix.")

    if not (Utils.is_a_name(name)):
        raise Exception(
            "The parameter 'name' should be a string. Only characters 'a-z', 'A-Z', '0-9' and '_' are allowed. It should not begin with a number.")

    if not Utils.is_a_color(color):
        raise Exception(
            "The parameter 'color' should be a HTML-compatible color.")

    if (not Utils.is_a_number(opacity)) or opacity < 0 or opacity > 1:
        raise Exception(
            "The parameter 'opacity' should be a float between 0 and 1.")

    #desl_z = htm * Utils.trn([0, 0, -0.18])
    desl_z = htm * Utils.trn([0, 0, 0])

    arm1_links, arm1_base_3d_obj, arm1_htmbase, arm1_htmeef, arm1_q0 = _create_davinci_arm1(
        color=color, opacity=opacity)
    arm2_links, arm2_base_3d_obj, arm2_htmbase, arm2_htmeef, arm2_q0 = _create_davinci_arm2(
        color=color, opacity=opacity)
    chest = _create_davinci_chest(name=name, color=color, opacity=opacity)
    desl_z = htm * Utils.trn([0, 0, -0.18])
    robot_arm1 = rb.Robot(name + "__arm1", links=arm1_links,
                          list_base_3d_obj=arm1_base_3d_obj,
                          htm=np.identity(4),
                          htm_base_0=arm1_htmbase,
                          htm_n_eef=arm1_htmeef,
                          q0=arm1_q0, eef_frame_visible=eef_frame_visible,
                          joint_limits=joint_limits)
    robot_arm2 = rb.Robot(name + "__arm2", links=arm2_links,
                          list_base_3d_obj=arm2_base_3d_obj,
                          htm=np.identity(4),
                          htm_base_0=arm2_htmbase,
                          htm_n_eef=arm2_htmeef,
                          q0=arm2_q0, eef_frame_visible=eef_frame_visible,
                          joint_limits=joint_limits)
    return Group([robot_arm1, robot_arm2, chest])
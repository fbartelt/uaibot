import numpy as np


class _DisStructLinkObj:

    @property
    def link_number(self):
        """The index of the link in which the collision point is."""
        return self._link_number

    @property
    def link_col_obj_number(self):
        """The index of the collision object of the link in which the collision point is."""
        return self._link_col_obj_number

    @property
    def distance(self):
        """The distance (in meters) between the link and the object."""
        return self._distance

    @property
    def point_link(self):
        """The closest point (witness) in the link. Written in scenario coordinates and in meters."""
        return np.array(self._point_link)

    @property
    def point_object(self):
        """The closest point (witness) in the object. Written in scenario coordinates and in meters."""
        return np.array(self._point_object)

    @property
    def jac_distance(self):
        """The Jacobian of the distance in the robot's configuration space."""
        return np.array(self._jac_distance)

    #######################################
    # Constructor
    #######################################

    def __init__(self, link_number, link_col_obj_number, distance, point_link, point_object, jac_distance):

        self._link_number = link_number
        self._link_col_obj_number = link_col_obj_number
        self._distance = distance
        self._point_link = point_link
        self._point_object = point_object
        self._jac_distance = jac_distance

    #######################################
    # Std. Print
    #######################################

    def __repr__(self):

        string  = "Distance info: \n"
        string += " Link number: "+str(self.link_number)+"\n"
        string += " Collision object of the link number: "+str(self.link_col_obj_number )+"\n"
        string += " Distance: " + str(self.distance) + " m\n"
        string += " Point link: " + str(self.point_link.tolist()) + " m\n"
        string += " Point object: " + str(self.point_object.tolist()) + " m\n"
        string += " Jacobian distance: " + str(self._jac_distance.tolist()) + "\n"
        return string


class _DistStructRobotObj:

    #######################################
    # Attributes
    #######################################

    @property
    def obj(self):
        """Return the associated object."""
        return self._obj

    @property
    def robot(self):
        """Return the associated robot."""
        return self._robot

    @property
    def jac_dist_mat(self):
        """
		Return the matrix in which each row we have the distance Jacobian (gradient) for each robot link.
		"""
        return np.array(self._jac_dist_mat)

    @property
    def dist_vect(self):
        """
		Return the column vector in which each row we have the distance for each robot link.
		"""
        return np.array(self._dist_vect).reshape((self.no_items, 1))

    @property
    def no_items(self):
        """Return the number of items."""
        return self._no_items

    def __getitem__(self, key):
        return self._list_info[key]

    #######################################
    # Constructor
    #######################################

    def __init__(self, obj, robot):

        self._obj = obj
        self._robot = robot
        self._obj_name = obj.name
        self._robot_name = robot.name
        self._no_items = 0

        n = len(robot.links)
        self._list_info = []
        self._jac_dist_mat = np.zeros((0, n))
        self._dist_vect = []

    #######################################
    # Std. Print
    #######################################

    def __repr__(self):

        return "Distance struct between robot '" + self.robot.name + "' and object '" \
               + self.obj.name + "', with " + str(self.no_items) + " items"

    #######################################
    # Methods
    #######################################

    def _append(self, link_number, link_col_obj_number, distance, point_link, point_object, jac_distance):

        self._list_info.append(
            _DisStructLinkObj(link_number, link_col_obj_number, distance, point_link, point_object, jac_distance))

        self._jac_dist_mat = np.vstack((self._jac_dist_mat, jac_distance))
        self._dist_vect.append(distance)
        self._no_items += 1


    def get_item(self, link_number, link_col_obj_number):
        for dist_info in self._list_info:
            if link_number == dist_info.link_number and link_col_obj_number == dist_info.link_col_obj_number:
                return dist_info

        raise Exception("Item not found!")

    def get_closest_item(self):
        minimum_distance = float('inf')
        index_minimum = -1
        for i in range(self._no_items):
            if self[i].distance < minimum_distance:
                minimum_distance = self[i].distance
                index_minimum = i

        return self[index_minimum]


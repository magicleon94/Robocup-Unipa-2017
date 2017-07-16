"""
This module containts the class that manages the state and current targets of the robot
"""
import constants


class States(object):
    """ Class definition"""

    def __init__(self):
        self.colors = ["red", "blue", "yellow", "blue"]  # red blue yellow pill
        self.target_degrees = [constants.OBJECTS_FROM_START_DEGREE, constants.AREA_RED_FROM_OBJECTS_DEGREE,
                               constants.OBJECTS_FROM_RED_AREA_DEGREE, constants.AREA_BLUE_FROM_OBJECTS_DEGREE,
                               constants.OBJECTS_FROM_BLUE_AREA_DEGREE, constants.AREA_YELLOW_FROM_OBJECTS_DEGREE,
                               constants.OBJECTS_FROM_YELLOW_AREA_DEGREE, constants.AREA_BLUE_FROM_OBJECTS_DEGREE]
        self.progress = 0
        self.target_color = self.colors[self.progress]
        self.target_type = "object"
        self.target_heading = self.target_degrees[self.progress]

    def get_targets(self):
        """ Simply returns the current targets """
        return self.target_heading, self.target_type, self.target_color

    def state_transition(self):
        """ Handles the change of targets """

        self.progress += 1

        if self.progress >= 2 * len(self.colors):
            # This is the end of the road, no more targets
            self.target_color = None
            self.target_type = None
            self.target_heading = None
            return

        if self.progress % 2 == 0:
            self.target_type = "object"
        else:
            self.target_type = "area"

        self.target_heading = self.target_degrees[self.progress]
        self.target_color = self.colors[int(self.progress / 2)]

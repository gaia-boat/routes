# notes:
# Brazil is mostly on a negative latitude and always on a negative longitude
# A.O. representation
# (xb,ye)----------------------(xe,ye)
# |                            |
# |                            |
# |                            |
# |                            |
# (xb,yb)----------------------(xb,ye)


class MapRouter():
    def __init__(self, x_begin, x_end, y_begin, y_end):
        points = [
            (x_begin, y_begin), (x_begin, y_end),
            (x_end, y_begin), (x_end, y_end)]
        area_of_operations = []
        on_route = False
        evasion_in_progress = False
        current_position = (0, 0)   # tuple(latitude, longitude)

    def set_area(self):
        """
        Sets the area of operations for the boat, in a 2d array with geolocation
        points.
        """
        y_amp = abs(self.points[0][1] - self.points[1][1])
        x_amp = abs(self.points[0][0] - self.points[2][0])
        self.area_of_operations = [x_amp][y_amp]
        # need to set all points as geo locations

    def evade(self, current_pos, obstruction_size):
        """
        Traces and creates a evasion route if there is something obstructing the
        boat's path.
        """
        self.evasion_in_progress = True
        # stuff
        self.evasion_in_progress = False

    def _trace_route(self, parameter_list):
        """
        Traces a route using the area of operations map.
        """
        pass

    def _trace_evasion(self, parameter_list):
        """
        Traces an evasion route for the evade function
        """
        pass

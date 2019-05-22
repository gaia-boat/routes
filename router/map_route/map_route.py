import math
from router.macros import GPS_PRECISION

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
    """
    Class with the mapping functions for the router.
    """

    def __init__(self, x_begin, x_end, y_begin, y_end):
        self.points = [
            (x_begin, y_begin), (x_begin, y_end),
            (x_end, y_begin), (x_end, y_end)]
        self.area_of_operations = []
        self.on_route = False
        self.evasion_in_progress = False
        self.current_position = (30, 30)   # tuple(latitude, longitude)
        self.base_location = (0, 0)   # tuple(latitude, longitude)

    def set_area(self):
        """
        Sets the area of operations for the boat, in a 2d array with
        geolocation points.
        """
        y_amp = abs(self.points[0][1] - self.points[1][1])
        x_amp = abs(self.points[0][0] - self.points[2][0])
        self.area_of_operations = [x_amp][y_amp]

    def evade(self, current_pos, obstruction_size):
        """
        Traces and creates a evasion route if there is something obstructing
        the boat's path.
        """
        pass

    def _trace_collection_route(self):
        """
        Traces a route using the area of operations map.
        To trace the routes it is assumed that the points are in minutes if
        they are not in seconds they must be converted before this method is
        used.
        """
        if(self.current_position[0] < self.points[0][0]
                or self.current_position[0] > self.points[3][0]
                or self.current_position[1] < self.points[0][1]
                or self.current_position[1] > self.points[3][1]):
            return []
        route = []

        x = self.current_position[0]
        y = self.current_position[1]
        route.append((x, y))

        # go to the initial point in x axis
        while(x - self.points[0][0] >= GPS_PRECISION):
            x -= GPS_PRECISION
            route.append((x, y))

        # go to the initial point in y axis
        while(y - self.points[0][1] >= GPS_PRECISION):
            y -= GPS_PRECISION
            route.append((x, y))

        # travels the whole area
        while(self.points[3][1] - y >= GPS_PRECISION):
            list_of_x = self._unidimentional_router(x, 0)
            for new_x in list_of_x:
                x = new_x
                route.append((x, y))
            y += GPS_PRECISION
            route.append((x, y))
        return route

    def _unidimentional_router(self, pos, dimention):
        """
        Creates a list of positions to be followed, tracing linear routes.
        """
        route = []
        if(self.points[3][dimention] - pos <= GPS_PRECISION):
            while(pos - self.points[0][dimention] > GPS_PRECISION):
                pos -= GPS_PRECISION
                print(pos)
                route.append(pos)
        else:
            while(self.points[3][dimention] - pos > GPS_PRECISION):
                pos += GPS_PRECISION
                route.append(pos)
        return route

    def _trace_diagonal_route(self, pos, dest):
        """
        Traces a diagonal, or angled route moving at two axis at once.
        """
        x = pos[0]
        y = pos[1]
        dist_x = dest - x
        dist_y = dest - y
        dist_d = math.sqrt((dist_x*dist_x) + (dist_y*dist_y))

        GPS_PRECISION_x = GPS_PRECISION*dist_x/dist_d
        GPS_PRECISION_y = GPS_PRECISION*dist_y/dist_d

        if(pos[0] > dest[0]):
            GPS_PRECISION_x = GPS_PRECISION_x * -1
        if(pos[1] > dest[1]):
            GPS_PRECISION_y = GPS_PRECISION_y * -1

        route = list()
        while(abs(x - dest[0]) > GPS_PRECISION_x
                and abs(y - dest[1]) > GPS_PRECISION_y):
            x += GPS_PRECISION_x
            y += GPS_PRECISION_y
            route.append((x, y))

    def _trace_base_route(self):
        """
        Traces the most basic route given an area of operation.
        """

        x = self.current_position[0]
        y = self.current_position[1]

        route = []

        if(x > self.base_location[0]):
            while(x - self.base_location[0] >= GPS_PRECISION):
                x -= GPS_PRECISION
                route.append((x, y))
        else:
            while(self.base_location[0] - x >= GPS_PRECISION):
                x += GPS_PRECISION
                route.append((x, y))

        if(y > self.base_location[1]):
            while(y - self.base_location[1] >= GPS_PRECISION):
                y -= GPS_PRECISION
                route.append((x, y))
        else:
            while(self.base_location[1] - y >= GPS_PRECISION):
                y += GPS_PRECISION
                route.append((x, y))
        return route

    def _trace_evasion(self, parameter_list):
        """
        Traces an evasion route for the evade function
        """
        pass

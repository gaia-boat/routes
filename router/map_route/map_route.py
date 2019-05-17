import math

# notes:
# Brazil is mostly on a negative latitude and always on a negative longitude
# A.O. representation
# (xb,ye)----------------------(xe,ye)
# |                            |
# |                            |
# |                            |
# |                            |
# (xb,yb)----------------------(xb,ye)

#five meters in degrees
five_meters = 0.00004499633

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
        # need to set all points as geo locations

    def evade(self, current_pos, obstruction_size):
        """
        Traces and creates a evasion route if there is something obstructing
        the boat's path.
        """
        self.evasion_in_progress = True
        # stuff
        self.evasion_in_progress = False

    # To trace the routes it is assumed that the points are in minutes if
    # they are not in seconds they must be converted before this method.
    def _trace_collection_route(self):
        """
        Traces a route using the area of operations map.
        """
        if(self.current_position[0] < self.points[0][0]
                or self.current_position[0] > self.points[3][0]
                or self.current_position[1] < self.points[0][1]
                or self.current_position[1] > self.points[3][1]):
            return []
        route = []

        x = self.current_position[0]
        y = self.current_position[1]
        route.append((x,y))
        
        # goes to the point x0 
        while(x - self.points[0][0] >= five_meters):
            x -= five_meters
            route.append((x, y))

        # goes to the point y0
        while(y - self.points[0][1] >= five_meters):
            y -= five_meters
            route.append((x, y))

        # travels the whole area        
        while(self.points[3][1] - y >= five_meters):
            list_of_x = self._unidimentional_router(x,0)
            for new_x in list_of_x:
                x = new_x
                route.append((x,y))
            y += five_meters 
            route.append((x,y))
        return route

    def _unidimentional_router(self,pos,dimention):
        route = []
        if(self.points[3][dimention] - pos <= five_meters):
            while(pos - self.points[0][dimention] > five_meters):
                pos -= five_meters
                print(pos)
                route.append(pos)
        else:
            while(self.points[3][dimention] - pos > five_meters):
                pos += five_meters
                route.append(pos)
        return route

    def _trace_diagonal_route(self,pos,dest):
        x = pos[0]
        y = pos[1]
        dist_x = dest - x
        dist_y = dest - y
        dist_d = math.sqrt((dist_x*dist_x) + (dist_y*dist_y))
        five_meters_x = five_meters*dist_x/dist_d
        five_meters_y = five_meters*dist_y/dist_d
        if(pos[0] > dest[0]):
            five_meters_x = five_meters_x * -1
        if(pos[1] > dest[1]):
            five_meters_y = five_meters_y * -1
        
        route = []
        while(abs(x - dest[0]) > five_meters_x and abs(y - dest[1]) > five_meters_y):
            x += five_meters_x
            y += five_meters_y
            route.append((x,y))
            
    def _trace_base_route(self):
        """"""

        x = self.current_position[0]
        y = self.current_position[1]

        route = []

        if(x > self.base_location[0]):
            while(x - self.base_location[0] >= five_meters):
                x -= five_meters
                route.append((x, y))
        else:
            while(self.base_location[0] - x >= five_meters):
                x += five_meters
                route.append((x, y))

        if(y > self.base_location[1]):
            while(y - self.base_location[1] >= five_meters):
                y -= five_meters
                route.append((x, y))
        else:
            while(self.base_location[1] - y >= five_meters):
                y += five_meters
                route.append((x, y))
        return route

    def _trace_evasion(self, parameter_list):
        """
        Traces an evasion route for the evade function
        """
        pass

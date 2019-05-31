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


# rota sera subida e decida, tipo comprimento de onda
# funcsobeedesce()->verifica se sobe x->se puder, x++, senao fim de rota
# ->iterar pelo y ascendentemente sempre adicionando o par de coordenadas na rota
# ->verifica se pode subir x->se puder, x++,senao fim de rota
# ->iterar pelo y descendentemente sempre adicionando o par de coordenadas na rota->repete

# enquanto estiver em coleta, vou chamar sobeedesce ate acabar a rota.
# funcao de desvio deve funcionar do msm jeito

class MapRouter():
    """
    Class with the mapping functions for the router.
    """

    def __init__(self, begin, end, current, base):
        self.points = [begin, end]
        self.current_position = current
        self.base_location = base

    def trace_diagonal_route(self, destination):
        """
        Traces the smallest route between the current position and a given
        destination.
        """
        x = self.current_position[0]
        y = self.current_position[1]
        distance_x = destination[0] - x
        distance_y = destination[1] - y

        real_distance = math.sqrt(
            (distance_x * distance_x) + (distance_y * distance_y))

        five_meters_x = GPS_PRECISION * distance_x / real_distance
        five_meters_y = GPS_PRECISION * distance_y / real_distance

        route = []
        while(abs(x - destination[0]) > abs(five_meters_x) and
              abs(y - destination[1]) > abs(five_meters_y)):
            x += five_meters_x
            y += five_meters_y
            route.append((x, y))
        return route

    def trace_route_to_base(self):
        """
        Traces a route back to the base.
        """
        return self.trace_diagonal_route(self.base_location)

    def trace_collection_route(self):
        """
        Traces a route using the area of operations map.
        To trace the routes it is assumed that the points are in minutes if
        they are not in minutes conversion must happen before this method is
        used.
        """
        route = []

        x = self.current_position[0]
        y = self.current_position[1]

        while(self.points[1][0] - x > GPS_PRECISION):
            x += GPS_PRECISION
            route.append((x, y))

        if(self.points[1][1] - y >= GPS_PRECISION):
            print(self.points[0][0], x)
            y += GPS_PRECISION
            route.append((x, y))
            while(x - self.points[0][0] > GPS_PRECISION):
                x -= GPS_PRECISION
                route.append((x, y))

        return route

    def trace_evasion_route(self, route, blocked_pos, direction=None):
        """
        Traces an evasion route for the evade function. Must receive the blocked
        geolocation param.
        Returns a new route with the evasion manuver.

        Args:
        route = []

        blocked_pos = (lat, long)

        direction = None
        """
        reusable_route = route[blocked_pos:]

        if direction is not None:
            middle = self._get_center()
            return trace_evasion_route(route, blocked_pos, direction=direction)

        adjacent_blocked_route = tuple(
            blocked_pos[0], blocked_pos[1] + GPS_PRECISION)

        route_to_adjacent = self.trace_diagonal_route(adjacent_blocked_route)

        if blocked_pos == route[-1]:
            return route_to_adjacent

        return route_to_adjacent + reusable_route

    def set_current_pos(self, geolocation):
        """
        Setter for the current_pos attr.
        """
        self.current_position = geolocation

    def _get_center(self):
        """
        Gets the middle point inside the operation area.
        """
        return tuple((self.points[0][0] - self.points[1][0]) / 2,
                     (self.points[0][1] - self.points[1][1]) / 2)

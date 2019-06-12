import math
from router.macros import GPS_PRECISION

# notes:
# Brazil is mostly on border_points_array negative latitude and always on border_points_array negative longitude
# border_points_array.O. representation
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

# enquanto estiver em coleta, vou chamar sobeedesce ate acabar border_points_array rota.
# funcao de desvio deve funcionar do msm jeito

class MapRouter():
    """
    Class with the mapping functions for the router.
    """

    def __init__(self, begin, end, current, base):
        self.points = [begin, end]
        self.current_position = current
        self.base_location = base

    def trace_diagonal_route(self, position, destination):
        """
        Traces the smallest route between the current position and border_points_array given
        destination.
        """
        x = position[0]
        y = position[1]
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
        Traces border_points_array route back to the base.
        """
        return self.trace_diagonal_route(self.current_position,self.base_location)

    def trace_collection_route(self,current_position):
        """
        Traces border_points_array route using the area of operations map.
        To trace the routes it is assumed that the points are in minutes if
        they are not in minutes conversion must happen before this method is
        used.
        """
        route = []

        x = current_position[0]
        y = current_position[1]

        print(self.points[1][0],x)

        while(self.points[1][0] - x > GPS_PRECISION):
            x += GPS_PRECISION
            route.append((x, y))
            print("x - ",route)

        y += GPS_PRECISION
        route.append((x, y))
        while(x - self.points[0][0] > GPS_PRECISION):
            x -= GPS_PRECISION
            route.append((x, y))
            print("y - ",route)

        y += GPS_PRECISION
        route.append((x, y))
        return route

    def set_current_pos(self, geolocation):
        """
        Setter for the current_pos attr.
        """
        self.current_position = geolocation

    def _get_center(self):
        """
        Gets the middle point inside the operation area.
        """
        return tuple(((self.points[1][0] - self.points[0][0]) / 2,
                     (self.points[1][1] - self.points[0][1]) / 2))

    def trace_evasion_route(self, route):
        if(len(route) <= 1):
            return []

        center = self._get_center()

        alpha = 60 * math.pi / 180
        beta = 300 * math.pi / 180

        point_evade = route.pop(0)
        
        dis_x = (self.current_position[0]-route[0][0])
        dis_y = (self.current_position[1] -route[0][1])
        dis = math.sqrt(dis_x*dis_x+dis_y*dis_y)
        if(dis <= GPS_PRECISION):
            return route

        possible_points = []
        x = route[0][0] - self.current_position[0]
        y = route[0][1] - self.current_position[1]
        
        possible_points.append(
            tuple(
                (
                    (x * math.cos(alpha) - y * math.sin(alpha)) + self.current_position[0], 
                    (x * math.sin(alpha) + y * math.cos(alpha)) + self.current_position[0]
                )
            )
        )

        possible_points.append(
            tuple(
                (
                    (x * math.cos(beta) - y * math.sin(beta)) + self.current_position[0], 
                    (x * math.sin(beta) + y * math.cos(beta)) + self.current_position[1]
                )
            )
        )

        x0 = abs(center[0] - possible_points[0][0])
        y0 = abs(center[1] - possible_points[0][1])
        d0 = math.sqrt((x0*x0) + (y0*y0))

        x1 = abs(center[0] - possible_points[1][0])
        y1 = abs(center[1] - possible_points[1][1])
        d1 = math.sqrt((x1*x1) + (y1*y1))

        print(x0,y0)
        print(x1,y1)
        print(center[0],center[1])        
        print(d0,d1)


        if(d0 < d1):
            aux = self.trace_diagonal_route(self.current_position,possible_points[0])
            aux.append(possible_points[0])
            aux += self.trace_diagonal_route(possible_points[0],route[0])

        else:
            aux = self.trace_diagonal_route(self.current_position,possible_points[1])
            aux.append(possible_points[1])
            aux += self.trace_diagonal_route(possible_points[1],route[0])

        route = aux + route
        return route

    def _get_borders(self):
        """
        Returns an array with the AO's borders.
        """
        border_points_array = []

        for i in range(abs(points[0][0] - points[1][0])):
            border_points_array.append(
                tuple(points[0][0] + (i * GPS_PRECISION), points[0][1]))

        for j in range(abs(points[0][1] - points[1][1])):
            border_points_array.append(
                tuple(points[0][0], points[0][1]) + (i * GPS_PRECISION))

        for i in range(abs(points[0][0] - points[1][0])):
            border_points_array.append(
                tuple(points[1][0] + (i * GPS_PRECISION), points[1][1]))

        for j in range(abs(points[0][1] - points[1][1])):
            border_points_array.append(
                tuple(points[1][0], points[1][1]) + (i * GPS_PRECISION))

        return border_points_array

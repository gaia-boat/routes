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
# five_meters = 1

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
        self.points = [begin, end] # begin and end are tuples of floats
        self.current_position = current   # tuple(latitude, longitude)
        self.base_location = base   # tuple(latitude, longitude)

    def trace_diagonal_route(self,destination):
        """
        Traces the smallest route between the current position and a given
        destination.
        """
        x = self.current_position[0]
        y = self.current_position[1]
        distance_x = destination[0] - x
        distance_y = destination[1] - y
        
        #the real distance is calculated using pythagoras
        real_distance = math.sqrt((distance_x*distance_x)+(distance_y*distance_y))
        
        # using basic trigonometry i discovered the componets in x and y nescessary
        # to travel five meters in the direction of my destination
        five_meters_x = five_meters*distance_x/real_distance
        five_meters_y = five_meters*distance_y/real_distance
        
        route = []
        while(abs(x - destination[0]) > abs(five_meters_x) and abs(y - destination[1]) > abs(five_meters_y)):
            x += five_meters_x
            y += five_meters_y
            route.append((x,y))
        return route

    def trace_route_to_base(self):
        return self.trace_diagonal_route(self.base_location)


    def trace_collection_route(self):
        """
        Traces a route using the area of operations map.
        """
        route = []

        x = self.current_position[0]
        y = self.current_position[1]

        print(self.points[1][0],x)
        while(self.points[1][0] - x > five_meters):
            x += five_meters
            route.append((x,y))

        
        if(self.points[1][1] - y >= five_meters):            
            print(self.points[0][0],x)
            y += five_meters
            route.append((x,y))
            while(x - self.points[0][0] > five_meters):
                x -= five_meters
                route.append((x,y))
        
        return route

    def trace_evasion_route(self, parameter_list):
        """
        Traces an evasion route for the evade function
        """
        pass

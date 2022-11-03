from typing import OrderedDict
from manim import *
import random

class FiveRoutes(Scene):
    def generate_random_route(self,node_count):
        nodes = [i for i in range(node_count)]
        edges = [(i,i+1) for i in range(node_count - 1)]
        layout = OrderedDict()
        for i in range(node_count):
            layout[i] = (random.randint(-5,0),random.randint(-3,3),0)
        return Graph(nodes, edges,layout=layout )

    def construct(self):
        route_count = 5
        route_length = 4
        routes = [self.generate_random_route(route_length) for _ in range(route_count)]

        G = routes[0]
            
        steps = [
            Text("""routes = [

            ]""").scale(0.8).to_edge(RIGHT),
            Text("""routes = [
                route_1
            ]""").scale(0.8).to_edge(RIGHT),
            Text("""routes = [
                route_1,
                route_2
            ]""").scale(0.8).to_edge(RIGHT),
            Text("""routes = [
                route_1,
                route_2,
                route_3
            ]""").scale(0.8).to_edge(RIGHT),
            Text("""routes = [
                route_1,
                route_2,
                route_3,
                route_4
            ]""").scale(0.8).to_edge(RIGHT),
            Text("""routes = [
                route_1,
                route_2,
                route_3,
                route_4,
                route_5
            ]""").scale(0.8).to_edge(RIGHT)
        ]
        list_element = steps[0]
        self.play(Write(list_element))

        for i in range(0,len(routes)):
            G = routes[i]
            self.play(Create(G))
            
            self.play(
                FadeOut(G,target_position=list_element.get_center(),scale = (0.4)),
                Transform(list_element,steps[i+1])
            )

        self.play(list_element.animate.move_to(ORIGIN).scale(1.2))
        self.wait()
        self.play(Unwrite(list_element))
        self.wait()

FiveRoutes().render()
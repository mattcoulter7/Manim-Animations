from typing import OrderedDict, Tuple
from manim import *

class GraphStretch(Animation):
    def __init__(self, scene:Scene, graph: Graph,scale_factor: Tuple, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(graph,  **kwargs)
        scale_factor = [*scale_factor,0]
        scene.play(*[v.animate.move_to(v.get_center() * scale_factor) for v in graph.vertices.values()])



class AddingLocation(Scene):
    def construct(self):
        text = Tex("Solution 1").scale(2)
        self.play(Write(text))
        self.wait()
        self.play(Unwrite(text))

        # graph construction
        edges = []
        partitions = []
        c = 0
        layers = [5, 8, 8, 1]  # the number of neurons in each layer

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1)))
            c += i
        for i, v in enumerate(layers[1:]):
                last = sum(layers[:i+1])
                for j in range(v):
                    for k in range(last - layers[i], last):
                        edges.append((k + 1, j + last + 1))

        vertices = np.arange(1, sum(layers) + 1)
        graph = Graph(
            vertices,
            edges,
            layout='partite',
            partitions=partitions,
            vertex_config={'radius': 0.20}
        )
        self.add(graph)
        for v in graph.vertices.values():
            v.move_to(v.get_center() * (5,1,0))
        graph.update()

        #labels
        input_labels = ['flow(t-60)','flow(t-45)','flow(t-30)','flow(t-15)','t']
        input_elements = VGroup()
        for label,node in zip(input_labels,partitions[0]):
            vertice = graph.vertices[node]
            input_elements.add(MathTex(label).next_to(vertice,LEFT))
        self.add(input_elements)

        output_labels = ['flow(t)']
        output_elements = VGroup()
        for label,node in zip(output_labels,partitions[-1]):
            vertice = graph.vertices[node]
            output_elements.add(MathTex(label).next_to(vertice,RIGHT))
        self.add(output_elements)
        
        # show the input
        input_group = VGroup()
        input_group.add(graph.vertices[5])
        input_group.add(*[l for edge,l in graph.edges.items() if edge[0] == 5])
        input_group.add(input_elements[-1])
        self.play(FadeIn(input_group))
            

        self.wait(2)
                    

AddingLocation().render()
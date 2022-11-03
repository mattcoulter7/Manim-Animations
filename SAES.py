from typing import OrderedDict, Tuple
from manim import *
import math

class GraphStretch(Animation):
    def __init__(self, scene:Scene, graph: Graph,scale_factor: Tuple, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(graph,  **kwargs)
        scale_factor = [*scale_factor,0]
        scene.play(*[v.animate.move_to(v.get_center() * scale_factor) for v in graph.vertices.values()])

class SAES(Scene):
    def construct(self):
        title = Text("SAES").scale(2).to_edge(UP)
        self.play(Write(title))

        # graph construction
        edges = []
        partitions = []
        c = 0
        layers = [5,3,5,3,5,3,1]  # the number of neurons in each layer

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
        self.play(Create(graph))
        GraphStretch(self,graph,(2,1))
        
        #labels
        input_labels = ['flow(t-60)','flow(t-45)','flow(t-30)','flow(t-15)','scats']
        input_elements = VGroup()
        for label,node in zip(input_labels,partitions[0]):
            vertice = graph.vertices[node]
            input_elements.add(MathTex(label).next_to(vertice,LEFT))

        output_labels = ['flow(t)']
        output_elements = VGroup()
        for label,node in zip(output_labels,partitions[-1]):
            vertice = graph.vertices[node]
            output_elements.add(MathTex(label).next_to(vertice,RIGHT))
        
        layer_labels = ['input','encode','decode','encode','decode','fine tuning','output']
        layer_elements = VGroup()
        for label,layer in zip(layer_labels,partitions):
            bottom_node = layer[-1]
            vertice = graph.vertices[bottom_node]
            layer_elements.add(Tex(label).rotate(-math.pi/2).next_to(vertice,DOWN))
        self.play(Write(output_elements),Write(input_elements),Write(layer_elements))
        
        self.wait()
        self.play(
            Uncreate(graph),
            Unwrite(input_elements),
            Unwrite(output_elements),
            Unwrite(title),
            Unwrite(layer_elements)
        )

            

SAES().render()
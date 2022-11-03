from typing import OrderedDict, Tuple
from manim import *

class GraphStretch(Animation):
    def __init__(self, scene:Scene, graph: Graph,scale_factor: Tuple, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(graph,  **kwargs)
        scale_factor = [*scale_factor,0]
        scene.play(*[v.animate.move_to(v.get_center() * scale_factor) for v in graph.vertices.values()])

class AbsoluteTimeModel(Scene):
    def construct(self):
        title = Text("Absolute Time Model").scale(1.5).to_edge(UP)
        self.play(Write(title))

        # graph construction
        edges = []
        partitions = []
        c = 0
        layers = [3,5,5,5,1]  # the number of neurons in each layer

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
        input_labels = ['dayindex','t','scats']
        input_elements = VGroup()
        for label,node in zip(input_labels,partitions[0]):
            vertice = graph.vertices[node]
            input_elements.add(MathTex(label).next_to(vertice,LEFT))
        self.play(Write(input_elements))

        output_labels = ['flow(t)']
        output_elements = VGroup()
        for label,node in zip(output_labels,partitions[-1]):
            vertice = graph.vertices[node]
            output_elements.add(MathTex(label).next_to(vertice,RIGHT))
        self.play(Write(output_elements))
        self.wait()
        self.play(Uncreate(graph),Unwrite(input_elements),Unwrite(output_elements),Unwrite(title))       

AbsoluteTimeModel().render()
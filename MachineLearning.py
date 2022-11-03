from typing import OrderedDict, Tuple
from manim import *

class GraphStretch(Animation):
    def __init__(self, scene:Scene, graph: Graph,scale_factor: Tuple, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(graph,  **kwargs)
        scale_factor = [*scale_factor,0]
        scene.play(*[v.animate.move_to(v.get_center() * scale_factor) for v in graph.vertices.values()])

class MachineLearning(Scene):
    def construct(self):
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
        self.play(Create(graph))
        GraphStretch(self,graph,(5,1))
        
        #labels
        input_labels = ['flow(t-60)','flow(t-45)','flow(t-30)','flow(t-15)','scats']
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

        # data flow
        for partition in partitions:
            partition_paths = []
            for node in partition:
                connecting_nodes = list(filter(lambda a: a[0] == node,edges))
                if len(connecting_nodes) == 0: continue
                
                vertice = graph.vertices[node]
                
                dots = [Dot(color=DARK_BLUE).move_to(vertice.get_center()) for _ in connecting_nodes]
                paths = [TracedPath(d.get_center, dissipating_time=0.5, stroke_opacity=[0, 1],stroke_color=DARK_BLUE,stroke_width=4) for d in dots]
                
                connecting_vertices = [graph.vertices[n[1]] for n in connecting_nodes]
                partition_paths.append([dots,paths,connecting_vertices])
            
                self.add(*[d for d in dots],*[p for p in paths])
                self.play(
                    *[d.animate.move_to(v.get_center()) for v,d in zip(connecting_vertices,dots)]
                )
                self.play(*[FadeOut(d) for d in dots])
                    

MachineLearning().render()
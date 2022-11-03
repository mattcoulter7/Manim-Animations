from typing import OrderedDict, Tuple
from manim import *
from random import randrange
import math
import numpy as np
import csv
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

class GraphStretch(Animation):
    def __init__(self, scene:Scene, graph: Graph,scale_factor: Tuple, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(graph,  **kwargs)
        scale_factor = [*scale_factor,0]
        scene.play(*[v.animate.move_to(v.get_center() * scale_factor) for v in graph.vertices.values()])

class ModelPerLocation(Scene):
    def construct(self):
        #text = Tex("Solution 2").scale(2)
        #self.play(Write(text))
        #self.wait()
        #self.play(Unwrite(text))

        graph_group = VGroup()

        # graph construction
        edges = []
        partitions = []
        c = 0
        layers = [4, 8, 8, 1]  # the number of neurons in each layer

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
        graph_group.add(graph)
        for v in graph.vertices.values():
            v.move_to(v.get_center() * (5,1,0))
        graph.update()

        #labels
        input_labels = ['flow(t-60)','flow(t-45)','flow(t-30)','flow(t-15)']
        input_elements = VGroup()
        for label,node in zip(input_labels,partitions[0]):
            vertice = graph.vertices[node]
            input_elements.add(MathTex(label).next_to(vertice,LEFT))
        graph_group.add(input_elements)

        output_labels = ['flow(t)']
        output_elements = VGroup()
        for label,node in zip(output_labels,partitions[-1]):
            vertice = graph.vertices[node]
            output_elements.add(MathTex(label).next_to(vertice,RIGHT))
        graph_group.add(output_elements)

        self.add(graph_group)
        self.play(graph_group.animate.shift(LEFT*3,DOWN).scale(0.5))
        
        # map
        layout_scale = 3

        data = pd.read_csv("traffic_network2.csv", encoding='utf-8').fillna(0)
        lat_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Latitude'].values.reshape(-1, 1))
        long_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Longitude'].values.reshape(-1, 1))
        scaled_latitudes = lat_scaler.transform(data['Latitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        scaled_longitudes = long_scaler.transform(data['Longitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        neighbours = data['Neighbours'].values
        locations = data['SCATS Number'].values
        connections = []

        real_layout = {}
        
        for i in range(len(data.values)):
            scats = locations[i]
            real_layout[scats] = [scaled_longitudes[i],scaled_latitudes[i],0]

            for n in [int(x) for x in neighbours[i].split(';')]:
                connections.append((scats,n))
        G = Graph(locations,connections, layout = real_layout)
        G.to_edge(RIGHT)
        self.add(G)

        text_group = VGroup()
        for loc in G.vertices:
            pos = np.array(G.vertices[loc].get_center()) + np.array([-0.2,0.2,0])
            text_group.add(Text(str(loc)).move_to(pos).scale(0.3))

        self.add(text_group)
        
        self.wait(2)

        
        for v in list(G.vertices.values())[:5]:
            graph_copy = graph_group.copy()
            self.add(graph_copy)
            self.play(FadeOut(graph_copy,target_position=v.get_center(),scale=0.2))

        self.wait()
                    

ModelPerLocation().render()
from manim import *
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

config.background_color = BLACK

class Sites(MovingCameraScene):
    def construct(self):
        layout_scale = 3

        data = pd.read_csv("traffic_network2.csv", encoding='utf-8').fillna(0)
        lat_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Latitude'].values.reshape(-1, 1))
        long_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Longitude'].values.reshape(-1, 1))
        scaled_latitudes = lat_scaler.transform(data['Latitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        scaled_longitudes = long_scaler.transform(data['Longitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        neighbours = data['Neighbours'].values
        locations = data['SCATS Number'].values
        connections = []
        
        line_layout = {}
        for (i,loc) in enumerate(locations):
            line_layout[loc] = [i - len(locations) / 2,0,0]

        real_layout = {}
        
        for i in range(len(data.values)):
            scats = locations[i]
            real_layout[scats] = [scaled_longitudes[i],scaled_latitudes[i],0]

            for n in [int(x) for x in neighbours[i].split(';')]:
                connections.append((scats,n))

        self.camera.frame.save_state()
        G = Graph(locations,connections, layout = line_layout)
        
        self.play(Create(G))
        #self.add(graph1)

        self.play(G.animate.change_layout(real_layout))

        text_group = VGroup()
        for loc in real_layout:
            pos = np.array(real_layout[loc]) + np.array([-0.2,0.2,0])
            text_group.add(Text(str(loc),).move_to(pos).scale(0.3))

        self.play(Write(text_group))
        
        self.wait(1)

        self.play(Unwrite(text_group))

        self.play(Uncreate(G))
Sites().render()
from manim import *
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

config.background_color = BLACK

class LocationSupport2(MovingCameraScene):
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
        G = Graph(locations,connections, layout = real_layout)
        
        self.add(G)

        focus_vertice = G.vertices[4321]
        self.camera.frame.move_to(focus_vertice.get_center()).set(width=focus_vertice.width * 2)

        text_group = VGroup()
        for loc in real_layout:
            pos = np.array(real_layout[loc]) + np.array([-0.2,0.2,0])
            text_group.add(Text(str(loc),).move_to(pos).scale(0.3))

        self.add(text_group)
        
        self.wait(2)

        self.play(Restore(self.camera.frame))
        self.wait(4)
        self.play(Unwrite(text_group),G.animate.change_layout(layout=line_layout))
        self.wait()
        self.play(Uncreate(G))
        self.wait(2)
LocationSupport2().render()
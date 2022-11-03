from manim import *
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

config.background_color = BLACK

class DistanceCalculation(MovingCameraScene):
    def construct(self):
        # graph construction
        layout_scale = 3

        data = pd.read_csv("traffic_network2.csv", encoding='utf-8').fillna(0)
        lat_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Latitude'].values.reshape(-1, 1))
        long_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Longitude'].values.reshape(-1, 1))
        scaled_latitudes = lat_scaler.transform(data['Latitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        scaled_longitudes = long_scaler.transform(data['Longitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        neighbours = data['Neighbours'].values
        locations = data['SCATS Number'].values
        connections = []

        layout = {}
        
        for i in range(len(data.values)):
            scats = locations[i]
            layout[scats] = [scaled_longitudes[i],scaled_latitudes[i],0]

            for n in [int(x) for x in neighbours[i].split(';')]:
                connections.append((scats,n))

        self.camera.frame.save_state()
        G = Graph(locations,connections, layout = layout)
        

        text_group = VGroup()
        for i,vertice in enumerate(list(G.vertices.values())):
            long = data['Longitude'].values[i]
            lat = data['Latitude'].values[i]

            pos = np.array(vertice.get_center()) + np.array([-0.2,0.2,0])
            text_group.add(MathTex("(",f"{lat:.3f}",",",f"{long:.3f}",")").move_to(pos).scale(0.3))

        self.play(Create(G),Write(text_group))

        self.wait(1)

        # zoom into 2 points
        focus_group = VGroup(
            G.vertices[2846],
            G.vertices[970]
        )
        self.play(self.camera.frame.animate.move_to(focus_group.get_center()).set_width(focus_group.width*2))

        import_statement = Text("from geopy.distance import geodesic as GD").scale(0.5)
        
        text_970 = text_group[list(locations).index(970)]
        text_2846 = text_group[list(locations).index(2846)]

        variables = VGroup(text_970,text_2846)
        text_group.remove(text_970,text_2846)
        self.add(variables)
        eq1 = MathTex("GD(","(lat1", ",", "long1)",",","(lat2", ",", "long2)", ") =", "dist")
        eq2 = MathTex("GD(",f"({variables[0][1].tex_string}", ",", f"{variables[0][3].tex_string})",",",f"({variables[1][1].tex_string}", ",", f"{variables[1][3].tex_string})", ") =", "1.96km").scale(0.2)

        eq_group = VGroup(import_statement,eq1).arrange(DOWN).move_to(self.camera.frame.get_center()).scale(0.2).shift(LEFT * 0.5 + DOWN * 0.4)
        eq2.move_to(eq1.get_center())
        self.play(Write(eq_group))

        self.wait(0.5)
        self.play(TransformMatchingTex(Group(eq1, variables), eq2))
        self.wait(0.5)

        eq_group.add(eq2)
        eq_group.remove(eq1)
        self.play(
            self.camera.frame.animate
                .move_to(eq_group.get_center())
                .set_width(eq_group.width * 1.4),
            FadeOut(G),
            FadeOut(text_group)
        )

        self.play(Unwrite(import_statement),Unwrite(eq_group))
        self.wait(2)

DistanceCalculation().render()
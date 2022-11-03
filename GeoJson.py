from manim import *
import math
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

config.background_color = BLACK

class GeoJSON(Scene):
    def construct(self):

        json_data = Text("""{
        "type":"FeatureCollection",
        "features":[
            {
                "type":"Feature",
                "properties":{
                    "stroke":"#757575",
                    "stroke-width":5
                },
                "geometry":{
                    "type":"LineString",
                    "coordinates":[
                    [
                        145.0928369,
                        -37.8658025
                    ],
                    [
                        145.0950869,
                        -37.8534425
                    ],
                    ...
                    ]
                }
            }
        ]
        }""").scale(0.4).to_edge(RIGHT)

        route_data = Text("""--ROUTE 1--
        970 - WARRIGAL/HIGH ST RD
        3685 - WARRIGAL/HIGHBURY
        2000 - BURWOOD HWY/WARRIGAL/TOORAK
        4043 - BURKE/TOORAK
        4040 - BURKE/CAMBERWELL/RIVERSDALE
        4266 - BURWOOD/AUBURN/CAMBERWELL
        4264 - BURWOOD/GLENFERRIE
        4263 - BURWOOD/POWER
        3002 - BARKERS/DENMARK/POWER
        Length:		9
        Distance:		10.94km
        Cost:		15.93mins""").scale(0.4).to_edge(RIGHT)


        # graph construction
        layout_scale = 3
        data = pd.read_csv("traffic_network2.csv", encoding='utf-8').fillna(0)
        lat_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Latitude'].values.reshape(-1, 1))
        long_scaler = MinMaxScaler(feature_range=(-layout_scale, layout_scale)).fit(data['Longitude'].values.reshape(-1, 1))
        scaled_latitudes = lat_scaler.transform(data['Latitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        scaled_longitudes = long_scaler.transform(data['Longitude'].values.reshape(-1, 1)).reshape(1, -1)[0]
        neighbours = data['Neighbours'].values
        locations = data['SCATS Number'].values
        locations_list = list(locations)
        connections = []

        layout = {}
        
        for i in range(len(data.values)):
            scats = locations[i]
            layout[scats] = [scaled_longitudes[i],scaled_latitudes[i],0]

            for n in [int(x) for x in neighbours[i].split(';')]:
                connections.append((scats,n))

        G = Graph(locations,connections, layout = layout)
        self.play(Create(G))
        self.wait()

        # hide nodes not en route
        route = [970,3685,2000,4043,4040,4266,4264,4263,3002]
        route_connections = [(route[i],route[i+1]) for i in range(len(route) - 1)]
        
        focus_group = VGroup(
            *[G.vertices[i] for i in route],
            *[G.edges[i] for i in route_connections]
        )
        
        remove_edges = [e for e in G.edges.items() if e[1] not in focus_group]
        remove_vertices = [v for v in G.vertices.items() if v[1] not in focus_group]

        remove_edges_group = VGroup(*[e[1] for e in remove_edges])
        remove_vertices_group = VGroup(*[v[1] for v in remove_vertices])

        self.add(focus_group)
        self.play(
            FadeOut(remove_edges_group),
            FadeOut(remove_vertices_group)
        )
        filtered_remove_edges = []
        for e in remove_edges:
            shape = e[0]
            reversed_shape = (shape[1],shape[0])
            if reversed_shape not in filtered_remove_edges:
                filtered_remove_edges.append(shape)

        G.remove_edges(*[e for e in filtered_remove_edges])
        G.remove_vertices(*[e[0] for e in remove_vertices])

        self.play(G.animate.rotate(-math.pi/5).to_edge(LEFT).shift(UP + RIGHT * 0.6).scale(1.2))

        # add the text
        focus_texts = VGroup()
        for scats in route:
            index = locations_list.index(scats)
            long = data['Longitude'].values[index]
            lat = data['Latitude'].values[index]
            vertice = G.vertices[scats]

            focus_texts.add(
                MathTex(f"{scats} ","(",f"{lat:.3f}",",",f"{long:.3f}",")")
                    .scale(0.4)
                    .next_to(vertice,RIGHT)
            )

        self.play(Write(focus_texts))

        focus_texts_copy = focus_texts.copy()
        self.wait()
        self.play(
            FadeOut(focus_texts_copy,target_position=route_data.get_center(),scale = 0.5),
            Write(route_data)
        )

        self.wait()
        self.play(Transform(route_data,json_data))
        self.wait()

        image = ImageMobject('map.png')
        self.play(
            FadeOut(route_data,target_position=ORIGIN,scale=0.5),
            FadeOut(G,target_position=ORIGIN,scale=0.5),
            FadeOut(focus_texts,target_position=ORIGIN,scale=0.5),
            FadeIn(image)
        )
        self.wait(2)

GeoJSON().render()

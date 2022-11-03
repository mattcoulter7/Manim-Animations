from manim import *

from sklearn.preprocessing import MinMaxScaler

class CostFormula(Scene):
    def construct(self):
        text = MathTex(r"time = \frac{distance}{speed}").scale(2)
        self.play(Write(text))
        self.wait()
        self.play(text.animate.to_edge(UP).scale(0.6))

        G = Graph([1, 2, 3], [(1, 2), (2, 3)],
                        layout={1: [-5, 0, 0], 2: [0, 0, 0], 3: [5, 0, 0]}
                        )
        self.play(Create(G))

        lines = list(G.edges.values())
        vertices = list(G.vertices.values())

        line1 = lines[0]
        node = vertices[1]
        line2 = lines[1]

        line1_text = Text("segment1_time").scale(0.6).next_to(line1,UP)
        node_text = Text("+ 30s").scale(0.6).next_to(node,UP)
        line2_text = Text(" + segment2_time").scale(0.6).next_to(line2,UP)
        result_text = Text("= route_time").next_to(node,DOWN)

        self.play(Write(line1_text))
        self.play(Write(node_text))
        self.play(Write(line2_text))
        self.play(Write(result_text))

        self.wait(2)

        self.play(Unwrite(text),Uncreate(G),Unwrite(line1_text),Unwrite(node_text),Unwrite(line2_text),Unwrite(result_text))

CostFormula().render()
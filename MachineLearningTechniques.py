from typing import Tuple
from manim import *

class GraphStretch(Animation):
    def __init__(self, scene:Scene, graph: Graph,scale_factor: Tuple, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(graph,  **kwargs)
        scale_factor = [*scale_factor,0]
        scene.play(*[v.animate.move_to(v.get_center() * scale_factor) for v in graph.vertices.values()])

class MachineLearningTechniques(Scene):
    def construct(self):
        label_group = VGroup(
            VGroup(
                Text("GRU"),
                Text("LSTM"),
                Text("SAES")
            ).arrange(RIGHT),
            VGroup(
                Text("RNN",color=DARK_BLUE),
                Text("Absolute Time Model",color=DARK_BLUE)
            ).arrange(RIGHT).scale(0.8)
        ).scale(2)

        for text in label_group[0]:
            self.play(Write(text))
        self.wait(2)

        self.play(label_group[0].animate.scale(0.5).shift(DOWN))
        for text in label_group[1]:
            self.play(Write(text))

        self.wait(1)
        self.play(Unwrite(label_group))
        
                    

MachineLearningTechniques().render()
from manim import *

class DrawCircle(Scene):
    def construct(self):
        circle = Circle(color=WHITE,radius=1)
        self.play(Create(circle))
        self.wait(5)

DrawCircle().render()
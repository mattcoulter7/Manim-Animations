from manim import *

from sklearn.preprocessing import MinMaxScaler

class TitleSolution2(Scene):
    def construct(self):
        text = Tex("Solution 2").scale(2)
        self.play(Write(text))
        self.wait()
        self.play(Unwrite(text))

TitleSolution2().render()
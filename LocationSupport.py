from manim import *

config.background_color = WHITE

class LocationSupport(Scene):
    def construct(self):
        text = Text("""How can I learn about 
        41 Locations?""",color=BLACK).scale(0.6)
        self.play(Write(text))
        self.wait(2)
        self.play(Unwrite(text))
        

LocationSupport().render()
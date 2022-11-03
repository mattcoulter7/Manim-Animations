from manim import *

config.background_color = BLACK

class Count(Animation):
    def __init__(self, number: Integer, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)

class DatasetSize2(Scene):
    def construct(self):
        number = Integer(0).set_color(WHITE)
        group = VGroup(
            number,
            Text("training records").scale(0.5)
        ).arrange(DOWN)
        self.add(group)

        self.wait(2)
        
        number.add_updater(lambda a: group.arrange(DOWN))
        self.play(
            number.animate.scale(2),
            Count(number, 0, 330_000, rate_func=lingering)
        )
        self.wait(6)
        self.play(
            number.animate.scale(0.4),
            Count(number, 330_000, 8_000, rate_func=lingering)
        )
        self.wait(2)

DatasetSize2().render()
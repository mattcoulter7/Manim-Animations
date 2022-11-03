from manim import *
import math
import numpy as np

config.background_color = BLACK

class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)

class DatasetSize(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        x_min,x_max,x_step = 0,20,1
        y_min,y_max,y_step = 0,20,1
        axes = Axes(
            x_range=[x_min, x_max,x_step/2],
            y_range=[y_min,y_max,y_step/2],
            axis_config={"color": DARK_BLUE},
            x_axis_config={
                "include_tip":False,
            },
            y_axis_config={
                "include_tip":False,
            }
        )

        graph = axes.plot(lambda x: x, color=GREEN)

        self.play(Create(axes))
        self.play(Create(graph))

        moving_dot = Dot(axes.i2gp(graph.t_min, graph), color=ORANGE)
        dot_1 = Dot(axes.i2gp(graph.t_min, graph))
        dot_2 = Dot(axes.i2gp(graph.t_max, graph))

        self.add(axes, graph, dot_1, dot_2, moving_dot)
        self.play(self.camera.frame.animate.move_to(moving_dot.get_center() + RIGHT).scale(0.8))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center() + RIGHT)
        self.camera.frame.add_updater(update_curve)

        number = DecimalNumber().set_color(WHITE).scale(2)
        self.add(number)
        def update_number(mob):
            number.next_to(moving_dot)
        self.camera.frame.add_updater(update_number)
        #update_number(self.camera.frame)

        self.play(
            MoveAlongPath(moving_dot, graph, rate_func=lingering),
            Count(number, 0, 1000, run_time=8, rate_func=lingering),
            self.camera.frame.animate.scale(0.4)
        )
        self.camera.frame.remove_updater(update_curve)
        self.camera.frame.remove_updater(update_number)

        self.play(Restore(self.camera.frame))

DatasetSize().render()
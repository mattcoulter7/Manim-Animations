from manim import *
import math
import numpy as np
from pyparsing import White

config.background_color = BLACK

MAX_SPEED = 60 # estimate to be the speed limit for all roads
CAPACITY_SPEED = 32 # canvas says 48
MAX_FLOW_RATE = 1500 # canvas says 1800
A = -MAX_FLOW_RATE / (CAPACITY_SPEED * CAPACITY_SPEED)
B = -2 * CAPACITY_SPEED * A

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

def convert_flow_to_speed(flow: float, over_capacity: bool = False) -> float:
    # clamp the flow value to the flow capacity
    if B*B+4*A*flow < 0: return None

    if over_capacity:
        traffic_speed = (-B + math.sqrt(B*B+4*A*flow)) / (2 * A)
    else:
        traffic_speed = (-B - math.sqrt(B*B+4*A*flow)) / (2 * A)

    # select the min speed as traffic can't breach the speed limit
    return traffic_speed

def convert_flow_to_speed_clamped(flow: float, over_capacity: bool = False):
    return min(convert_flow_to_speed(flow,over_capacity),MAX_SPEED)

def original_conversion(flow: float):
    return (convert_flow_to_speed(flow,True),convert_flow_to_speed(flow,False))

class FlowVsSpeed(Scene):
    def construct(self):
        # 1. speed = speed_to_flow(flow)
        text = Text("speed = flow_to_speed(flow)")
        self.play(Write(text))
        self.wait()
        self.play(Unwrite(text))
        self.wait(2)

        # axes creation
        x_min,x_max,x_step = 0,MAX_FLOW_RATE,250
        y_min,y_max,y_step = 0,CAPACITY_SPEED * 2,20
        axes = Axes(
            x_range=[x_min, x_max-0.0001,x_step/2],
            y_range=[y_min,y_max,y_step/2],
            axis_config={"color": DARK_BLUE},
            x_axis_config={
                "numbers_to_include": range(x_min, x_max + x_step, x_step),
                "numbers_with_elongated_ticks":range(x_min, x_max + x_step, x_step),
                "include_tip":True,
            },
            y_axis_config={
                "numbers_to_include": range(y_min, y_max + y_step, y_step),
                "numbers_with_elongated_ticks":range(y_min, y_max + y_step, y_step),
                "include_tip":True,
            }
        )
        axes_labels = axes.get_axis_labels(x_label='flow', y_label='speed')
        self.play(Create(axes),Write(axes_labels))
        self.wait(2)

        # 2. draw the original model (white)
        upper_bound_graph_original = axes.plot(lambda x: convert_flow_to_speed(x,False), color=WHITE)
        lower_bound_graph_original = axes.plot(lambda x: convert_flow_to_speed(x,True), color=WHITE)
        self.play(Create(lower_bound_graph_original),Create(upper_bound_graph_original))
        self.wait(2)

        # 3. add the equation to the graph
        original_label = axes.get_graph_label(
            upper_bound_graph_original, r"x=-\frac{375}{256}y^{2}+\frac{375}{4}y", x_val=3*x_max/4, direction=UP
        )
        self.play(Write(original_label))
        self.wait(2)

        # 4. draw white point on both upper bound and lower bounds travelling from left to right of graph
        moving_dot_upper = Dot(axes.i2gp(upper_bound_graph_original.t_min, upper_bound_graph_original), color=WHITE,radius=0.12)
        dot_upper_label = VGroup(Text("("),DecimalNumber(0),Text(","),DecimalNumber(CAPACITY_SPEED*2),Text(")")).arrange(RIGHT).next_to(moving_dot_upper,LEFT)

        moving_dot_lower = Dot(axes.i2gp(lower_bound_graph_original.t_min, lower_bound_graph_original), color=WHITE,radius=0.12)
        dot_lower_label = VGroup(Text("("),DecimalNumber(0),Text(","),DecimalNumber(CAPACITY_SPEED*2),Text(")")).arrange(RIGHT).next_to(moving_dot_lower,LEFT)

        def on_dot_move(ele):
            dot_upper_label[3].set_value(convert_flow_to_speed(dot_upper_label[1].number,False))
            dot_lower_label[3].set_value(convert_flow_to_speed(dot_lower_label[1].number,True))
            dot_upper_label.arrange(RIGHT).next_to(moving_dot_upper,LEFT)
            dot_lower_label.arrange(RIGHT).next_to(moving_dot_lower,LEFT)

        moving_dot_upper.add_updater(on_dot_move)
        self.play(Create(moving_dot_upper),Create(moving_dot_lower),Write(dot_upper_label),Write(dot_lower_label))
        self.play(
            MoveAlongPath(moving_dot_upper, upper_bound_graph_original, rate_func=linear,run_time=4),
            MoveAlongPath(moving_dot_lower, lower_bound_graph_original, rate_func=linear,run_time=4),
            Count(dot_upper_label[1], 0, MAX_FLOW_RATE, run_time=4, rate_func=linear),
            Count(dot_lower_label[1], 0, MAX_FLOW_RATE, run_time=4, rate_func=linear),
        )
        moving_dot_upper.remove_updater(on_dot_move)
        self.play(
            Unwrite(original_label),
            Uncreate(moving_dot_upper),
            Uncreate(moving_dot_lower),
            Uncreate(dot_upper_label),
            Uncreate(dot_lower_label)
        )
        self.wait(2)
        # 5. color the top and bottom
        lower_bound_graph = axes.plot(lambda x: convert_flow_to_speed(x,True), color=DARK_BLUE)
        upper_bound_graph = axes.plot(lambda x: convert_flow_to_speed(x,False), color=RED)
        
        self.play(
            Create(lower_bound_graph),
            Create(upper_bound_graph),
            Uncreate(upper_bound_graph_original),
            Uncreate(lower_bound_graph_original),
        )


        lower_bound_label = axes.get_graph_label(
            lower_bound_graph, r"y=\frac{-B-\sqrt{B^{2}+4Ax}}{2A}", x_val=3*x_max/4, direction=DOWN
        )
        upper_bound_label = axes.get_graph_label(
            upper_bound_graph, r"y=\frac{-B+\sqrt{B^{2}+4Ax}}{2A}", x_val=3*x_max / 4, direction=UP
        )

        self.play(Write(lower_bound_label),Write(upper_bound_label))

        v1 = MathTex("v", "=",f"{CAPACITY_SPEED}")
        v2 = MathTex("q", "=",f"{MAX_FLOW_RATE}")
        v3 = MathTex("a", "=",r"\frac{-q}{v^2}")
        v4 = MathTex("b", "=","-2va")
        variables = VGroup(v1,v2,v3,v4).arrange(DOWN).shift(LEFT*3.6)
        self.play(Write(variables))
        self.wait(2)
        
        # 6. fade out bottom
        self.play(
            FadeOut(lower_bound_graph),
            FadeOut(lower_bound_label),
        )
        self.wait(1)

        # 7. fade in bottom, fade out top
        self.play(
            FadeIn(lower_bound_graph),
            FadeIn(lower_bound_label),
            FadeOut(upper_bound_graph),
            FadeOut(upper_bound_label),
        )
        self.wait(1)

        # 8. fade in top
        self.play(
            FadeIn(upper_bound_graph),
            FadeIn(upper_bound_label)
        )
        self.wait(1)

        # 9. draw speed limit
        speed_graph = axes.plot(lambda x: MAX_SPEED, color=RED)
        speed_label = axes.get_graph_label(
            speed_graph, label=f"y={MAX_SPEED}", x_val=3*x_max / 4, direction=UP
        )

        self.play(Create(speed_graph))
        self.play(Write(speed_label))
        self.wait(2)
        
        # 10. wrap top to speed limit        
        upper_bound_graph_clamped = axes.plot(lambda x: convert_flow_to_speed_clamped(x,False), color=RED)
        upper_bound_label_clamped = axes.get_graph_label(
            upper_bound_graph, r"y=min(\frac{-B+\sqrt{B^{2}+4Ax}}{2A},60)", x_val=3*x_max / 4, direction=UP
        )

        self.play(
            Transform(upper_bound_graph,upper_bound_graph_clamped),
            Transform(upper_bound_label,upper_bound_label_clamped),
            Uncreate(speed_graph),
            Uncreate(speed_label)
        )
        self.wait(2)

        # 11. add point at x = 1500
        self.play(
            Create(moving_dot_upper),
            Write(dot_upper_label)
        )
        self.wait(2)

        # 12. hide bottom line
        self.play(
            Uncreate(lower_bound_graph),
            Unwrite(lower_bound_label),
        )
        self.wait(2)

        # 13. uncreate everything
        self.play(
            Uncreate(upper_bound_graph),
            Uncreate(upper_bound_label),
            Uncreate(axes),
            Unwrite(axes_labels),
            Unwrite(variables),
            Uncreate(moving_dot_upper),
            Unwrite(dot_upper_label)
        )
        self.wait(2)

FlowVsSpeed().render()
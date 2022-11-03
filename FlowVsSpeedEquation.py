from manim import *

class FlowVsSpeedEquation(Scene):
    def example(self):
        equation_1 = MathTex("w", "\\times","v", "=", "1")
        equation_1.shift(UP*2).scale(2)
        equation_2 = MathTex("v", "=", "w^{-1}")
        equation_2.scale(2)
        equation_3 = MathTex("w", "\\times","w^{-1}", "=", "1")
        equation_3.shift(UP*2).scale(2)

        self.play(Write(equation_1), Write(equation_2))
        self.play(FadeOut(equation_1[2]))

        self.play(
            TransformMatchingShapes(
                VGroup(equation_1[0:2], equation_1[3:], equation_2[2].copy()),
                equation_3,
            )
        )

    def construct(self):
        v1 = MathTex("v", "=","30")
        v2 = MathTex("q", "=","1500")
        v3 = MathTex("a", "=",r"\frac{-q}{v^2}")
        v4 = MathTex("b", "=","-2va")
        variables = VGroup(v1,v2,v3,v4).arrange(RIGHT)

        equation1 = MathTex("y","=",r"\frac{-b \pm \sqrt{b^2 + 4ax}}{2a}")
        equation2 = MathTex("y","=",r"\frac{-(-2va) \pm \sqrt{((-2va))^2 + 4ax}}{2a}")
        equation3 = MathTex("y","=",r"v \pm \sqrt{4(va)^2 + 4ax}")
        equation4 = MathTex("y","=",r"v \pm \sqrt{(-2v(\frac{-q}{v^2}))^2 + 4(\frac{-q}{v^2})x}")
        equation5 = MathTex("y","=",r"v \pm \sqrt{\frac{4q^2-4qx}{v}}")
        
        equations = VGroup(variables,equation1,equation2,equation3,equation4,equation5).arrange(DOWN)
        self.add(equations)
        self.wait()


        pass

FlowVsSpeedEquation().render()
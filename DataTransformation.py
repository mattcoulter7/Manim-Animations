from manim import *

config.background_color = BLACK

class DataTransformation(Scene):
    def construct(self):
        dataset = VGroup(
            Text("SCATS Number: 0970"),
            Text("Location: WARRIGAL RD N of HIGH STREET RD"),
            Text("CD MELWAY: 060 G10"),
            Text("NB LATITUDE: -37.86703"),
            Text("NB LONGITUDE: 145.09159"),
            Text("HF VicRoads Internal: 249"),
            Text("VR Internal Stat: 182"),
            Text("VR Internal Loc: 1"),
            Text("NB TYPE SURVEY: 1"),
            Text("Start Time: 2006.10.01"),
            VGroup(Text("00:00"),Text(":"),Text("83")).arrange(),
            VGroup(Text("00:15"),Text(":"),Text("100")).arrange(),
            VGroup(Text("00:30"),Text(":"),Text("97")).arrange(),
            VGroup(Text("00:45"),Text(":"),Text("57")).arrange(),
            VGroup(Text("01:00"),Text(":"),Text("31")).arrange(),
            VGroup(Text("01:15"),Text(":"),Text("20")).arrange(),
            VGroup(Text("01:30"),Text(":"),Text("18")).arrange(),
            VGroup(Text("01:45"),Text(":"),Text("97")).arrange(),
            VGroup(Text("02:00"),Text(":"),Text("57")).arrange(),
            VGroup(Text("02:15"),Text(":"),Text("31")).arrange(),
            VGroup(Text("02:30"),Text(":"),Text("20")).arrange(),
            VGroup(Text("02:45"),Text(":"),Text("100")).arrange(),
            VGroup(Text("03:00"),Text(":"),Text("97")).arrange(),
            VGroup(Text("03:15"),Text(":"),Text("57")).arrange(),
            VGroup(Text("03:30"),Text(":"),Text("31")).arrange(),
            VGroup(Text("03:45"),Text(":"),Text("20")).arrange(),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5)
        dataset.to_edge(LEFT + UP)

        self.add(dataset)

        # remove elements
        remove_text_group = VGroup(*dataset[1:9])
        dataset.remove(*remove_text_group.submobjects)
        self.play(FadeOut(remove_text_group))

        # move elements up
        self.play(
            dataset.animate
                .arrange(DOWN, aligned_edge=LEFT)
                .to_edge(LEFT + UP)
        )

        # show transformations
        new_datasets = []
        time_index = 2
        for _ in range(time_index,len(dataset.submobjects)):
            scats_ele = dataset[0].copy()
            date_ele = dataset[1].copy()
            time_ele = dataset[time_index]
            
            dataset.remove(scats_ele,date_ele,time_ele)

            new_dataset = VGroup(
                scats_ele,
                date_ele,
                time_ele[0],
                time_ele[2]
            )

            time_ele.remove(time_ele[0],time_ele[2])
            dataset.remove(time_ele)

            self.play(
                new_dataset.animate
                    .arrange(DOWN,aligned_edge=RIGHT)
                    .scale(1.5)
                    .to_edge(RIGHT + UP),
                dataset.animate
                    .arrange(DOWN, aligned_edge=LEFT)
                    .to_edge(LEFT + UP)
            )

            new_dataset[2] = VGroup(Text("Time: ").scale(0.67),new_dataset[2]).arrange()
            new_dataset[3] = VGroup(Text("Flow: ").scale(0.67),new_dataset[3]).arrange()
            new_dataset.arrange(DOWN,aligned_edge=RIGHT).to_edge(RIGHT + UP)

            self.play(
                Write(new_dataset[2][0]),
                Write(new_dataset[3][0])
            )
            
            # draw a box
            rect = SurroundingRectangle(new_dataset, buff = .1,color=DARK_BLUE)
            self.play(
                Create(rect),
            )
            new_dataset.add(rect)

            # Move previous left, and fade out older one
            self.play(
                new_dataset.animate
                    .scale(0.5)
                    .to_edge(DOWN + RIGHT),
                *[d.animate.shift(LEFT * 3) for d in new_datasets[-2:]],
                *[FadeOut(d) for d in new_datasets[-3:-2]],
                *[Uncreate(d[-1]) for d in new_datasets[-3:-2]]
            )
            new_datasets.append(new_dataset)

        self.wait(1)

DataTransformation().render()
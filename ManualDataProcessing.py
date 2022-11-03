from manim import *
import math
import numpy as np

class ManualDataProcessing(MovingCameraScene):
    def construct(self):
        raw_data = [
    "2200",
    "MAROONDAH/UNION",
    "INT",
    "-37.81631",
    "145.09812",
    "3126;4063",
    "2820",
    "CHANDLER HWY/PRINCESS",
    "INT",
    "-37.79477",
    "145.03077",
    "3662;4321",
    "2825",
    "EASTERN/BURKE",
    "INT",
    "-37.78661",
    "145.06202",
    "4030;2827;2820",
    "2827",
    "EASTERN/BULLEEN/THOMPSONS",
    "INT",
    "-37.78093",
    "145.07733",
    "2825;4051",
    "2846",
    "MONASH/HIGH ST RD",
    "INT",
    "-37.8612671",
    "145.058038",
    "970",
    "3001",
    "BARKERS/CHURCH/HIGH",
    "INT",
    "-37.81441",
    "145.02243",
    "3002;3662;4821;4262",
    "3002",
    "BARKERS/DENMARK/POWER",
    "INT",
    "-37.81489",
    "145.02663",
    "3001;3662;4263;4035",
    "3120",
    "BURKE/CANTERBURY",
    "INT",
    "-37.82264",
    "145.05734",
    "4035;3122;4040",
    "3122",
    "CANTERBURY/STANHOPE",
    "INT",
    "-37.82379",
    "145.06466",
    "3120;3127;3804",
    "3126",
    "CANTERBURY/WARRIGAL/UNION",
    "INT",
    "-37.82778",
    "145.09885",
    "3127;2200;3682",
    "3127",
    "CANTERBURY/BALWYN",
    "INT",
    "-37.82506",
    "145.078",
    "3122;4063;3126",
    "3180",
    "DONCASTER/BALWYN",
    "INT",
    "-37.79611",
    "145.08372",
    "4051;4057",
    "3662",
    "HIGH/DENMARK",
    "INT",
    "-37.80876",
    "145.02757",
    "3001;3002;4324;4335;2820",
    "3682",
    "WARRIGAL/RIVERSDALE",
    "INT",
    "-37.83695",
    "145.09699",
    "3126;3804;2000",
    "3685",
    "WARRIGAL/HIGHBURY",
    "INT",
    "-37.85467",
    "145.09384",
    "2000;0970",
    "3804",
    "RIVERSDALE/TRAFALGAR/STANHOPE",
    "INT",
    "-37.83331",
    "145.06247",
    "4040;3122;3812;3682",
    "3812",
    "CAMBERWELL/SEYMOUR/TRAFALGAR",
    "INT",
    "-37.83738",
    "145.06119",
    "3804;4040",
    "4030",
    "BURKE/DONCASTER/KILBY/HIGH",
    "INT",
    "-37.79561",
    "145.06251",
    "4321;4032;4051;2825",
    "4032",
    "BURKE/BELMORE/HARP",
    "INT",
    "-37.80202",
    "145.06127",
    "4321;4030;4057;4034",
    "4034",
    "BURKE/COTHAM/WHITEHORSE",
    "INT",
    "-37.81147",
    "145.05946",
    "4324;4032;4063;4035",
    "4035",
    "BURKE/BARKERS/MONT ALBERT",
    "INT",
    "-37.8172654",
    "145.0583603",
    "3002;4034;3120",
    "4040",
    "BURKE/CAMBERWELL/RIVERSDALE",
    "INT",
    "-37.83256",
    "145.05545",
    "4272;3120;3804;3812;4043;4266",
    "4043",
    "BURKE/TOORAK",
    "INT",
    "-37.84683",
    "145.05275",
    "4273;4040;2000",
    "4051",
    "DONCASTER/BULLEEN/SEVERN",
    "INT",
    "-37.79419",
    "145.0696",
    "4030;3180;2827",
    "4057",
    "BALWYN/BELMORE",
    "INT",
    "-37.80431",
    "145.08197",
    "4032;3180;4063",
    "4063",
    "WHITEHORSE/BALWYN/MAROONDAH",
    "INT",
    "-37.81404",
    "145.0801",
    "4034;4057;2200;3127",
    "4262",
    "BURWOOD/CHURCH",
    "INT",
    "-37.82155",
    "145.01503",
    "3001;4263",
    "4263",
    "BURWOOD/POWER",
    "INT",
    "-37.8228462",
    "145.0251292",
    "4262;3002;4264"
]
            
        grid = VGroup(*map(lambda cell: Text(cell),raw_data)).scale(0.5).arrange_in_grid(28,6)

        self.camera.frame.set(width=grid.width)
        
        self.play(Write(grid))
        target_ele = grid[73] # cell
        
        self.play(
            self.camera.frame.animate.move_to(target_ele.get_center()).set(width=target_ele.width)
        )

        new_text = Text("/PRINCESS/S'PARK/COTHAM",color=DARK_BLUE).scale(0.5).set_opacity(0)
        updated_cell = VGroup(target_ele,new_text)
        grid[73] = updated_cell
        
        updated_cell.arrange()
        grid.arrange_in_grid(28,6)

        def on_update(ele):
            self.camera.frame.move_to(updated_cell.get_center())
        
        new_text.add_updater(on_update)
        self.play(
            self.camera.frame.animate.set(width=updated_cell.width)
        )
        new_text.remove_updater(on_update)

        new_text.set_opacity(1)
        self.play(Write(new_text))

        rect = SurroundingRectangle(updated_cell, buff = .1,color=DARK_BLUE)
        updated_cell.add(rect)
        self.play(
            Create(rect),
            self.camera.frame.animate.move_to(grid.get_center()).set(width=grid.width)
        )
        self.wait(2)
        self.play(Unwrite(grid))

ManualDataProcessing().render()
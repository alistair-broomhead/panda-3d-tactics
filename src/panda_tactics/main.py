from panda3d.core import (
    PointLight,
    AmbientLight,
)

from panda_tactics.base import TacticsBase
from panda_tactics.camera import PlayerCamera
from panda_tactics.controls import Controls
from panda_tactics.models import Model, GridBox


class PandaTactics:
    selected = None

    def make_light(self):
        render = self.base.render

        ambient_light = AmbientLight("global_illumination")
        ambient_light.set_color((0.1, 0.1, 0.1, 0))
        ambient = render.attach_new_node(ambient_light)
        render.set_light(ambient)

        light_node = PointLight("point_light")
        light_node.set_color((1, 1, 1, 0))
        light_node.set_max_distance(30)

        light = render.attach_new_node(light_node)
        light.set_pos(-2, 10, 5)
        render.set_light(light)

    def make_map(self):
        # This could be called on any  subclass, but I prefer to be explicit
        Model.associate_base(self.base)

        self.grid.clear()

        # So far we're only working on a flat plane, eventually we'll have a json level representation
        h = 0

        for x in range(-10, 11):
            for y in range(-10, 11):
                self.grid[x, y, h] = GridBox((x, y, h))

    def __init__(self):
        self.grid = {}
        self.base = TacticsBase()

        # This could be called on any  subclass, but I prefer to be explicit
        Model.associate_base(self.base)

        self.make_map()
        self.make_light()

        self.camera = PlayerCamera(
            self.base.camera, on_move=self.select_cube, target=(0, -10, 0)
        )
        self.controls = Controls(self.camera)

    def select_cube(self, pos):
        pos = tuple(pos)

        if pos in self.grid:
            self.selected = self.grid[pos].select()
        elif self.selected is not None:
            self.selected = self.selected.deselect()

    def run(self):
        self.base.run()

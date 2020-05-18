# Panda3D provides that unhelpfully orphaned 'direct' package as well as its own
# noinspection PyPackageRequirements
from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight

from panda_tactics.camera import PlayerCamera
from panda_tactics.controls import Controls
from panda_tactics.models import Model, GridBox


class PandaTactics:
    selected = None

    def make_light(self):

        # set up a light source
        light_node = PointLight("point_light")
        light_node.set_color((1, 1, 1, 1))
        light_node.set_max_distance(10)

        light = self.app.render.attach_new_node(light_node)
        light.set_pos(0.5, 0.5, 3)
        self.app.render.set_light(light)

    def make_map(self):
        # This could be called on any  subclass, but I prefer to be explicit
        Model.associate_app(self.app)

        self.grid.clear()

        # So far we're only working on a flat plane, eventually we'll have a json level representation
        h = 0
        for x in range(-10, 11):
            for y in range(-10, 11):
                self.grid[x, y, h] = GridBox((x, y, h))

    def __init__(self):

        self.grid = {}
        self.app = ShowBase()
        self.app.disable_mouse()

        # This could be called on any  subclass, but I prefer to be explicit
        Model.associate_app(self.app)

        self.make_map()
        self.make_light()

        self.camera = PlayerCamera(
            self.app.camera,
            on_move=self.select_cube
        )
        self.controls = Controls(self.camera)

    def select_cube(self, pos):
        pos = tuple(pos)

        if pos in self.grid:
            self.selected = self.grid[pos].select()
        elif self.selected is not None:
            self.selected = self.selected.deselect()

    def run(self):
        self.app.run()

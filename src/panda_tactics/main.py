# Panda3D provides that unhelpfully orphaned 'direct' package as well as its own
# noinspection PyPackageRequirements
from direct.showbase.ShowBase import ShowBase

from panda_tactics.camera import (
    PlayerCamera,
)
from panda_tactics.controls import Controls


class PandaTactics:
    def make_map(self):
        loader = self.app.loader
        scene = self.app.render

        for x in range(-10, 10):
            for y in range(-10, 10):
                cube = loader.load_model('models/box')
                cube.reparent_to(scene)
                cube.set_scale(0.9, 0.9, 0.9)
                cube.set_pos(x, y, 0)

    def __init__(self):
        self.app = ShowBase()
        self.app.disable_mouse()
        self.camera = PlayerCamera(self.app.camera)
        self.controls = Controls(self.camera)

        self.make_map()

    def run(self):
        self.app.run()

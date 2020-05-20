# Panda3D provides that unhelpfully orphaned 'direct' package as well as its own
# noinspection PyPackageRequirements
from direct.filter.CommonFilters import CommonFilters

# noinspection PyPackageRequirements
from direct.showbase.ShowBase import ShowBase


class TacticsBase(ShowBase):
    def __init__(self, start_direct=True, window_type=None):
        super().__init__(fStartDirect=start_direct, windowType=window_type)
        self.disable_mouse()
        self.setBackgroundColor(0, 0, 0)

        self.filters = CommonFilters(self.win, self.cam)
        self.filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, intensity=5.0, size=1)

        self.bufferViewer.setPosition("llcorner")
        self.bufferViewer.setLayout("hline")
        self.backface_culling_on()

        self.task_mgr.do_method_later(
            delayTime=0,
            funcOrTask=self.bufferViewer.enable,
            extraArgs=(1,),
            name="Enable Buffer Viewer",
        )

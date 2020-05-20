from panda_tactics.models.decoration import material, Palette
from panda_tactics.models.model import Model


class GridBox(Model):
    _selected = None

    def __str__(self):
        return f'GridBox({self.pos}, selected={self.selected})'

    class Materials:
        main_unselected = material(1, Palette.specular_purple)
        main_selected = material(1, Palette.specular_purple)
        highlight = material(0, Palette.emission_yellow)

    def select(self):
        self.selected = True
        return self

    def deselect(self):
        self.selected = False

    def _update_selected(self):
        selected = self.selected
        if selected:
            self._outline.set_color(Palette.ambient_blue)
            self._outline.set_material(self.Materials.main_selected, 1)
            self._highlight.show()
        else:
            self._outline.set_color(Palette.ambient_light_blue)
            self._outline.set_material(self.Materials.main_unselected, 1)
            self._highlight.hide()

    @classmethod
    def _set_selected(cls, new_obj):
        prev_obj = cls._selected
        cls._selected = new_obj

        for obj in prev_obj, new_obj:
            if isinstance(obj, cls):
                obj._update_selected()

    def __init__(self, pos, selected=False):

        super().__init__(pos=pos)

        self.node = self._loader.new_node(self)
        self.node.set_pos(pos)

        self._outline = self._loader.load_model(
            'grid-box-outline',
            parent=self.node,
            two_sided=True,
        )
        self._highlight = self._loader.load_model(
            'grid-box-highlight',
            parent=self.node,
            two_sided=True,
            colour=Palette.ambient_yellow,
            material_=self.Materials.highlight,
        )

        if selected:
            self._set_selected(self)
        else:
            self._update_selected()

    @property
    def selected(self):
        return self._selected is self

    @selected.setter
    def selected(self, is_selected: bool):
        if is_selected:
            self._set_selected(self)
        elif self.selected:
            self._set_selected(None)

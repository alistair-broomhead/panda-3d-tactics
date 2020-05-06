from direct.showbase.DirectObject import DirectObject


class Binding:
    def __init__(self):
        self._accept = {}
        self.obj = DirectObject()

    def set(self, key):
        def bind(method):
            self._accept[key] = method.__name__

            return method
        return bind

    def bind(self, obj):
        for key, meth in self._accept.items():
            self.obj.accept(key, getattr(obj, meth))
            self.obj.accept(f'{key}-repeat', getattr(obj, meth))


class Controls:
    _bindings = Binding()

    def __init__(self, camera):
        self.camera = camera
        self._bindings.bind(self)

    @_bindings.set('w')
    def target_up(self):
        self.camera.retarget_relative(y=1)

    @_bindings.set('a')
    def target_left(self):
        self.camera.retarget_relative(x=-1)

    @_bindings.set('s')
    def target_down(self):
        self.camera.retarget_relative(y=-1)

    @_bindings.set('d')
    def target_right(self):
        self.camera.retarget_relative(x=1)

    @_bindings.set('arrow_up')
    def rotate_focus_up(self):
        self.camera.refocus_relative(latitude=-10)

    @_bindings.set('arrow_down')
    def rotate_focus_down(self):
        self.camera.refocus_relative(latitude=10)

    @_bindings.set('arrow_left')
    def rotate_focus_left(self):
        self.camera.refocus_relative(longitude=-30)

    @_bindings.set('arrow_right')
    def rotate_focus_right(self):
        self.camera.refocus_relative(longitude=30)

    @_bindings.set('shift')
    def zoom_out(self):
        self.camera.refocus_relative(distance=5)

    @_bindings.set('control')
    def zoom_in(self):
        self.camera.refocus_relative(distance=-5)

    @_bindings.set('escape')
    def exit(self):
        exit(0)


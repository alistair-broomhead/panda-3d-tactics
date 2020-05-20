import json
import pathlib

from panda3d.core import *


def read_model(model):
    def process_node(geometry_node):
        for i in range(geometry_node.getNumGeoms()):
            return process(geometry_node.getGeom(i))

    def process(geom):
        vertex_data = geom.getVertexData()
        return {
            'vertices': tuple(process_vertices(vertex_data)),
            'triangles': tuple(
                process_primitive(geom.getPrimitive(i))
                for i in range(geom.getNumPrimitives())
            ),
        }

    def process_vertices(vertex_data):
        vertex = GeomVertexReader(vertex_data, 'vertex')
        while not vertex.isAtEnd():
            yield tuple(vertex.getData3())

    def process_primitive(primitive):
        primitive = primitive.decompose()

        return tuple(
            tuple(
                primitive.getVertex(i) for i in range(
                    primitive.getPrimitiveStart(p),
                    primitive.getPrimitiveEnd(p),
                )
            )
            for p in range(primitive.getNumPrimitives())
        )

    for geometry_node_path in model.findAllMatches('**/+GeomNode'):
        return process_node(geometry_node_path.node())


def create_vertex_data(model_name, vertices):
    vertex_data = GeomVertexData(
        model_name,
        GeomVertexFormat.get_v3(),
        Geom.UHStatic,
    )
    vertex_data.set_num_rows(len(vertices))
    writer = GeomVertexWriter(vertex_data, 'vertex')
    for vertex in vertices:
        writer.add_data3f(*vertex)

    return vertex_data


def create_triangles(primitives):
    for triangles in primitives:
        prim = GeomTriangles(Geom.UHStatic)
        for triangle in triangles:
            prim.add_vertices(*triangle)
        yield prim


class Loader:

    _model_path = pathlib.Path('assets/models')

    def __init__(self, base):
        self.base = base
        self._loaded = {}
        self._geom = {}

    def new_node(self, name):
        return self.base.render.attach_new_node(
            GeomNode(str(name))
        )

    def _raw_geometry(self, model_name):
        if model_name in self._loaded:
            return self._loaded[model_name]

        json_file_name = self._model_path / f'{model_name}.json'

        try:
            with open(json_file_name) as json_file:
                geometry = self._loaded[model_name] = json.load(json_file)
        except FileNotFoundError:
            geometry = self._loaded[model_name] = read_model(
                self.base.loader.load_model(
                    str((self._model_path / model_name).as_posix())
                )
            )
            with open(json_file_name, 'w') as json_file:
                json.dump(geometry, json_file, indent=1)

        return geometry

    def _geometry(self, model_name):
        if model_name in self._geom:
            return self._geom[model_name]

        raw = self._raw_geometry(model_name)

        vertex_data = create_vertex_data(model_name, raw['vertices'])
        triangles = create_triangles(raw['triangles'])

        self._geom[model_name] = geom = Geom(vertex_data)
        for triangle in triangles:
            geom.add_primitive(triangle)

        return geom

    def load_model(
        self,
        model_name,
        parent=None,
        colour=None,
        material_=None,
        scale=1,
        two_sided=False,
        transparency=TransparencyAttrib.MDual,
    ):

        node = GeomNode(model_name)
        node.add_geom(self._geometry(model_name))

        if parent is None:
            parent = self.base.render

        model = parent.attach_new_node(node)
        model.set_transparency(transparency)
        model.set_two_sided(two_sided)
        model.set_scale(scale)

        if colour is not None:
            model.set_color(colour)

        if material_ is not None:
            model.set_material(material_)

        model.set_pos(0, 0, 0)

        return model


class Model:
    _base = None
    _loader = None

    @classmethod
    def associate_base(cls, base):
        Model._base = base
        Model._loader = Loader(base)

    def __init__(self, pos):
        if self._base is None:
            raise ValueError(
                f'{type(self)} must be associated with an base '
                f'before it can be initialised'
            )

        self.pos = pos

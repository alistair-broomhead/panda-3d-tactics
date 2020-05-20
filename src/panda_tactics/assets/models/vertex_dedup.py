import json
import sys


def de_dup(json_file_name):
    with open(json_file_name) as json_file:
        geom = json.load(json_file)

    original_tris = geom["triangles"][0]
    # since lists are un-hashable, convert to tuples
    original_vertices = tuple(map(tuple, geom["vertices"]))
    # deduplicate vertices
    new_vertices = sorted(tuple(set(original_vertices)))
    # This reverse lookup can be used to find the new index for a vertex
    lookup = {vertex: index for (index, vertex) in enumerate(new_vertices)}
    # we should deduplicate triangles too now that we have standardised vertices
    new_tris = set(
        tuple(
            # this double lookup wil convert old to new
            lookup[original_vertices[vertex_index]]
            for vertex_index in tri
        )
        for tri in original_tris
    )
    new_geometry = {
        "vertices": new_vertices,
        "triangles": [sorted(new_tris)],
    }

    with open(f"{json_file_name}-reduced.json", "w") as json_file:
        json.dump(
            new_geometry, json_file, indent=1,
        )


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        de_dup(filename)

from panda3d.core import Material


def material(metallic, colour):
    material_ = Material()
    material_.set_metallic(metallic)
    material_.set_shininess(metallic)

    if metallic:
        material_.set_specular(colour)
    else:
        material_.set_emission(colour)

    return material_


class Palette:
    ambient_blue = (0.1, 0.1, 0.5, 1)
    ambient_light_blue = (0.2, 0.2, .75, 0.5)
    ambient_yellow = (0.75, 0.75, 0.2, .9)

    emission_yellow = (1, 1, 0.3, 1)

    specular_lilac = (.4, .3, 0.35, 0.5)
    specular_purple = (0.3, 0.2, 0.25, 0.2)

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
    blue = (0.1, 0.1, 0.5, 0.25)
    purple = (0.3, 0.2, 0.25, 0.5)
    light_blue = (0.2, 0.2, .75, 0.75)
    lilac = (.4, .3, 0.35, 0.5)
    yellow = (0.75, 0.75, 0.2, 0.25)

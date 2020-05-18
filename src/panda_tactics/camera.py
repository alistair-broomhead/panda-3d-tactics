import collections
import math

# noinspection PyPackageRequirements,PyPep8Naming
from direct.interval import LerpInterval as interval
import panda3d.core


class Angle:
    def __init__(self, degrees=0):
        self.degrees = degrees

    @property
    def degrees(self):
        return self._degrees

    @degrees.setter
    def degrees(self, degrees):
        self._degrees = degrees
        self.radians = radians = degrees * math.pi / 180
        self.sin = math.sin(radians)
        self.cos = math.cos(radians)


class Focus:
    _offset = None
    _hpr = None

    @staticmethod
    def _clamp(num, min_val, max_val):
        if min_val >= max_val:
            raise ValueError

        if num <= min_val:
            return min_val
        if num >= max_val:
            return max_val

        return num

    def __str__(self):
        return (f'Focus('
                f'distance={self.distance}, '
                f'longitude={self.longitude}, '
                f'latitude={self.latitude}, '
                f'skew={self.skew})')

    def __init__(self, distance=1, longitude=0, latitude=0, skew=0):
        if distance < 1:
            distance = 1

        self._distance = self._clamp(distance, 5, 30)
        self._longitude = Angle(longitude)
        self._latitude = Angle(self._clamp(latitude, -80, -10))
        self._skew = skew

    @property
    def distance(self):
        return self._distance

    @property
    def longitude(self):
        return self._longitude.degrees % 360

    @property
    def latitude(self):
        return self._latitude.degrees

    @property
    def skew(self):
        return self._skew

    @property
    def offset(self):
        if self._offset is None:
            self._offset = panda3d.core.Vec3F(
                self._distance * self._longitude.sin * self._latitude.cos,
                -self._distance * self._longitude.cos * self._latitude.cos,
                -self._distance * self._latitude.sin,
            )
        return self._offset

    @property
    def hpr(self):
        if self._hpr is None:
            self._hpr = panda3d.core.Point3(
                self._longitude.degrees,
                self._latitude.degrees,
                self._skew
            )
        return self._hpr

    def rotated(self, longitude=0, latitude=0, skew=0):
        if latitude == longitude == skew == 0:
            return self

        return Focus(
            distance=self._distance,
            longitude=self._longitude.degrees + longitude,
            latitude=self._latitude.degrees + latitude,
            skew=self._skew + skew,
        )

    def moved(self, distance=0):
        if distance == 0:
            return self

        return Focus(
            distance=self._distance - distance,
            longitude=self._longitude.degrees,
            latitude=self._latitude.degrees,
            skew=self._skew,
        )


class PlayerCamera:
    _movement = None
    _target = panda3d.core.Point3(0, 0, 0)
    _focus = Focus(distance=15, longitude=0, latitude=-50)

    def _on_move(self, point: panda3d.core.Point3):
        pass

    def __init__(self, camera, focus=_focus, target=_target, on_move=None):
        self.camera = camera

        if on_move is not None:
            self._on_move = on_move

        self._move(focus=focus, target=target)

    def retarget_relative(self, x=0, y=0, z=0):
        """
        As this is a relative camera movement, we ignore the command if we are
        part-way into another movement, in order to prevent run-away input.

        As this is a translation, I want to rotate the x-y axis with the camera,
        but only in 90 degree increments, so that movement is always a whole
        world unit.
        """
        if self._movement.stopped:
            longitude = self._focus.longitude

            # how many 90 degree rotations to apply
            for _ in range((longitude + 45) // 90):
                x, y = -y, x

            previous = self._target

            self._move(target=panda3d.core.Point3(
                x + previous.x,
                y + previous.y,
                z + previous.z,
            ))

    def retarget_to(self, target):
        if isinstance(target, collections.Iterable):
            target = panda3d.core.Point3(*target)
        elif not isinstance(target, panda3d.core.Point3):
            target = target.get_pos()

        self._move(target=target)

    def refocus_relative(self, distance=0, longitude=0, latitude=0, skew=0):
        """
        As this is a relative camera movement, we ignore the command if we are
        part-way into another movement, in order to prevent run-away input.
        """
        if self._movement.stopped:
            self._move(
                focus=self._focus.moved(distance)
                                 .rotated(longitude, latitude, skew)
            )

    def refocus_to(self, focus: Focus):
        self._move(focus=focus)

    def _move(self, focus=None, target=None):
        if focus is None:
            focus = self._focus
        else:
            self._focus = focus

        if target is None:
            target = self._target
        else:
            self._target = target
            self._on_move(target)

        self._movement = interval.LerpPosHprInterval(
            nodePath=self.camera,
            duration=0.1,
            pos=target + focus.offset,
            hpr=focus.hpr,
            blendType='easeInOut',
        )
        self._movement.start()

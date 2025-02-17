from functools import partial

from sidekick import lazy

import arcade
from fgarcade.assets import get_tile, get_sprite
from fgarcade.enums import Role
from .base import GameWindow


class HasPlatformsMixin(GameWindow):
    """
    Mixin clasis for arcade.Window's that define methods for creating platforms
    and elements on screen.
    """

    #: Configuration
    world_theme = 'green'

    #: Scale factor
    scaling = 1.0

    #: Platform list
    platforms = lazy(lambda _: arcade.SpriteList(is_static=True))

    #: Decorations
    background_decorations = lazy(lambda _: arcade.SpriteList(is_static=True))
    foreground_decorations = lazy(lambda _: arcade.SpriteList(is_static=True))

    #: Geometric properties
    @lazy
    def scene_horizontal_end(self):
        return max(max(x.right for x in self.platforms), self.width)

    @lazy
    def scene_vertical_end(self):
        return max(max(x.top for x in self.platforms), self.height) + 128

    #
    # Overrides
    #
    def draw_platforms(self):
        self.background_decorations.draw()
        self.platforms.draw()

    def draw_foreground_decorations(self):
        self.foreground_decorations.draw()

    def draw_elements(self):
        self.draw_platforms()
        super().draw_elements()

    def draw_foreground_elements(self):
        super().draw_foreground_elements()
        self.draw_foreground_decorations()

    #
    # Create elements
    #
    def create_ground(self, size, coords=(0, 0), end='default', height=1,
                      roles=(Role.BACKGROUND, Role.OBJECT), **kwargs):
        """
        Create a horizontal patch of ground.

        Args:
            size (int):
                Size of ground element in tiles.
            coords (int, int):
                Tuple with (x, y) coordinates of the first tile.
            end ({'default', 'sharp', 'round', None}):
                Style of ending tiles.
            height:
                Height in tiles. If height > 1, it generates extra solid ground
                tiles to fill the requested space.
        """

        if end == 'default':
            endl, endr = 'gl', 'gr'
        elif end == 'sharp':
            endl, endr = 'sl', 'sr'
        elif end == 'round':
            endl, endr = 'rl', 'rr'
        elif end == 'None' or end is None:
            endl = endr = 'g'
        else:
            endl, endr = end

        # Remove smooth_ends parameter from constructor
        kwargs_ = kwargs.copy()
        kwargs_.pop('smooth_ends', None)
        role_fill, role_top = roles

        new = partial(self._get_tile, role=role_fill, **kwargs_)
        if height > 1:
            x, y = coords
            for j in range(height - 1):
                for i in range(size):
                    pos = ((x + i) * 64 + 32, (y - j) * 64 - 32)
                    self.__append(new('e1', position=pos))

        return self.create_platform(
            size, coords, right=endr, left=endl, middle='g', single='gs',
            role=role_top, **kwargs)

    def create_platform(self, size, coords=(0, 0),
                        smooth_ends=True, role=Role.PLATFORM,
                        right='pr', left='pl', single='ps', middle='p', **kwargs):
        """
        Create a platform.

        The main difference between platform and horizontal ground is that a
        platform does not collide with the Player when it is reaching it from
        bellow. A ground triggers a collision with player going from any
        direction.

        Args:
            size (int):
                Size of the platform (in number of tiles)
            coords (int, int):
                Position of initial tile.
            smooth_ends (bool):
                If True, render a rounded tile in both ends.
            role:
                Role given to platform tile. Defaults to Role.PLATFORM.
            single ({'ps'}):
            left ({'pl'}):
            right ({'pr'}):
            middle ({'p'}):
                Sprite used at each position on the platform.
        """
        scale = self.scaling
        lst = []
        x, y = coords
        x = (x * 64 + 32) * scale
        y = (y * 64 + 32) * scale
        dx = 64 * scale
        add = lambda x, **kwargs: lst.append(self._get_tile(x, role=role, **kwargs))

        if size <= 0:
            raise ValueError('size must be positive')
        elif size == 1:
            add(single if smooth_ends else middle, position=(x, y))
        elif size == 2:
            add(left if smooth_ends else middle, position=(x, y))
            add(right if smooth_ends else middle, position=(x + dx, y))
        else:
            add(left if smooth_ends else middle, position=(x, y))
            for n in range(1, size - 1):
                add(middle, position=(x + n * dx, y))
            pos = (x + (size - 1) * dx, y)
            add(right if smooth_ends else middle, position=pos)

        self.__extend(lst)
        return lst

    def create_ramp(self, direction, size, coords=(0, 0), fill=True, **kwargs):
        """
        Creates a ramp that goes diagonally 'up' or 'down', according to the
        chosen direction.

        Args:
            direction ({'up', 'down'}):
                Vertical direction going from left to right.
            size (int):
                Number of elements in the diagonal.
            coords (int, int):
                Position of initial tile.
            fill:
                If True, fill with ground tiles.
        """

        if direction == 'up':
            top = 'gl'
            u = 1
            skip = 0
        elif direction == 'down':
            top = 'gr'
            u = -1
            skip = size - 1
        else:
            raise TypeError("direction must be either 'up' or 'down'")
        bottom = 'e1'
        x, y = coords
        new = partial(self._get_tile, **kwargs)

        for i in range(size):
            tile = new(top, position=(x * 64 + 32, y * 64 + 32 * u))
            self.platforms.append(tile)

            if i != skip:
                tile = new(bottom, position=(x * 64 + 32, (y - 1) * 64 + 32 * u))
                self.background_decorations.append(tile)

            if fill:
                for j in range(0, skip + u * i - 1):
                    pos = (x * 64 + 32, (y - j - 2) * 64 + u * 32)
                    tile = new('e1', role=Role.BACKGROUND, position=pos)
                    self.background_decorations.append(tile)
            x += 1
            y += u

    def create_tower(self, height, width=1, coords=(0, 0),
                     roles=(Role.OBJECT, Role.OBJECT), **kwargs):
        """
        Creates a tower of blocks that climbs vertically up by the given height.

        Args:
            height (int):
                Vertical size in number of tiles.
            width (int):
                Width of the tower element.
            coords (int, int):
                Position of the base.
        """
        x, y = coords
        kwargs.update(roles=roles, height=height)
        return self.create_ground(width, (x, y + height - 1), **kwargs)

    def create_block(self, name, coords=(0, 0), role=Role.OBJECT):
        """
        Create a new block at given coordinates.
        """
        sprite = get_sprite(f'other/block/{name}',
                            scale=self.scaling,
                            position=self.tile_to_position(*coords),
                            role=role)
        self.__append(sprite)

    def create_arrow(self, name, coords=(0, 0), role=Role.BACKGROUND):
        """
        Creates a new arrow
        """
        x, y = coords
        x += 0.5
        y += 0.4
        sprite = get_sprite(f'other/arrows/{name}',
                            scale=self.scaling,
                            position=self.tile_to_position(x, y),
                            role=role)
        self.__append(sprite)

    def create_fence(self, name='full', coords=(0, 0), role=Role.FOREGROUND):
        return self.create_object(f'other/fence/{name}', coords, role)

    def create_foreground(self, name, coords=(0, 0), at=None):
        return self.create_object(name, coords, Role.FOREGROUND, at=at)

    def create_background(self, name, coords=(0, 0), at=None):
        return self.create_object(name, coords, Role.BACKGROUND, at=at)

    def create_object(self, name, coords=(0, 0), role=Role.OBJECT, at=None):
        sprite = get_sprite(name, scale=self.scaling, role=role)
        x, y = self.tile_to_position(*coords)
        x = int(x + 32)
        y = int(y + sprite.height / 2)
        sprite.position = [x, y]
        if at is None:
            self.__append(sprite)
        else:
            at.append(sprite)
        return sprite

    #
    # Auxiliary methods
    #
    def tile_to_position(self, i, j):
        return 64 * i, 64 * j

    def _get_tile(self, kind, color=None, scale=None, **kwargs):
        if color is None:
            color = self.world_theme
        if scale is None:
            scale = self.scaling
        return get_tile(kind, color, scale=scale, **kwargs)

    def __append(self, obj, which=None):
        if which:
            which.append(obj)
        elif getattr(obj, 'role', None) == Role.BACKGROUND:
            self.background_decorations.append(obj)
        elif getattr(obj, 'role', None) == Role.FOREGROUND:
            self.foreground_decorations.append(obj)
        else:
            self.platforms.append(obj)

    def __extend(self, objs, which=None):
        for obj in objs:
            self.__append(obj, which)

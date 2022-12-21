from .constants import Align, Font, Color


class AlignAtt:
    def __init__(self, align: Align, **kwargs):
        super().__init__(**kwargs)
        self.align = align

    @property
    def align(self) -> Align:
        return self._align

    @align.setter
    def align(self, align: Align):
        try:
            align = Align(align)
        except ValueError:
            pass

        if align is not None and align not in Align:
            raise ValueError('Unknown alignment')
        self._align = align


class WidthAtt:
    def __init__(self, width: int, min_width: int, max_width: int, **kwargs):
        super().__init__(**kwargs)
        self._min_width = min_width
        self._max_width = max_width
        self.width = width

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        try:
            width = int(width)
        except TypeError:
            pass

        if width is not None and (width < self._min_width or width > self._max_width):
            raise ValueError(
                f'"width" must be bewteen {self._min_width} and {self._max_width} inclusive')
        self._width = width


class HeightAtt:
    def __init__(self, height: int, min_height: int, max_height: int, **kwargs):
        super().__init__(**kwargs)
        self._min_height = min_height
        self._max_height = max_height
        self.height = height

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int):
        try:
            height = int(height)
        except TypeError:
            pass

        if height is not None and (height < self._min_height or height > self._max_height):
            raise ValueError(
                f'"height" must be bewteen {self._min_height} and {self._max_height} inclusive')
        self._height = height


class FontAtt:
    def __init__(self, font: Font, **kwargs):
        super().__init__(**kwargs)
        self.font = font

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, font: Font):
        try:
            font = Font(font)
        except ValueError:
            pass

        if font is not None and font not in Font:
            raise ValueError(
                f'"font" must be valid.')
        self._font = font


class LineSpcAtt:
    def __init__(self, linespc, min_linespc=0, max_linespc=255, **kwargs):
        super().__init__(**kwargs)
        self._min_linespc = min_linespc
        self._max_linespc = max_linespc
        self.linespc = linespc

    @property
    def linespc(self) -> int:
        return self._linespc

    @linespc.setter
    def linespc(self, linespc: int):
        try:
            linespc = int(linespc)
        except TypeError:
            pass

        if linespc is not None and (self._min_linespc > linespc or linespc > self._max_linespc):
            raise ValueError(
                f'"linespc" must be between {self._min_linespc} and {self._max_linespc} inclusive'
            ) from None
        self._linespc = linespc


class RotateAtt:
    def __init__(self, rotate, **kwargs):
        super().__init__(**kwargs)
        self._rotate = rotate

    @property
    def rotate(self) -> bool:
        return self._rotate

    @rotate.setter
    def rotate(self, rotate: bool):
        try:
            rotate = bool(rotate)
        except TypeError:
            pass

        self._rotate = rotate


class ColorAtt:
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        self.color = color

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Color):
        try:
            color = Color(color)
        except TypeError:
            pass

        if color not in Color:
            raise ValueError('Unknonw color')
        self._color = color





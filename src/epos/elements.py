import xml.etree.ElementTree as ET

from . import status
from .attributes import AlignAtt, ColorAtt, WidthAtt, HeightAtt, FontAtt, RotateAtt, LineSpcAtt
from .constants import Color, Align, Mode, BarcodeType, HRI, Font, CutType, Lang


class BaseElement:
    """
    Base class for all ePOS-Print XML elements
    """
    tag: str
    text: str

    def __init__(self, tag, text='', **kwargs):
        super().__init__(**kwargs)
        self.tag = tag
        self.attr = {}
        self.text = text
        self.tail = ''

        self.namespaces = {
            's': 'http://schemas.xmlsoap.org/soap/envelope/',
            'epos-print': 'http://www.epson-pos.com/schemas/2011/03/epos-print',
        }

    def to_xml(self):
        """
        Converts the object to XML
        """
        self.attr = {}
        self._load_attrs()
        attr = {k: str(v).lower() for k, v in self.attr.items() if v is not None}
        element = ET.Element(self.tag, attr)
        element.text = self.text
        element.tail = self.tail
        return element

    def to_str(self):
        return ET.tostring(self.to_xml(), encoding='utf-8', )

    def from_xml(self, xml: str):
        """
        Loads xml data
        """
        dom = ET.fromstring(xml)

    def _add_ns(self, tag: str) -> str:
        r = f'{{{self.namespaces["a"]}}}{tag}'
        # print(r)
        return r

    def _load_attrs(self):
        """To be overwritten by element class"""
        raise NotImplementedError


class Response(BaseElement):
    """
    This is an XML document that is sent back from a printer to an application.
    Reference:
    https://reference.epson-biz.com/modules/ref_epos_print_xml_en/index.php?vid=ref_epos_print_xml_en_xmlforcontrollingprinter_response
    """
    def __init__(self, success=True):
        super().__init__('response')

        self.success = success
        self.code = ''
        self.status = 0
        self.battery = 0

    def _load_attrs(self):
        self.attr['xmlns'] = self.namespaces['epos-print']
        self.attr['success'] = str(self.success).lower()
        if self.code:
            self.attr['code'] = self.code
        self.attr['status'] = str(self.status)
        self.attr['battery'] = str(self.battery)

    def get_status(self) -> list[str]:
        return status.parse_code(self.status)


class Text(BaseElement, FontAtt, WidthAtt, HeightAtt, AlignAtt, LineSpcAtt, RotateAtt, ColorAtt):
    def __init__(
            self,
            text: str = '',
            lang: Lang = None,
            font: Font = None,
            smooth: bool = None,
            double_width: bool = None,
            double_height: bool = None,
            width: int = None,
            height: int = None,
            reverse: bool = None,
            underline: bool = None,
            bold: bool = None,
            color: Color = None,
            x: int = None,
            y: int = None,
            align: Align = None,
            rotate: bool = None,
            linespc: int = None
    ):
        super().__init__(
            tag='text',
            text=text,
            font=font,
            width=width, min_width=1, max_width=8,
            height=height, min_height=1, max_height=8,
            align=align,
            linespc=linespc,
            rotate=rotate,
            color=color
        )

        self.lang = lang
        self.smooth = smooth
        self.double_width = double_width
        self.double_height = double_height
        self.reverse = reverse
        self.underline = underline
        self.bold = bold
        self.x = x
        self.y = y

    def _load_attrs(self):
        self.attr['lang'] = self.lang.value if self.lang else None
        self.attr['font'] = self.font.value if self.font else None
        self.attr['dw'] = self.double_width
        self.attr['dh'] = self.double_height
        self.attr['width'] = self.width
        self.attr['height'] = self.height
        self.attr['reverse'] = self.reverse
        self.attr['em'] = self.bold
        self.attr['color'] = self.color.value if self.color else None
        self.attr['x'] = self.x
        self.attr['y'] = self.y
        self.attr['align'] = self.align.value if self.align else None
        self.attr['rotate'] = self.rotate
        self.attr['linespc'] = self.linespc
        self.attr['smooth'] = self.smooth
        self.attr['ul'] = self.underline

    @property
    def lang(self) -> Lang:
        return self._lang

    @lang.setter
    def lang(self, lang: Lang):
        try:
            lang = Lang(lang)
        except ValueError:
            pass

        if lang is not None and lang not in Lang:
            raise ValueError('"lang" is invalid') from None
        self._lang = lang

    @property
    def smooth(self) -> bool:
        return self._smooth

    @smooth.setter
    def smooth(self, smooth: bool):
        if smooth == 'true':
            self._smooth = True
        elif smooth == 'false':
            self._smooth = False
        else:
            self._smooth = smooth
    
    @property
    def double_width(self) -> bool:
        return self._double_width

    @double_width.setter
    def double_width(self, double_width: bool):
        if double_width == 'true':
            self._double_width = True
        elif double_width == 'false':
            self._double_width = False
        else:
            self._double_width = double_width

    @property
    def dw(self):
        return self.double_width

    @dw.setter
    def dw(self, dw):
        self.double_width = dw
    
    @property
    def double_height(self) -> bool:
        return self._double_height

    @double_height.setter
    def double_height(self, double_height: bool):
        if double_height == 'true':
            self._double_height = True
        elif double_height == 'false':
            self._double_height = False
        else:
            self._double_height = double_height

    @property
    def dh(self):
        return self.double_height

    @dh.setter
    def dh(self, dh):
        self.double_height = dh
    
    @property
    def reverse(self) -> bool:
        return self._reverse

    @reverse.setter
    def reverse(self, reverse: bool):
        if reverse == 'true':
            self._reverse = True
        elif reverse == 'false':
            self._reverse = False
        else:
            self._reverse = reverse

    @property
    def underline(self) -> bool:
        return self._underline

    @underline.setter
    def underline(self, underline: bool):
        if underline == 'true':
            self._underline = True
        elif underline == 'false':
            self._underline = False
        else:
            self._underline = underline
    
    @property
    def ul(self):
        return self.underline
    
    @ul.setter
    def ul(self, ul):
        self.underline = ul
    
    @property
    def bold(self) -> bool:
        return self._bold

    @bold.setter
    def bold(self, bold: bool|str):
        if bold == 'true':
            self._bold = True
        elif bold == 'false':
            self._bold = False
        else:
            self._bold = bold

    @property
    def em(self):
        return self.bold

    @em.setter
    def em(self, em):
        self.bold = em
    
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        try:
            x = int(x)
        except TypeError:
            pass
        
        if x is not None and (x < 0 or x > 576):
            raise ValueError('"x" must be between 0 and 576 inclusive') from None
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        try:
            y = int(y)
        except TypeError:
            pass

        if y is not None and (y < 0 or y > 65535):
            raise ValueError('"y" must be between 0 and 576 inclusive') from None
        self._y = y


class Feed(BaseElement, LineSpcAtt):
    def __init__(
            self,
            unit: int = None,
            line: int = None,
            linespc: int = None
    ):
        super().__init__(
            tag='feed',
            linespc=linespc
        )
        self.unit = unit
        self.line = line

    def _load_attrs(self):
        self.attr['unit'] = self.unit
        self.attr['line'] = self.line
        self.attr['linespc'] = self.linespc

    @property
    def unit(self) -> int:
        return self._unit

    @unit.setter
    def unit(self, unit: int):
        try:
            unit = int(unit)
        except TypeError:
            pass

        if unit is not None and (0 > unit or unit > 255):
            raise ValueError('"unit" must be between 0 and 255 inclusive') from None
        self._unit = unit

    @property
    def line(self) -> int:
        return self._line

    @line.setter
    def line(self, line: int):
        try:
            line = int(line)
        except TypeError:
            pass

        if line is not None and (line < 0 or line > 255):
            raise ValueError('"line" must be between 0 and 255 inclusive') from None
        self._line = line


class Image(BaseElement, AlignAtt, ColorAtt, WidthAtt, HeightAtt):
    def __init__(
            self,
            width: int = 0, height: int = 0,
            text: str = '',
            color: Color = None,
            align: Align = None,
            mode: Mode = Mode.MONO
    ):
        super().__init__(
            tag='image',
            text=text,
            align=align,
            width=width, min_width=0, max_width=576,
            height=height, min_height=0, max_height=655635,
            color=color
        )
        self.mode = mode

    def _load_attrs(self):
        self.attr['width'] = self.width
        self.attr['height'] = self.height
        self.attr['color'] = self.color.value
        self.attr['align'] = self.align.value if self.align else None
        if self.mode != Mode.MONO:
            self.attr['mode'] = self.mode.value

    @property
    def mode(self) -> Mode:
        return self._mode

    @mode.setter
    def mode(self, mode: Mode):
        try:
            mode = Mode(mode)
        except TypeError:
            pass

        if mode not in Mode:
            raise ValueError('Unknown mode')
        self._mode = mode


class Logo(BaseElement, AlignAtt):
    def __init__(
            self,
            key1: int = 0,
            key2: int = 0,
            align: Align = None
    ):
        super().__init__(tag='logo', align=align)
        self.key1 = key1
        self.key2 = key2

    def _load_attrs(self):
        self.attr['key1'] = str(self.key1)
        self.attr['key2'] = str(self.key2)
        self.attr['align'] = self.align
    
    @property
    def key1(self) -> int:
        return self._key1
    
    @key1.setter
    def key1(self, key1: int):
        try:
            key1 = int(key1)
        except TypeError:
            pass

        if key1 < 0 or key1 > 255:
            raise ValueError('"key1" must be bewteen 0 and 255 inclusive') from None
        self._key1 = key1

    @property
    def key2(self) -> int:
        return self._key2

    @key2.setter
    def key2(self, key2: int):
        try:
            key2 = int(key2)
        except TypeError:
            pass

        if key2 < 0 or key2 > 255:
            raise ValueError('"key2" must be bewteen 0 and 255 inclusive') from None
        self._key2 = key2


class Barcode(BaseElement, AlignAtt, WidthAtt, HeightAtt, FontAtt, RotateAtt):
    def __init__(
            self,
            type: BarcodeType = BarcodeType,
            text='',
            hri: HRI = None,
            font: Font = None,
            width: int = None,
            height: int = None,
            align: Align = None,
            rotate: bool = None
    ):
        super().__init__(
            tag='barcode',
            text=text,
            font=font,
            width=width, min_width=2, max_width=6,
            height=height, min_height=0, max_height=255,
            align=align,
            rotate=rotate
        )
        self.type = type
        self.hri = hri

    def _load_attrs(self):
        self.attr['type'] = self.type.value
        self.attr['hri'] = self.hri.value
        self.attr['font'] = self.font.value
        self.attr['width'] = self.width
        self.attr['height'] = self.height
        self.attr['align'] = self.align.value
        self.attr['rotate'] = self.rotate

    @property
    def type(self) -> BarcodeType:
        return self._type

    @type.setter
    def type(self, type: BarcodeType):
        try:
            type = BarcodeType(type)
        except TypeError:
            pass

        if type not in BarcodeType:
            raise ValueError('The barcodetype is invalid') from None
        self._type = type

    @property
    def hri(self) -> HRI:
        return self._hri

    @hri.setter
    def hri(self, hri: HRI):
        try:
            hri = HRI(hri)
        except TypeError:
            pass

        if hri not in HRI:
            raise ValueError('The HRI is invalid') from None
        self._hri = hri


class Symbol(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class HLine(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class VLineBegin(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class VLineEnd(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Page(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Area(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Direction(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Position(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Line(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Rectangle(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Cut(BaseElement):
    def __init__(self, type: CutType = None):
        super().__init__('cut')
        self.type = type

    def _load_attrs(self):
        self.attr['type'] = self.type
        
    @property
    def type(self) -> CutType:
        return self._type

    @type.setter
    def type(self, type: CutType):
        try:
            type = CutType(type)
        except ValueError:
            pass

        if type is not None and type not in CutType:
            raise ValueError('Unknown type')
        self._type = type


class Pulse(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Sound(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Command(BaseElement):  # TODO implement
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Layout(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class Recovery(BaseElement):
    def __init__(self):
        super().__init__('recovery')

    def _load_attrs(self):
        pass


class Reset(BaseElement):
    def __init__(self):
        super().__init__('reset')

    def _load_attrs(self):
        pass


class BatchBegin(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class BatchEnd(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class RotateBegin(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()


class RotateEnd(BaseElement):
    def __init__(self):
        super().__init__('')
        raise NotImplementedError()

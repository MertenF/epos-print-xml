from enum import Enum


class Color(Enum):
    COLOR_1 = 'color_1'
    DEFAULT = None


class Align(Enum):
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class Mode(Enum):
    MONO = 'mono'


class Font(Enum):
    A = 'font_a'
    B = 'font_b'


class BarcodeType(Enum):
    UPC_A = 'upc_a'
    UPC_E = 'upc_e'
    EAN13 = 'ean13'
    JAN13 = 'jan13'
    EAN8 = 'ean8'
    JAN8 = 'jan8'
    CODE39 = 'code39'
    ITF = 'itf'
    CODABAR = 'codabar'
    CODE93 = 'code93'
    CODE128 = 'code128'
    GS1_128 = 'gs1_128'
    GS1_DATABAR_OMNIDIRECTIONAL = 'gs1_databar_omnidirectiona'
    GS1_DATABAR_TRUNCATED = 'gs1_databar_truncated'
    GS1_DATABAR_LIMITED = 'gs1_databar_limited'
    GS1_DATABAR_EXPANDED = 'gs1_databar_expanded'


class HRI(Enum):
    NONE = 'None'
    ABOVE = 'above'
    BELOW = 'below'
    BOTH = 'both'


class CutType(Enum):
    NO_FEED = 'no_feed'
    FEED = 'feed'


class Lang(Enum):
    EN = 'en'
    DE = 'de'
    FR = 'fr'
    IT = 'it'
    ES = 'es'

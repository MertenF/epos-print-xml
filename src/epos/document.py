from dataclasses import dataclass, field
from typing import Type, Generic, TypeVar
import xml.etree.ElementTree as ET

from .elements import BaseElement

B = TypeVar('B', bound='BaseElement')


@dataclass
class EposDocument:
    parameters: list = field(default_factory=list)
    body: list[Type[BaseElement]] = field(default_factory=list)

    def add_parameter(self, element: Generic[B]) -> None:
        self.parameters.append(element)

    def add_body(self, element: Generic[B]) -> None:
        self.body.append(element)

    def parameters_to_xml(self) -> ET.Element:
        return _to_xml('parameter', self.parameters)

    def body_to_xml(self) -> ET.Element:
        return _to_xml('epos-print', self.body)

    def parameters_to_str(self) -> str:
        return ET.tostring(self.parameters_to_xml(), encoding='unicode', short_empty_elements=False)

    def body_to_str(self, url_encode_newlines=False) -> str:
        s = ET.tostring(self.body_to_xml(), encoding='unicode')
        s = s.replace(' />', '/>')
        if url_encode_newlines:
            s = s.replace('\n', '&#10;')
        return s


def _to_xml(base_tag: str, element_list: list[Type[B], ...]) -> ET.Element:
    root = ET.Element(
        base_tag,
        xmlns='http://www.epson-pos.com/schemas/2011/03/epos-print',
    )
    for element in element_list:
        root.append(element.to_xml())
    return root

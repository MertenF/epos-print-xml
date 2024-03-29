import xml.etree.ElementTree as ET

import requests

from .document import EposDocument
from .elements import Cut, Response

namespaces = {
    's': 'http://schemas.xmlsoap.org/soap/envelope/',
    'epos-print': 'http://www.epson-pos.com/schemas/2011/03/epos-print',
}


class Printer:
    def __init__(
            self,
            ip: str,
            request_timeout: int = 3,
            use_https: bool = False,
            devid: str = 'local_printer',
            job_timeout: int = 5000,
            url: str = '/cgi-bin/epos/service.cgi',
    ):
        self.ip = ip
        self.request_timeout = request_timeout
        self.use_https = use_https
        self.devid = devid
        self.job_timeout = job_timeout
        self.url = url

    def printer_ready(self) -> bool:
        """
        Send empty page to check the status

        Returns true if online, false if offline.

        :return Boolean
        """
        response = self.print_empty()
        return response.success

    def print_empty(self) -> Response:
        """
        Send an empty document to the printer.
        Used to gather status information

        :return: Response
        """
        doc = EposDocument()
        response = self.print(doc, autocut=False)
        return response

    def print(self, doc: EposDocument, autocut: bool = True) -> Response:
        if autocut:
            doc.add_body(Cut())
        r = self._send_printjob(doc.body_to_str())

        response = Response(success=False)
        try:
            xml_dom = ET.fromstring(r)
        except ET.ParseError:
            response.code = 'PARSING_ERROR'
            return response

        body = xml_dom.find('./s:Body', namespaces)
        if not body:
            response.code = 'NO_BODY_FOUND'
            return response

        for element in body:
            if 'response' in element.tag:
                attr = element.attrib
                break
        else:
            response.code = 'NO_RESPONSE_FOUND'
            return response

        response.success = attr['success'] == 'true'
        response.code = attr['code']
        response.status = int(attr['status'])
        response.battery = int(attr['battery'])

        return response

    def _send_printjob(self, data: str) -> str:
        prefix = 'https://' if self.use_https else 'http://'
        url = prefix + self.ip + self.url
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
            'SOAPAction': '""',
        }
        params = {'devid': self.devid, 'timeout': self.job_timeout}

        response = requests.post(
            url,
            data=_add_soap_enveloppe(data),
            headers=headers,
            params=params,
            timeout=self.request_timeout,
        )

        return response.text


def _add_soap_enveloppe(body: str, header: str = '') -> str:
    """Add the soap enveloppe, header and body"""
    soap = [f'<s:Envelope xmlns:s="{namespaces["s"]}">']

    if header:
        soap.append('<s:Header>')
        soap.append(header)
        soap.append('/<s:Header>')
    soap.append('<s:Body>')
    soap.append(body)
    soap.append('</s:Body>')
    soap.append('</s:Envelope>')

    return ''.join(soap)

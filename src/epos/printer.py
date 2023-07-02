import xml.etree.ElementTree as ET

import requests

from .document import EposDocument
from .elements import Cut, Response


namespaces = {
    's': 'http://schemas.xmlsoap.org/soap/envelope/',
    'epos-print': 'http://www.epson-pos.com/schemas/2011/03/epos-print',
}

class Printer:
    def __init__(self, ip):
        self.ip = ip

        # Defaults, normally not changed
        self.use_https = False
        self.devid = 'local_printer'
        self.timeout = 5000
        self.url = '/cgi-bin/epos/service.cgi'

    def try_connection(self):
        """Send empty page to check the status"""
        doc = EposDocument()
        resp = self.print(doc, autocut=False)
        return resp.success

    def print(self, doc: EposDocument, autocut=True) -> Response:
        if autocut:
            doc.add_body(Cut())
        r = self._send_printjob(doc.body_to_str())

        response = Response(success=False)

        xml_dom = ET.fromstring(r)
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

    def _send_printjob(self, data):
        prefix = 'https://' if self.use_https else 'http://'
        url = prefix + self.ip + self.url
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
            'SOAPAction': '""',
        }
        params = {'devid': self.devid, 'timeout': self.timeout}

        response = requests.post(
            url,
            data=_add_soap_enveloppe(data),
            headers=headers,
            params=params,
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

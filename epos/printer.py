import requests

from .constants import BarcodeType
from .document import EposDocument
from .elements import Text, Feed, Cut, Barcode


class Printer:
    def __init__(self, ip):
        self.ip = ip

        # Defaults, normally not changed
        self.use_https = False
        self.devid = 'local_printer'
        self.timeout = 5000
        self.url = '/cgi-bin/epos/service.cgi'

    def try_connection(self):
        """Send empty page and check the status"""
        doc = EposDocument()
        resp = self._send_printjob(doc.body_to_str())
        return 'success="true' in resp

    def print(self, doc: EposDocument, autocut=True):
        if autocut:
            doc.add_body(Cut())
        resp = self._send_printjob(doc.body_to_str())
        return resp

    def _send_printjob(self, data):
        prefix = 'https://' if self.use_https else 'http://'
        url = prefix + self.ip + self.url
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
            'SOAPAction': '""',
        }
        params = {'devid': self.devid, 'timeout': self.timeout}

        print(data)

        response = requests.post(
            url,
            data=_add_soap_enveloppe(data),
            headers=headers,
            params=params,
        )

        return response.text


def _add_soap_enveloppe(body: str, header: str = '') -> str:
    """Add the soap enveloppe, header and body"""
    soap = []

    soap.append('<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">')
    if header:
        soap.append('<s:Header>')
        soap.append(header)
        soap.append('/<s:Header>')
    soap.append('<s:Body>')
    soap.append(body)
    soap.append('</s:Body>')
    soap.append('</s:Envelope>')

    return ''.join(soap)


def main():
    printer = Printer('10.0.0.12')
    print(printer.try_connection())

    doc = EposDocument()
    doc.add_body(Text(
        'Dit is een test voor ene lange lijn text ************** ZEEEERRRR LANGE LIJN TEXT hmmm zonder een enter in\n'))
    t = Text('Inverteren?')
    t.reverse = True
    doc.add_body(t)
    doc.add_body(Feed(2))
    doc.add_body(Barcode(BarcodeType.CODE39, 'BARCODE'))

    doc.add_body(Cut())
    printer.print(doc)


if __name__ == '__main__':
    main()

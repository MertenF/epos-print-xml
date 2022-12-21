# py-epos-print-xml
Python library to communicate with Epson thermal printers via ePos-Print XML.
This makes it easy and intuitive to create print orders for ePos-Print XML compatible printers, like the Epson TM-T20, TM-m30 and TM-m50 series.
Depending on the printer model, some elements are not supported. Check you manual or the [Epson reference](https://reference.epson-biz.com/modules/ref_epos_print_xml_en/index.php?vid=ref_epos_print_xml_en_devicespecifications_supportedelementslist) to see which elements are supported.

This is still in active development, don't expect everything to work.

## Example

```python
from epos.printer import Printer
from epos.document import EposDocument
from epos.elements import Text, Feed, Barcode
from epos.constants import Align

# Create a new printer object with 10.0.0.12 as ip
printer = Printer('10.0.0.12')
# Check if we can connect to the printer with no errors, otherwise exit
if not printer.try_connection():
    exit()

# Create a new EposDocument object
# This will contain all the individual elements
doc = EposDocument()

# Add an element directly to the body of the document
doc.add_body(Text('This is example text!\n'))
doc.add_body(Feed()) # Another way to add a newline

# It's also possible to first create the text object and then change the properties
t = Text('Some special text :O\n')
t.bold = True
t.align = Align.CENTER
doc.add_body(t)

# Add 2 empty lines
doc.add_body(Feed(2))

# Add a barcode
doc.add_body(Barcode(BarcodeType.CODE39, 'text in barcode'))

# Send the whole document to the printer
# This will automatially send a Cut at the end of the document body
printer.print(doc) 
```


## Documentation
Tech reference of all the xml elements by Epson: https://reference.epson-biz.com/modules/ref_epos_print_xml_en/index.php?content_id=1

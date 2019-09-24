# Created by yuwenhao at 16/02/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer


def parse_obj(lt_objs):

    list_of_lt_objs = list(lt_objs)

    if not list_of_lt_objs: return []

    obj = list_of_lt_objs[0]
    if isinstance(obj,
                  (pdfminer.layout.LTTextBox, pdfminer.layout.LTTextBoxVertical, pdfminer.layout.LTTextBoxHorizontal)):
        return [obj.get_text()] + parse_obj(list_of_lt_objs[1:])
    elif isinstance(obj, pdfminer.layout.LTFigure):
        return parse_obj(obj) + parse_obj(list_of_lt_objs[1:])
    else:
        return []


def get_texts_from_pdf(file):
    fp = open(file, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # loop over all pages in the document

    all_text_tokens = []

    for i, page in enumerate(PDFPage.create_pages(document)):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        all_text_tokens += parse_obj(layout._objs)
    return all_text_tokens


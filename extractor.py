import ctypes
import logging
from typing import Set, List
import os

import PyPDF2.pdf
import pypdfium2 as pdfium

from errors import URLError
from util import URLUtil


class Extractor:
  """
  The ``Extractor`` class is used to perform URL extraction from PDF documents.
  It uses `PyPDF2 <https://pypi.org/project/PyPDF2/>`_ and `PyPDFium2 <https://pypi.org/project/pypdfium2/>`_ for this.
  Here, PyPDF2 is used to extract URLs from PDF annotations, while PyPDFium2 is used to extract URLs from PDF text.

  When extracting URLs, priority is given to URLs from PDF annotations, as they were found less error-prone than URLs from PDF text.
  This is because URLs in PDF text may be extracted partially (e.g., truncated due to a newline character) or with
  additional characters (e.g., with unwanted letters from the sentence following a URL).

  """

  def __init__(self):
    self.util = URLUtil()

  def extract_annot_urls(self, fp: str) -> Set[str]:
    """
    Extract Annotated URLs from PDF (Using PyPDF2)

    :param fp: Path to PDF
    :return: Set of Annotated URLs in PDF

    """
    urls = set()
    with open(fp, "rb") as file:
      try:
        pdf = PyPDF2.pdf.PdfFileReader(file, strict=False)
        for page in pdf.pages:
          page: PyPDF2.pdf.PageObject = page.getObject()
          if "/Annots" in page:
            for annot in page["/Annots"]:
              try:
                annot = annot.getObject()
              except PyPDF2.utils.PdfReadError as e:
                annot = ''
                logging.debug(e)
              if "/A" in annot:
                ann = annot["/A"].getObject()
              elif "/S" in annot:
                ann = annot["/S"].getObject()
              else:
                continue
              if "/URI" in ann:
                try:
                  urls.add(self.util.canonicalize_url(ann["/URI"]))
                except URLError as e:
                  logging.debug(e)
      except Exception as e: 
        logging.debug(e)
    return urls

  def extract_text_urls(self, fp: str) -> Set[str]:
    """
    Extract Text URLs from PDF (Using PDFium)

    :param fp: Path to PDF
    :return: Set of Text URLs in PDF

    """
    urls = set()
    buf_len = 2048
    buffer = (ctypes.c_ushort * buf_len)()
    buffer_ = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ushort))
    
    doc = pdfium.FPDF_LoadDocument(fp, None)
    page_count = pdfium.FPDF_GetPageCount(doc)
    for i in range(page_count):
      # load PDF page
      page = pdfium.FPDF_LoadPage(doc, i)
      # load text in PDF page
      text = pdfium.FPDFText_LoadPage(page)
      # Load links in PDF text
      links = pdfium.FPDFLink_LoadWebLinks(text)
      link_count = pdfium.FPDFLink_CountWebLinks(links)
      # get each URL
      for j in range(link_count):
        url_length = pdfium.FPDFLink_GetURL(links, j, buffer_, buf_len)
        url_nums = buffer[:url_length - 1]
        url = "".join(map(chr, url_nums)).strip()
        try:
          urls.add(self.util.canonicalize_url(url))
        except URLError as e:
          logging.debug(e)
      pdfium.FPDFLink_CloseWebLinks(links)
      pdfium.FPDFText_ClosePage(text)
      pdfium.FPDF_ClosePage(page)
    pdfium.FPDF_CloseDocument(doc)
    return urls

  def extract_all_urls(self, fp: str) -> List[str]:
    """
    Extract All URLs from PDF (Using PyPDF2 and PDFium)

    :param fp: Path to PDF
    :return: Set of All URLs in PDF

    """
    # extract annotated URLs (baseline, always valid)
    annot_urls = set(self.extract_annot_urls(fp))
    # extract full text URLs (error-prone)
    full_text_urls = set(self.extract_text_urls(fp))
    # pick unique URLs from full_text_urls
    full_text_urls = self.util.pick_uniq_urls(full_text_urls)
    # pick URLs from full_text_urls do not match (exact/partial) any URL in annot_urls
    full_text_urls = self.util.pick_new_urls(full_text_urls, annot_urls)
    # concatenate, sort, and return
    all_urls = sorted(annot_urls.union(full_text_urls))
    urls = {"url_count":len(all_urls), "annot_urls":list(annot_urls), "text_urls":list(full_text_urls), "all_urls":all_urls}
    return urls

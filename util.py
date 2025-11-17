import streamlit as st
import datetime
import holidays
import tempfile
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from docx import Document as DocxDocument
from reportlab.pdfbase.pdfmetrics import stringWidth
import unicodedata

def sanitize_text(text: str) -> str:
    """
    Normalize and replace characters that commonly cause missing-glyph boxes in PDFs
    when using standard PostScript fonts (Helvetica). Replace en-dash, em-dash, curly
    quotes, ellipsis, etc. with plain ASCII equivalents.

    Additionally, remove control characters and 'other symbol' characters (commonly
    emoji) which standard PostScript fonts do not contain. If you want to preserve
    emoji/unicode symbols, register and use a Unicode TTF (e.g., DejaVuSans) instead.

    IMPORTANT: preserve common whitespace control characters (\n, \r, \t) so paragraph
    breaks are not lost when calling text.split('\\n') later in the code.
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return ""

    # Normalize to NFC
    text = unicodedata.normalize("NFC", text)

    # Mapping of problematic punctuation to ASCII equivalents
    replacements = {
        "\u2013": "-",  # en dash
        "\u2014": "-",  # em dash
        "\u2018": "'",  # left single quote
        "\u2019": "'",  # right single quote
        "\u201C": '"',  # left double quote
        "\u201D": '"',  # right double quote
        "\u2026": "...",  # ellipsis
        "\u2010": "-",  # hyphen
        "\u2212": "-",  # minus sign
        "\u00A0": " ",  # non-breaking space
    }

    # Translate the replacements
    for k, v in replacements.items():
        if k in text:
            text = text.replace(k, v)

    # Remove control characters and 'Other Symbol' (So) characters (emoji, etc.)
    filtered_chars = []
    # allow these whitespace/control characters so paragraph breaks remain
    allowed_controls = {"\n", "\r", "\t"}
    for ch in text:
        cat = unicodedata.category(ch)
        # Skip control characters (Cc) and other/formatting (Cf), and symbols of type 'So',
        # but preserve common whitespace controls listed above.
        if (cat.startswith("C") or cat == "So") and ch not in allowed_controls:
            continue
        filtered_chars.append(ch)

    text = "".join(filtered_chars)

    return text

def wrap_text_to_width(text, font_name, font_size, max_width):
    """
    Wrap a string so each line fits within max_width points.
    """
    text = sanitize_text(text)
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def draw_wrapped_section(c, title, text, x, y, width, height, line_height):
    title_font = "Helvetica-Bold"
    title_size = 12
    body_font = "Helvetica"
    body_size =

import pymupdf as fitz

from app.services.pdf_service import extract_text_from_pdf


def create_test_pdf():
    pdf = fitz.open()

    page = pdf.new_page()
    page.insert_text(
        (50, 50),
        "Alan Paul John\nPython React FastAPI"
    )

    pdf_bytes = pdf.tobytes()
    pdf.close()

    return pdf_bytes


def test_extract_text_from_pdf():
    pdf_bytes = create_test_pdf()

    text = extract_text_from_pdf(pdf_bytes)

    assert isinstance(text, str)
    assert "Alan Paul John" in text
    assert "Python" in text
    assert "React" in text

def test_extract_text_from_invalid_pdf():
    invalid_pdf = b"This is not a real PDF"

    try:
        extract_text_from_pdf(invalid_pdf)
        assert False, "Expected ValueError was not raised"

    except ValueError as exc:
        assert "Unable to process PDF" in str(exc)

def test_extract_text_from_multi_page_pdf():
    pdf = fitz.open()

    page1 = pdf.new_page()
    page1.insert_text(
        (50, 50),
        "Page One - Python React"
    )

    page2 = pdf.new_page()
    page2.insert_text(
        (50, 50),
        "Page Two - FastAPI PostgreSQL"
    )

    pdf_bytes = pdf.tobytes()
    pdf.close()

    text = extract_text_from_pdf(pdf_bytes)

    assert "Page One" in text
    assert "Page Two" in text
    assert "Python" in text
    assert "PostgreSQL" in text
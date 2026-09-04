import fitz


def extract_text_from_pdf(contents: bytes) -> str:
    """
    Extract text from PDF bytes.

    Raises:
        ValueError: If the PDF cannot be processed.
    """

    pdf_document = None

    try:
        # Open PDF from the bytes received from UploadFile
        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        text_parts = []

        # Extract text from every page
        for page in pdf_document:
            page_text = page.get_text()

            if page_text:
                text_parts.append(page_text)

        # Combine text from all pages
        return "\n".join(text_parts)

    except Exception as exc:
        raise ValueError(
            "Unable to process PDF"
        ) from exc

    finally:
        # Always close the PDF document
        if pdf_document is not None:
            pdf_document.close()
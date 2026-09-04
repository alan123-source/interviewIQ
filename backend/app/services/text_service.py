import re


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize extracted resume text.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove leading/trailing whitespace from each line
    lines = [
        line.strip()
        for line in text.split("\n")
    ]

    # Rebuild text
    text = "\n".join(lines)

    # Normalize multiple spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse 3 or more consecutive newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "uploads" / "resumes"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_resume_file(
    file_contents: bytes,
    original_filename: str | None,
) -> str:
    """
    Save a resume PDF to local storage.

    Returns the relative file path.
    """

    unique_filename = f"{uuid4()}.pdf"

    file_path = UPLOAD_DIR / unique_filename

    file_path.write_bytes(file_contents)

    relative_path = Path("uploads") / "resumes" / unique_filename

    return str(relative_path)

def delete_resume_file(file_path:str) ->None:
    full_path=BASE_DIR / file_path

    if full_path.exists():
        full_path.unlink()

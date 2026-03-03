import pydoc
import shutil

from pypdf import PdfReader


def read(path: str):
    reader = PdfReader(path)
    width, _ = shutil.get_terminal_size()

    data = ""
    for i, page in enumerate(reader.pages):
        data += "-" * (width) + "\n"
        data += centerize(f"||Page {i + 1}||")
        data += page.extract_text() + "\n"
        data += "-" * (width) + "\n"
    pydoc.pager(data)


def centerize(txt: str) -> str:
    width, _ = shutil.get_terminal_size()
    space = " " * ((width - len(txt)) // 2)
    return space + txt + space + "\n"

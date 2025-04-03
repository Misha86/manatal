import os
import re

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")


def secure_filename(filename: str) -> str:
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")

    normalized_filename = _filename_ascii_strip_re.sub("", "_".join(filename.split()))
    filename = str(normalized_filename).strip("._")
    return filename

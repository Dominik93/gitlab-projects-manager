import datetime
import time


def _prepare_header(content):
    header = []
    for key in content[0]:
        header.append(key)
    return header


def _prepare_row(headers_row, item):
    row = []
    for key in item:
        if key in headers_row:
            row.append(str(item[key]))
    return row


def write(file: str, content: list[dict], separator: str = ";", headers: list[str] = None):
    headers_row = headers if headers is not None else _prepare_header(content)
    with open(file.replace("{timestamp}", datetime.datetime.now().strftime("%H-%M-%S")), "w", encoding="utf-8") as f:
        f.write(separator.join(headers_row) + "\n")
        for item in content:
            row = _prepare_row(headers_row, item)
            f.write(separator.join(row) + "\n")

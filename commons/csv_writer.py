def _prepare_header(content):
    header = []
    for key in content[0]:
        header.append(key)
    return header


def _prepare_row(headers_row, item):
    row = []
    for key in item:
        if key in headers_row:
            row.append(item[key] if item[key] is not None else "")
    return row


def write(file: str, content: list[dict], separator: str = ";", headers: list[str] = None):
    headers_row = headers if headers is not None else _prepare_header(content)
    with open(file, "w", encoding="utf-8") as f:
        f.write(separator.join(headers_row) + "\n")
        for item in content:
            row = _prepare_row(headers_row, item)
            f.write(separator.join(row) + "\n")

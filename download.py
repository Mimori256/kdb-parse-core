import csv
import datetime
import io
import sys
from pathlib import Path

import requests

from subject_dataclass import Subject

KDB_URL = "https://kdb.tsukuba.ac.jp/"
KDB_EXPORT_ENCODING = "cp932"
CURRENT_KDB_ROW_LENGTH = len(Subject.CSV_HEADER) - 1


def get_academic_year(today: datetime.datetime | None = None) -> int:
    now = today or datetime.datetime.now()
    return now.year - 1 if now.month < 3 else now.year


def switch_to_japanese(session: requests.Session) -> None:
    response = session.post(
        KDB_URL,
        data={
            "widgetAction": "change",
            "widgetId": "BS0030",
            "pageId": "SB0070",
            "lang": "jpn",
        },
    )
    response.raise_for_status()


def create_download_payload(academic_year: int) -> dict[str, str]:
    return {
        "pageId": "SB0070",
        "action": "downloadList",
        "hdnFy": str(academic_year),
        "hdnTermCode": "",
        "hdnDayCode": "",
        "hdnPeriodCode": "",
        "hdnAgentName": "",
        "hdnOrg": "",
        "hdnIsManager": "",
        "hdnReq": "",
        "hdnFac": "",
        "hdnDepth": "",
        "hdnChkSyllabi": "",
        "hdnChkAuditor": "",
        "hdnChkExchangeStudent": "",
        "hdnChkConductedInEnglish": "",
        "hdnCourse": "",
        "hdnKeywords": "",
        "hdnFullname": "",
        "hdnDispDay": "",
        "hdnDispPeriod": "",
        "hdnOrgName": "",
        "hdnReqName": "",
        "cmbDwldtype": "csv",
    }


def is_html_response(content: bytes) -> bool:
    stripped = content.lstrip().lower()
    return stripped.startswith(b"<!doctype html") or stripped.startswith(b"<html")


def normalize_row(row: list[str]) -> list[str]:
    if len(row) == len(Subject.CSV_HEADER):
        return row

    if len(row) == CURRENT_KDB_ROW_LENGTH:
        return row[:7] + [""] + row[7:]

    raise ValueError(f"Unexpected CSV row length: {len(row)}")


def normalize_csv_text(csv_text: str) -> str:
    reader = csv.reader(io.StringIO(csv_text))
    rows = [row for row in reader if any(cell.strip() for cell in row)]

    if not rows:
        raise ValueError("The downloaded CSV is empty.")

    has_header = rows[0][0].strip() in {"科目番号", "Course Number"}
    data_rows = rows[1:] if has_header else rows

    normalized_rows = [Subject.CSV_HEADER]
    normalized_rows.extend(normalize_row(row) for row in data_rows)

    output = io.StringIO(newline="")
    writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writerows(normalized_rows)
    return output.getvalue()


def fetch_csv_text(session: requests.Session, academic_year: int) -> str:
    response = session.post(KDB_URL, data=create_download_payload(academic_year))
    response.raise_for_status()

    if is_html_response(response.content):
        raise ValueError("Failed to download CSV: KDB returned HTML instead.")

    decoded_text = response.content.decode(KDB_EXPORT_ENCODING)
    return normalize_csv_text(decoded_text)


def write_csv_if_changed(csv_text: str, output_path: str = "kdb.csv") -> bool:
    output_file = Path(output_path)

    if output_file.exists() and output_file.read_text(encoding="utf-8") == csv_text:
        print("No change")
        return False

    output_file.write_text(csv_text, encoding="utf-8")
    print("CSV updated")
    return True


def main() -> int:
    session = requests.Session()
    response = session.get(KDB_URL)
    response.raise_for_status()

    switch_to_japanese(session)
    csv_text = fetch_csv_text(session, get_academic_year())
    write_csv_if_changed(csv_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

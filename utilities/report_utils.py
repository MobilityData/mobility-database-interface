from utilities.validators import validate_report


def clean_report(report):
    validate_report(report)
    cleaned_report = {}
    for notice_type in report.get("notices"):
        notice_code = notice_type.get("code")
        cleaned_report[notice_code] = set()
        for notice in notice_type.get("notices"):
            cleaned_report[notice_code].add(notice.get("filename", ""))
    return cleaned_report

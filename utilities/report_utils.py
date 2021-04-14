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


def merge_reports(validation_report, system_report):
    return {**validation_report, **system_report}


def apply_report_to_scenario(report, scenario):
    use_cases_list = []
    for notices, use_cases in scenario:
        for notice in notices:
            pass
    return use_cases_list

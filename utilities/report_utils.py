from utilities.validators import validate_report
from utilities.notices import (
    STANDALONE,
    WITH_FILENAME,
    REPORT_NOTICES_TYPE,
    REPORT_NOTICES,
    REPORT_CODE,
    REPORT_FILENAME,
    REPORT_CHILD_FILENAME,
)


def clean_report(report):
    validate_report(report)
    cleaned_report = {STANDALONE: set(), WITH_FILENAME: {}}
    for notice_type in report.get(REPORT_NOTICES_TYPE):
        notice_code = notice_type.get(REPORT_CODE)
        for notice in notice_type.get(REPORT_NOTICES):
            if REPORT_FILENAME in notice or REPORT_CHILD_FILENAME in notice:
                if REPORT_FILENAME in notice:
                    filename = notice.get(REPORT_FILENAME)
                else:
                    filename = notice.get(REPORT_CHILD_FILENAME)
                if filename not in cleaned_report[WITH_FILENAME]:
                    cleaned_report[WITH_FILENAME][filename] = set()
                cleaned_report[WITH_FILENAME][filename].add(notice_code)
            else:
                cleaned_report[STANDALONE].add(notice_code)
    return cleaned_report


def merge_reports(validation_report, system_report):
    report = {STANDALONE: set(), WITH_FILENAME: {}}
    report[STANDALONE].update(validation_report[STANDALONE])
    report[STANDALONE].update(system_report[STANDALONE])

    with_filename_keys = set()
    with_filename_keys.update(validation_report[WITH_FILENAME].keys())
    with_filename_keys.update(system_report[WITH_FILENAME].keys())

    for key in with_filename_keys:
        report[WITH_FILENAME][key] = set()
        report[WITH_FILENAME][key].update(
            validation_report[WITH_FILENAME].get(key, set())
        )
        report[WITH_FILENAME][key].update(system_report[WITH_FILENAME].get(key, set()))
    return report


def apply_report_to_scenario(report, scenario):
    use_cases_list = []
    for notices, use_cases in scenario:
        for notice in notices:
            pass
    return use_cases_list

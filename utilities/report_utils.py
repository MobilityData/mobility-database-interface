from utilities.validators import validate_report
from utilities.notices import (
    STANDALONE,
    WITH_FILENAME,
    FILENAME,
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
    validated_scenario = []
    for use_case_notices, use_case_functions in scenario:
        is_valid = True

        # If a standalone notice is problematic for a use case
        # and exists in the report standalone notices,
        # then the use case is not valid
        if use_case_notices[STANDALONE].intersection(report[STANDALONE]):
            is_valid = False

        # If a notice "with filename" is problematic for a use case
        # and exists in the report notices "with filename"
        # for a filename concerned by the use case,
        # then the use case is not valid
        if use_case_notices[FILENAME].intersection(report[WITH_FILENAME].keys()):
            for filename, notices in report[WITH_FILENAME].items():
                if filename in use_case_notices[FILENAME] and use_case_notices[
                    WITH_FILENAME
                ].intersection(notices):
                    is_valid = False

        # If the use case is valid, keep it in the validated scenario
        if is_valid:
            validated_scenario += use_case_functions
    return validated_scenario

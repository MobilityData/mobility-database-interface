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
    # Verify the report has the minimum information to be valid
    validate_report(report)

    # Since the original report can be bulky,
    # we clean the report to keep only the meaningful information for us
    # Here "STANDALONE" stands for the set of notices that independent of a filename
    # and is related to a specific context.
    # "WITH_FILENAME" stands for the notices that can exist for various files (filenames)
    # and comes with either a "filename" of "child_filename" value in the original report.
    cleaned_report = {STANDALONE: set(), WITH_FILENAME: {}}

    # Gather notices
    for notice_type in report[REPORT_NOTICES_TYPE]:
        notice_code = notice_type[REPORT_CODE]
        for notice in notice_type[REPORT_NOTICES]:
            has_filename = REPORT_FILENAME in notice
            has_child_filename = REPORT_CHILD_FILENAME in notice
            if has_filename or has_child_filename:
                if has_filename:
                    filename = notice.get(REPORT_FILENAME)
                else:
                    filename = notice.get(REPORT_CHILD_FILENAME)

                # We use the filename as sub key within the "WITH_FILENAME" dictionary,
                # so a filename has a set of notice codes as value,
                # i.e. {filename_1: {code_1a ... code_1n}, ..., filename_2: {code_2a ... code_2n}}
                # This will reduce the verification of the problematic notices for each use case,
                # because only the filenames related to a use case will be checked for problematic notices.
                if filename not in cleaned_report[WITH_FILENAME]:
                    cleaned_report[WITH_FILENAME][filename] = set()
                cleaned_report[WITH_FILENAME][filename].add(notice_code)
            else:
                cleaned_report[STANDALONE].add(notice_code)

    # Return the cleaned report which will look like this:
    # {
    #   STANDALONE: {sa_code_1, ..., sa_code_n},
    #   WITH_FILENAME: {filename_1: {code_1a ... code_1n}, ..., filename_2: {code_2a ... code_2n}}
    # }
    return cleaned_report


def merge_reports(validation_report, system_report):
    # Merging both report into one to reduce
    # the verification time of the problematic notices of each use case.
    # By doing so, the verification will be done once (with a sole report),
    # instead of twice (on two reports).
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
    for use_case_key, (use_case_notices, use_case_functions) in scenario.items():
        is_valid = True

        # If a standalone notice is problematic for a use case
        # and exists in the report standalone notices,
        # then the use case is not valid
        has_standalone_problematic_notices = use_case_notices[STANDALONE].intersection(
            report[STANDALONE]
        )
        if has_standalone_problematic_notices:
            is_valid = False
        else:
            # Continue the verification only if the use case
            # is valid post standalone notices verification
            has_concerned_filename = use_case_notices[FILENAME].intersection(
                report[WITH_FILENAME].keys()
            )
            if has_concerned_filename:
                for filename, notices in report[WITH_FILENAME].items():
                    # If a notice "with filename" is problematic for a use case
                    # and exists in the report notices "with filename"
                    # for a filename concerned by the use case,
                    # then the use case is not valid
                    has_with_filename_problematic_notices = (
                        filename in use_case_notices[FILENAME]
                        and use_case_notices[WITH_FILENAME].intersection(notices)
                    )
                    if has_with_filename_problematic_notices:
                        is_valid = False
                        break

        # If the use case is valid, keep it in the validated scenario
        if is_valid:
            validated_scenario += use_case_functions
    return validated_scenario

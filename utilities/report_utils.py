from utilities.validators import validate_report


def clean_report(report):
    validate_report(report)
    cleaned_report = {"standalone": set(), "with_file": {}}
    for notice_type in report.get("notices"):
        notice_code = notice_type.get("code")
        for notice in notice_type.get("notices"):
            if "filename" in notice or "childFilename" in notice:
                if "filename" in notice:
                    filename = notice.get("filename")
                else:
                    filename = notice.get("childFilename")
                if filename not in cleaned_report["with_file"]:
                    cleaned_report["with_file"][filename] = set()
                cleaned_report["with_file"][filename].add(notice_code)
            else:
                cleaned_report["standalone"].add(notice_code)
    return cleaned_report


def merge_reports(validation_report, system_report):
    report = {"standalone": set(), "with_file": {}}
    report["standalone"].update(validation_report["standalone"])
    report["standalone"].update(system_report["standalone"])

    with_file_keys = set()
    with_file_keys.update(validation_report["with_file"].keys())
    with_file_keys.update(system_report["with_file"].keys())

    for key in with_file_keys:
        report["with_file"][key] = set()
        report["with_file"][key].update(validation_report["with_file"].get(key, set()))
        report["with_file"][key].update(system_report["with_file"].get(key, set()))
    return report


def apply_report_to_scenario(report, scenario):
    use_cases_list = []
    for notices, use_cases in scenario:
        for notice in notices:
            pass
    return use_cases_list

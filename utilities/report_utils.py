def clean_report(report):
    cleaned_report = {}
    for notices in report.get("notices", []):
        notices_key = notices.get("code", None)
        if notices_key:
            cleaned_report[notices_key] = set()
        else:
            raise (
                Exception,
                "The report is invalid, contains blank notices code value.",
            )
        for notice in notices.get("notices", []):
            if "filename" in notice:
                cleaned_report[notices_key].add(notice.get("filename", []))
    return cleaned_report

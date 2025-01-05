def validate_start_end_dates(date_start, date_end):
    """
    Validate that the start date is before the end date.
    """
    if date_start and date_end and date_start < date_end:
        return date_start, date_end

    return None, None


def validate_module_start_end_dates(start, end, old_module_dates):
    """
    Validate that the new module dates do not overlap with old module dates.
    """
    for dates in old_module_dates:
        old_start = dates.get("date_start")
        old_end = dates.get("date_end")

        if start < old_end and end > old_start:
            return False

    return True

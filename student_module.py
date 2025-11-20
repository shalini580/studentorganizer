def attendance_breakdown(profile):
    summaries = []
    total_held = 0
    total_attended = 0
    for name, info in profile.get("subjects", {}).items():
        weeks = info.get("weeks", {})
        held = sum(entry.get("held", 0) for entry in weeks.values())
        attended = sum(entry.get("attended", 0) for entry in weeks.values())
        total_held += held
        total_attended += attended
        percent = (attended / held * 100) if held else 0
        summaries.append({
            "name": name,
            "held": held,
            "attended": attended,
            "percent": percent,
        })
    overall_pct = (total_attended / total_held * 100) if total_held else 0
    return summaries, total_attended, total_held, overall_pct

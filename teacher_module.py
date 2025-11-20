def list_students(ds):
    """Return the students list (from datastore)."""
    return ds.s

def ensure_student_entry(ds, reg):
    stu = ds.student(reg)
    if not stu:
        return None
    return ds.ensure_student(stu)

def add_subject(ds, reg, subject_name, per_week):
    entry = ensure_student_entry(ds, reg)
    if entry is None:
        return False, "Student not found"
    if subject_name in entry["subjects"]:
        return False, "Subject exists"
    entry["subjects"][subject_name] = {"per_week": per_week or 0, "weeks": {}}
    ds.save()
    return True, None

def update_week(ds, reg, subject_names, week, held, attended):
    """
    subject_names: list of subject names to update
    held, attended are integers
    """
    entry = ensure_student_entry(ds, reg)
    if entry is None:
        return False, "Student not found"
    subs = entry["subjects"]
    updated = False
    for name in subject_names:
        if name not in subs:
            continue
        if attended > held:
            attended = held
        subj = subs[name]
        subj.setdefault("weeks", {})[str(week)] = {"held": held, "attended": attended}
        subj["per_week"] = subj.get("per_week", held) or held
        updated = True
    if updated:
        ds.save()
        return True, None
    return False, "No subjects updated"

def attendance_report(ds, reg):
    entry = ensure_student_entry(ds, reg)
    if entry is None:
        return None, "Student not found"
    summaries = []
    total_held = 0
    total_attended = 0
    for name, info in entry.get("subjects", {}).items():
        weeks = info.get("weeks", {})
        held = sum(e.get("held", 0) for e in weeks.values())
        att = sum(e.get("attended", 0) for e in weeks.values())
        total_held += held
        total_attended += att
        pct = (att / held * 100) if held else 0
        summaries.append({"name": name, "held": held, "attended": att, "percent": pct})
    overall = (total_attended / total_held * 100) if total_held else 0
    return {"summaries": summaries, "total_attended": total_attended, "total_held": total_held, "overall": overall}, None

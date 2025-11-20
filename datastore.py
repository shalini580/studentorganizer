import json, os

DF = "data.json"
SF = "students.json"
TF = "teachers.json"

DEF_STORE = {"attendance": {}, "todo": {}, "expenses": {}}
DEF_STUD = [
 {"reg":"24021107","name":"Asha Rao","password":"pass123"},
 {"reg":"24021108","name":"Irfan Khan","password":"pass234"},
 {"reg":"24021109","name":"Nandini Jain","password":"pass345"},
 {"reg":"24021110","name":"Kumar Vivek","password":"pass456"},
 {"reg":"24021111","name":"Meera Patel","password":"pass567"},
 {"reg":"24021112","name":"Rohit Das","password":"pass678"},
 {"reg":"24021113","name":"Divya Pillai","password":"pass789"},
 {"reg":"24021114","name":"Sanjay Roy","password":"pass890"},
]
DEF_TEACH = [
 {"reg":"T001","name":"Ms. Mehta","password":"teach123"},
 {"reg":"T002","name":"Mr. Fernandes","password":"teach234"},
 {"reg":"T003","name":"Dr. Sandhu","password":"teach345"},
 {"reg":"T004","name":"Prof. Iyer","password":"teach456"},
 {"reg":"T005","name":"Mrs. Rawat","password":"teach567"},
 {"reg":"T006","name":"Mr. Das","password":"teach678"},
 {"reg":"T007","name":"Ms. Kapoor","password":"teach789"},
 {"reg":"T008","name":"Dr. Roy","password":"teach890"},
]

def _safe_read(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _write(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _ensure_file(path, default):
    """Ensure file exists and contains valid JSON. If not, create/populate with default."""
    cur = _safe_read(path)
    if cur is None:
        _write(path, json.loads(json.dumps(default)))
        return json.loads(json.dumps(default))
    return cur

def _merge(list_obj, defaults):
    existing = {r["reg"] for r in list_obj}
    changed = False
    for r in defaults:
        if r["reg"] not in existing:
            list_obj.append(json.loads(json.dumps(r)))
            changed = True
    return changed

class DS:
    def __init__(self):
        # Make sure each dataset is stored in its own JSON file
        self.s = _ensure_file(SF, DEF_STUD)
        self.t = _ensure_file(TF, DEF_TEACH)
        self.d = _ensure_file(DF, DEF_STORE)
        # If defaults had new entries, merge and write back
        if _merge(self.s, DEF_STUD):
            _write(SF, self.s)
        if _merge(self.t, DEF_TEACH):
            _write(TF, self.t)
        # Ensure data.json has required sections
        self.d.setdefault("attendance", {})
        self.d.setdefault("todo", {})
        self.d.setdefault("expenses", {})
        _write(DF, self.d)

    def save(self):
        _write(DF, self.d)

    def _find(self, reg, collection):
        for r in collection:
            if r["reg"] == reg:
                return r
        return None

    def student(self, reg):
        return self._find(reg, self.s)

    def teacher(self, reg):
        return self._find(reg, self.t)

    def ensure_student(self, student):
        reg = student["reg"]
        att = self.d.setdefault("attendance", {})
        if reg not in att:
            att[reg] = {"name": student["name"], "subjects": {}}
        else:
            att[reg]["name"] = student["name"]
        self.d.setdefault("todo", {}).setdefault(reg, [])
        self.d.setdefault("expenses", {}).setdefault(reg, [])
        self.save()
        return att[reg]

    def todo_for(self, reg):
        self.d.setdefault("todo", {}).setdefault(reg, [])
        self.save()
        return self.d["todo"][reg]

    def expenses_for(self, reg):
        self.d.setdefault("expenses", {}).setdefault(reg, [])
        self.save()
        return self.d["expenses"][reg]

    def attendance_for(self, student):
        return self.ensure_student(student)

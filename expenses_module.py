def get_expenses(ds, reg):
    return ds.expenses_for(reg)

def add_expense(ds, reg, date, typ, note, amount):
    if typ is None or typ == "":
        return False, "Type required"
    try:
        a = float(amount)
    except (TypeError, ValueError):
        return False, "Invalid amount"
    data = ds.expenses_for(reg)
    data.append({"date": date, "type": typ, "note": note or "", "amount": a})
    ds.save()
    return True, None

def total_expenses(ds, reg):
    data = ds.expenses_for(reg)
    return sum(item.get("amount", 0.0) for item in data)

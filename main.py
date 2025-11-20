import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

import datastore as dsmod
import todo_module as todo_logic
import expenses_module as exp_logic
import student_module as sm_logic
import teacher_module as t_logic

COL = {
 "bg": "#0f172a", "panel": "#1f2937", "card": "#273449",
 "accent": "#38bdf8", "accent_dark": "#0284c7",
 "text": "#f8fafc", "muted": "#94a3b8"
}

class App:
    def __init__(self, root):
        self.r = root
        self.ds = dsmod.DS()
        self.u = None
        self.rl = None
        self.colors = COL
        self.r.title("Campus Productivity Hub")
        self.r.geometry("520x360")
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground=self.colors["text"])
        self.style.map("Accent.TButton", background=[("active", self.colors["accent_dark"])])
        self.style.configure("Secondary.TButton", background=self.colors["card"], foreground=self.colors["text"])
        self.style.configure("Heading.TLabel", font=("Segoe UI", 18, "bold"), background=self.colors["panel"], foreground=self.colors["text"])
        self.style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"])
        self.mainf = None
        self.show_login()

    def clear(self):
        if self.mainf:
            self.mainf.destroy()

    def show_login(self):
        self.clear()
        f = tk.Frame(self.r, padx=30, pady=30, bg=self.colors["panel"])
        f.pack(fill=tk.BOTH, expand=True)
        self.mainf = f
        ttk.Label(f, text="Campus Productivity Hub", style="Heading.TLabel").pack(pady=(0,10))
        ttk.Label(f, text="Login to continue", font=("Segoe UI", 11)).pack(pady=(0,10))
        ttk.Label(f, text="Registration Number").pack(anchor="w")
        e_reg = ttk.Entry(f); e_reg.pack(fill=tk.X, pady=5, ipady=3)
        ttk.Label(f, text="Password").pack(anchor="w")
        e_pwd = ttk.Entry(f, show="*"); e_pwd.pack(fill=tk.X, pady=5, ipady=3)

        def do_login():
            r = e_reg.get().strip(); p = e_pwd.get().strip()
            if not (r and p):
                messagebox.showinfo("Info", "Enter both fields.")
                return
            t = self.ds.teacher(r)
            if t and t["password"] == p:
                self.u = t; self.rl = "teacher"; self.show_home(); return
            s = self.ds.student(r)
            if s and s["password"] == p:
                self.u = s; self.rl = "student"
                self.ds.ensure_student(s)
                self.show_home(); return
            messagebox.showerror("Error", "Invalid login details.")

        ttk.Button(f, text="Login", command=do_login, style="Accent.TButton").pack(pady=15, fill=tk.X)

    def show_home(self):
        self.clear()
        f = tk.Frame(self.r, padx=30, pady=30, bg=self.colors["panel"])
        f.pack(fill=tk.BOTH, expand=True)
        self.mainf = f
        ttk.Label(f, text=f"Welcome {self.u['name']}", style="Heading.TLabel").pack(pady=(0,5))
        ttk.Label(f, text=f"Role: {self.rl.title()}", font=("Segoe UI", 11), foreground=self.colors["muted"]).pack(pady=(0,12))

        if self.rl == "teacher":
            ttk.Button(f, text="Teacher Module", command=self.open_teacher, style="Accent.TButton").pack(fill=tk.X, pady=6)
        else:
            ttk.Button(f, text="Student Module", command=self.open_student, style="Accent.TButton").pack(fill=tk.X, pady=6)

        ttk.Button(f, text="To-Do List", command=self.open_todo, style="Accent.TButton").pack(fill=tk.X, pady=6)
        ttk.Button(f, text="Expenses Tracker", command=self.open_expenses, style="Accent.TButton").pack(fill=tk.X, pady=6)
        ttk.Button(f, text="Logout", command=self.logout, style="Secondary.TButton").pack(fill=tk.X, pady=10)

    def logout(self):
        self.u = None; self.rl = None
        self.show_login()

    # ---------- To-Do GUI uses logic from todo_module ----------
    def open_todo(self):
        w = tk.Toplevel(self.r); w.title("To-Do List"); w.geometry("560x420"); w.configure(bg=self.colors["bg"])
        reg = self.u["reg"]
        tasks = todo_logic.get_tasks(self.ds, reg)

        lb = tk.Listbox(w, bg=self.colors["card"], fg=self.colors["text"], selectbackground=self.colors["accent"], height=12)
        lb.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20,10))

        def refresh():
            lb.delete(0, tk.END)
            for i, t in enumerate(tasks, 1):
                lb.insert(tk.END, f"{i}. {t['text']} [{t['state']}] ({t['date']})")

        def add_task():
            txt = simpledialog.askstring("Task", "Enter task:", parent=w)
            if not txt:
                return
            todo_logic.add_task(self.ds, reg, txt)
            refresh()

        def mark_done():
            sel = lb.curselection()
            if not sel:
                messagebox.showinfo("Info", "Select a task.")
                return
            todo_logic.mark_done(self.ds, reg, sel[0])
            refresh()

        def delete_task():
            sel = lb.curselection()
            if not sel:
                messagebox.showinfo("Info", "Select a task.")
                return
            todo_logic.delete_task(self.ds, reg, sel[0])
            refresh()

        btnf = tk.Frame(w, bg=self.colors["bg"]); btnf.pack(pady=8)
        ttk.Button(btnf, text="Add", command=add_task, style="Accent.TButton").grid(row=0, column=0, padx=6)
        ttk.Button(btnf, text="Done", command=mark_done, style="Accent.TButton").grid(row=0, column=1, padx=6)
        ttk.Button(btnf, text="Delete", command=delete_task, style="Accent.TButton").grid(row=0, column=2, padx=6)
        ttk.Button(btnf, text="Refresh", command=refresh, style="Secondary.TButton").grid(row=0, column=3, padx=6)
        refresh()

    # ---------- Expenses GUI uses logic from expenses_module ----------
    def open_expenses(self):
        w = tk.Toplevel(self.r); w.title("Expense Tracker"); w.geometry("660x420"); w.configure(bg=self.colors["bg"])
        reg = self.u["reg"]
        data = exp_logic.get_expenses(self.ds, reg)

        cols = ("date", "type", "note", "amount")
        tr = ttk.Treeview(w, columns=cols, show="headings", height=12)
        for c in cols:
            tr.heading(c, text=c.title()); tr.column(c, width=140)
        tr.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15,10))

        def refresh():
            tr.delete(*tr.get_children())
            for r in data:
                tr.insert("", tk.END, values=(r["date"], r["type"], r["note"], f"₹{r['amount']:.2f}"))

        def add_exp():
            date = simpledialog.askstring("Date", "YYYY-MM-DD (blank for today):", parent=w)
            if not date:
                date = datetime.today().strftime("%Y-%m-%d")
            typ = simpledialog.askstring("Type", "Category:", parent=w)
            if not typ:
                return
            note = simpledialog.askstring("Note", "Short note:", parent=w) or ""
            amt_text = simpledialog.askstring("Amount", "Enter amount:", parent=w)
            ok, err = exp_logic.add_expense(self.ds, reg, date, typ, note, amt_text)
            if not ok:
                messagebox.showerror("Error", err)
                return
            refresh()

        def show_total():
            total = exp_logic.total_expenses(self.ds, reg)
            messagebox.showinfo("Total", f"Total spent: ₹{total:.2f}")

        btnf = tk.Frame(w, bg=self.colors["bg"]); btnf.pack()
        ttk.Button(btnf, text="Add", command=add_exp, style="Accent.TButton").grid(row=0, column=0, padx=6)
        ttk.Button(btnf, text="Total", command=show_total, style="Accent.TButton").grid(row=0, column=1, padx=6)
        ttk.Button(btnf, text="Refresh", command=refresh, style="Secondary.TButton").grid(row=0, column=2, padx=6)
        refresh()

    # ---------- Student GUI uses student_module logic ----------
    def open_student(self):
        w = tk.Toplevel(self.r); w.title("My Attendance"); w.geometry("560x400"); w.configure(bg=self.colors["bg"])
        profile = self.ds.attendance_for(self.u)
        txt = tk.Text(w, width=60, height=15, state=tk.DISABLED, bg=self.colors["card"], fg=self.colors["text"], bd=0)
        txt.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        def show():
            txt.config(state=tk.NORMAL); txt.delete("1.0", tk.END)
            txt.insert(tk.END, f"Student: {profile['name']} ({self.u['reg']})\n\n")
            summaries, total_attended, total_held, overall_pct = sm_logic.attendance_breakdown(profile)
            if not summaries:
                txt.insert(tk.END, "No subjects yet. Contact your teacher.\n")
            else:
                for s in summaries:
                    txt.insert(tk.END, f"{s['name']}\n  Held: {s['held']}\n  Attended: {s['attended']}\n  Attendance: {s['percent']:.1f}%\n\n")
                txt.insert(tk.END, f"Overall\n  Held: {total_held}\n  Attended: {total_attended}\n  Attendance: {overall_pct:.1f}%\n")
            txt.config(state=tk.DISABLED)

        ttk.Button(w, text="Refresh", command=show, style="Accent.TButton").pack(pady=8)
        show()

    # ---------- Teacher GUI uses teacher_module logic ----------
    def open_teacher(self):
        w = tk.Toplevel(self.r); w.title("Teacher Attendance"); w.geometry("780x460"); w.configure(bg=self.colors["bg"])
        left = tk.Frame(w, bg=self.colors["panel"], padx=8, pady=8); left.pack(side=tk.LEFT, fill=tk.Y)
        right = tk.Frame(w, bg=self.colors["panel"], padx=8, pady=8); right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12,0))

        ttk.Label(left, text="Students", style="Heading.TLabel").pack(anchor="w", pady=(0,6))
        st_list = tk.Listbox(left, bg=self.colors["card"], fg=self.colors["text"], width=28, height=18, selectbackground=self.colors["accent"])
        st_list.pack()
        ttk.Label(right, text="Subjects", style="Heading.TLabel").pack(anchor="w", pady=(0,6))
        subj_box = tk.Listbox(right, bg=self.colors["card"], fg=self.colors["text"], height=14, selectbackground=self.colors["accent"])
        subj_box.pack(fill=tk.BOTH, expand=True)

        def refresh_students():
            st_list.delete(0, tk.END)
            for s in t_logic.list_students(self.ds):
                st_list.insert(tk.END, f"{s['reg']} - {s['name']}")

        def cur_reg():
            sel = st_list.curselection()
            if not sel:
                return None
            return st_list.get(sel[0]).split(" - ")[0]

        def load_subjects(_=None):
            subj_box.delete(0, tk.END)
            reg = cur_reg()
            if not reg:
                return
            entry = t_logic.ensure_student_entry(self.ds, reg)
            if not entry:
                return
            for name, info in entry["subjects"].items():
                subj_box.insert(tk.END, f"{name} | per week: {info.get('per_week', 0)} | weeks: {len(info.get('weeks', {}))}")

        def add_subject_flow():
            reg = cur_reg()
            if not reg:
                messagebox.showinfo("Info", "Select a student.")
                return
            name = simpledialog.askstring("Subject", "Subject name:", parent=w)
            if not name:
                return
            per = simpledialog.askinteger("Classes", "Classes per week:", parent=w, minvalue=0)
            if per is None:
                return
            ok, err = t_logic.add_subject(self.ds, reg, name, per)
            if not ok:
                messagebox.showerror("Error", err)
                return
            load_subjects()

        def update_week_flow():
            reg = cur_reg()
            if not reg:
                messagebox.showinfo("Info", "Select a student.")
                return
            entry = t_logic.ensure_student_entry(self.ds, reg)
            if not entry:
                return
            subs = entry["subjects"]
            if not subs:
                messagebox.showinfo("Info", "Add a subject first.")
                return
            names = ", ".join(subs.keys())
            choice = simpledialog.askstring(
                "Subject(s)",
                f"Type a subject name to update only that subject\nor type ALL to fill every subject.\n\nAvailable: {names}",
                parent=w,
            )
            if not choice:
                return
            choice = choice.strip()
            if choice.lower() == "all":
                targets = list(subs.keys())
            elif choice in subs:
                targets = [choice]
            else:
                messagebox.showinfo("Info", "Subject not found.")
                return
            week = simpledialog.askinteger("Week", "Week number to update (1-16):", parent=w, minvalue=1, maxvalue=16)
            if week is None:
                return
            # For each subject ask held and attended
            updated_any = False
            for subject_name in targets:
                held = simpledialog.askinteger("Classes held", f"{subject_name} — week {week}\nClasses held:", parent=w, minvalue=0)
                if held is None:
                    continue
                attended = simpledialog.askinteger("Classes attended", f"{subject_name} — week {week}\nClasses attended:", parent=w, minvalue=0)
                if attended is None:
                    continue
                ok, err = t_logic.update_week(self.ds, reg, [subject_name], week, held, attended)
                if ok:
                    updated_any = True
            if not updated_any:
                messagebox.showinfo("Info", "No updates saved.")
                return
            load_subjects()
            messagebox.showinfo("Saved", f"Saved week {week} data for {len(targets)} subject(s).")

        def view_report_flow():
            reg = cur_reg()
            if not reg:
                messagebox.showinfo("Info", "Select a student.")
                return
            rep, err = t_logic.attendance_report(self.ds, reg)
            if err:
                messagebox.showerror("Error", err)
                return
            lines = [f"Student: {self.ds.student(reg)['name']} ({reg})"]
            if not rep["summaries"]:
                lines.append("No attendance recorded yet.")
            else:
                for s in rep["summaries"]:
                    lines.append(f"{s['name']}: {s['attended']}/{s['held']} ({s['percent']:.1f}%)")
                lines.append("")
                lines.append(f"Overall: {rep['total_attended']}/{rep['total_held']} ({rep['overall']:.1f}%)")
            messagebox.showinfo("Report", "\n".join(lines))

        ttk.Button(left, text="Add Subject", command=add_subject_flow, style="Accent.TButton").pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Update Week", command=update_week_flow, style="Accent.TButton").pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Show Report", command=view_report_flow, style="Secondary.TButton").pack(fill=tk.X, pady=5)

        st_list.bind("<<ListboxSelect>>", lambda e: load_subjects())
        refresh_students()

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

def attendanceModule():
    profilesState = {"nextId": 1, "profiles": {}}     
    print("Attendance Manager (16-week Semester)")
    print("-")
    return mainMenu(profilesState)


def mainMenu(appState):
    while True:
        print("Main Menu:")
        print("1) Create New Profile")
        print("2) Add/Edit Weekly Attendance (All Subjects)")
        print("3) Generate Combined Report (All Subjects)")
        print("4) Generate Report (per Subject)")
        print("5) Edit Profile Details / Subjects")
        print("6) Exit")
        choice = input("Choose (1-6): ")
        if choice == "1":
            createProfile(appState)
        elif choice == "2":
            addWeeklyAttendance(appState)
        elif choice == "3":
            generateCombinedReport(appState)
        elif choice == "4":
            generateReport(appState)
        elif choice == "5":
            editProfile(appState)
        elif choice == "6":
            print("Goodbye!")
            return None
        else:
            print("Please choose a valid option.")


def promptNonEmpty(promptText):
    value = input(promptText)
    if value == "":
        print("Please enter a value.")
        return promptNonEmpty(promptText)
    return value


def promptNonNegativeInt(promptText):
    txt = input(promptText)
    if txt.isdigit():
        num = int(txt)
        if num >= 0:
            return num
    print("Please enter a non-negative whole number.")
    return promptNonNegativeInt(promptText)


def promptWeekNumber():
    txt = input("Enter week number (1-16): ")
    if txt.isdigit():
        num = int(txt)
        if 1 <= num <= 16:
            return num
    print("Please enter a week number between 1 and 16.")
    return promptWeekNumber()


def promptYesNo(promptText):
    ans = input(f"{promptText} (y/n): ").lower()
    if ans in ["y", "yes"]:
        return True
    if ans in ["n", "no"]:
        return False
    print("Please answer with 'y' or 'n'.")
    return promptYesNo(promptText)


def createProfile(appState):
    print("-")
    studentName = promptNonEmpty("Student name: ")
    print("Enter subjects with classes/week. Add at least one. Type 'done' to finish.")
    subjects = {}
    while True:
        name = input("Subject name (or 'done'): ")
        if name.lower() == "done":
            if len(subjects) == 0:
                print("Please add at least one subject.")
                continue
            break
        if name == "":
            print("Subject name cannot be empty.")
            continue
        if name in subjects:
            print("Subject already added.")
            continue
        perWeekTotal = promptNonNegativeInt("  Classes per week: ")
        subjects[name] = {
            "perWeekTotal": perWeekTotal,
            "attendanceByWeek": {}
        }

    profileId = appState["nextId"]
    appState["nextId"] = profileId + 1
    appState["profiles"][profileId] = {
        "studentName": studentName,
        "subjects": subjects
    }
    print(f"Created profile #{profileId} for {studentName} (Subjects: {', '.join(subjects.keys())}).")
    print("-")
    return profileId


def selectProfile(appState):
    profilesDict = appState["profiles"]
    if len(profilesDict) == 0:
        print("No profiles. Create one first.")
        return None
    print("Profiles:")
    for pid, pdata in profilesDict.items():
        subjectCount = len(pdata.get("subjects", {}))
        print(f"  {pid}) {pdata['studentName']} - {subjectCount} subject(s)")
    txt = input("Choose profile id: ")
    if txt.isdigit():
        chosenId = int(txt)
        if chosenId in profilesDict:
            return chosenId
    print("Please choose a valid profile id.")
    return selectProfile(appState)


def selectSubject(profileData):
    subjects = profileData.get("subjects", {})
    if len(subjects) == 0:
        print("No subjects found for this profile. Add subjects first.")
        return None
    print("Subjects:")
    subjectNames = list(subjects.keys())
    for i, name in enumerate(subjectNames, start=1):
        print(f"  {i}) {name} (classes/week: {subjects[name]['perWeekTotal']})")
    txt = input("Choose subject (number): ")
    if txt.isdigit():
        idx = int(txt)
        if 1 <= idx <= len(subjectNames):
            return subjectNames[idx - 1]
    print("Please choose a valid subject.")
    return selectSubject(profileData)


def addWeeklyAttendance(appState):
    print("-")
    profileId = selectProfile(appState)
    if profileId is None:
        return None
    profileData = appState["profiles"][profileId]
    weekNumber = promptWeekNumber()
    subjects = profileData.get("subjects", {})
    if len(subjects) == 0:
        print("No subjects found for this profile. Add subjects first.")
        print("-")
        return None
    print(f"Enter attended classes for week {weekNumber} (max per subject shown):")
    for name, sdata in subjects.items():
        perWeekTotal = sdata.get("perWeekTotal", 0)
        print(f"- {name}: classes/week = {perWeekTotal}")
        attended = promptNonNegativeInt("  Attended: ")
        if attended > perWeekTotal:
            print("  Attended cannot exceed classes/week. Capping to max.")
            attended = perWeekTotal
        sdata["attendanceByWeek"][weekNumber] = attended
    print(f"Saved week {weekNumber} attendance for all subjects (profile #{profileId}).")
    print("-")
    return None


def generateReport(appState):
    print("-")
    profileId = selectProfile(appState)
    if profileId is None:
        return None
    profileData = appState["profiles"][profileId]
    subjectName = selectSubject(profileData)
    if subjectName is None:
        return None
    subjectData = profileData["subjects"][subjectName]
    uptoWeekNumber = promptWeekNumber()
    if uptoWeekNumber < 1:
        uptoWeekNumber = 1
    if uptoWeekNumber > 16:
        uptoWeekNumber = 16

    perWeekTotal = subjectData["perWeekTotal"]
    totalConducted = perWeekTotal * uptoWeekNumber
    totalAttended = 0
    for weekNumber in range(1, uptoWeekNumber + 1):
        attendedInWeek = subjectData["attendanceByWeek"].get(weekNumber, 0)
        if attendedInWeek > perWeekTotal:
            attendedInWeek = perWeekTotal
        totalAttended += attendedInWeek

    percent = (totalAttended / totalConducted) * 100.0 if totalConducted > 0 else 0.0

    bar = buildBar(percent)

    print("Attendance Report")
    print("=")
    print(f"Student: {profileData['studentName']}")
    print(f"Subject: {subjectName}")
    print(f"Weeks Considered: {uptoWeekNumber} / 16")
    print(f"Classes/Week: {perWeekTotal}")
    print(f"Total Conducted: {totalConducted}")
    print(f"Total Attended: {totalAttended}")
    print(f"Attendance: {percent:.2f}%")
    print(bar)
    print("-")
    return None


def generateCombinedReport(appState):
    print("-")
    profileId = selectProfile(appState)
    if profileId is None:
        return None
    profileData = appState["profiles"][profileId]

    uptoWeekNumber = promptWeekNumber()
    if uptoWeekNumber < 1:
        uptoWeekNumber = 1
    if uptoWeekNumber > 16:
        uptoWeekNumber = 16

    subjects = profileData.get("subjects", {})
    if len(subjects) == 0:
        print("No subjects found for this profile.")
        print("-")
        return None

    totalConducted = 0
    totalAttended = 0

    for _, sdata in subjects.items():
        perWeekTotal = sdata.get("perWeekTotal", 0)
        totalConducted += perWeekTotal * uptoWeekNumber
        for weekNumber in range(1, uptoWeekNumber + 1):
            attendedInWeek = sdata["attendanceByWeek"].get(weekNumber, 0)
            if attendedInWeek > perWeekTotal:
                attendedInWeek = perWeekTotal
            totalAttended += attendedInWeek

    percent = (totalAttended / totalConducted) * 100.0 if totalConducted > 0 else 0.0

    bar = buildBar(percent)

    print("Combined Attendance Report (All Subjects)")
    print("=")
    print(f"Student: {profileData['studentName']}")
    print(f"Subjects: {', '.join(subjects.keys())}")
    print(f"Weeks Considered: {uptoWeekNumber} / 16")
    print(f"Total Conducted (all subjects): {totalConducted}")
    print(f"Total Attended (all subjects): {totalAttended}")
    print(f"Attendance: {percent:.2f}%")
    print(bar)
    print("-")
    return None


def editProfile(appState):
    print("-")
    profileId = selectProfile(appState)
    if profileId is None:
        return None
    profileData = appState["profiles"][profileId]
    print("Edit Menu:")
    print("1) Edit Student Name")
    print("2) Add Subject")
    print("3) Edit Subject Classes/Week")
    print("4) Rename Subject")
    print("5) Remove Subject")
    print("6) Back")
    menuChoice = input("Choose (1-6): ")
    if menuChoice == "1":
        profileData["studentName"] = promptNonEmpty("New student name: ")
        print("Updated.")
        return editProfile(appState)
    if menuChoice == "2":
        newName = promptNonEmpty("Subject name: ")
        if newName in profileData["subjects"]:
            print("Subject already exists.")
            return editProfile(appState)
        perWeek = promptNonNegativeInt("Classes per week: ")
        profileData["subjects"][newName] = {
            "perWeekTotal": perWeek,
            "attendanceByWeek": {}
        }
        print("Added subject.")
        return editProfile(appState)
    if menuChoice == "3":
        subjectName = selectSubject(profileData)
        if subjectName is None:
            return None
        perWeek = promptNonNegativeInt("New classes per week: ")
        profileData["subjects"][subjectName]["perWeekTotal"] = perWeek
        print("Updated classes per week.")
        return editProfile(appState)
    if menuChoice == "4":
        subjectName = selectSubject(profileData)
        if subjectName is None:
            return None
        newName = promptNonEmpty("New subject name: ")
        if newName in profileData["subjects"]:
            print("Another subject already has this name.")
            return editProfile(appState)
        profileData["subjects"][newName] = profileData["subjects"].pop(subjectName)
        print("Renamed subject.")
        return editProfile(appState)
    if menuChoice == "5":
        subjectName = selectSubject(profileData)
        if subjectName is None:
            return None
        if not promptYesNo(f"Remove subject '{subjectName}'?"):
            return editProfile(appState)
        profileData["subjects"].pop(subjectName, None)
        print("Removed subject.")
        return editProfile(appState)
    if menuChoice == "6":
        return None
    print("Please choose a valid option.")
    return editProfile(appState)


def buildBar(percent):
    equalsCount = int(percent // 5)
    if equalsCount > 20:
        equalsCount = 20
    if equalsCount < 0:
        equalsCount = 0
    spacesCount = 20 - equalsCount
    return "[" + ("=" * equalsCount) + (" " * spacesCount) + "]"


if __name__ == "__main__":           

    attendanceModule()
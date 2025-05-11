import os

def names():
    path= r"C:\Users\PRATIK SAHA\OneDrive\Desktop\project1\Successful proj\Attendance_project\Student pics"
    name01 = []
    all_files = os.listdir(path)
    for file in all_files:
        file = file.strip().lower()
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            name02 = file.replace(".jpg", "").replace(".jpeg", "").replace(".png", "")
            name01.append(name02)

    return name01

# a=names()
# print(a)
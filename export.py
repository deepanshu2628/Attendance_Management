import pandas as pd # pyright: ignore[reportMissingModuleSource]
from database import get_attendance

def export_attendance(filename="attendance_report.xlsx"):
    data = get_attendance()
    df = pd.DataFrame(data, columns=["Roll No", "Name", "Date", "Status"])
    df.to_excel(filename, index=False)
    print(f"Attendance exported to {filename}")
    return filename

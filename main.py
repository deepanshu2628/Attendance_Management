from gui import launch_gui
from database import connect_db

if __name__ == "__main__":
    connect_db()
    launch_gui()

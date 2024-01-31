import sys
import os
from datetime import datetime,date

from tendo import singleton

from PySide6.QtCore import (Qt,QTimer)
from PySide6.QtWidgets import (QLineEdit,QComboBox, QPushButton, QApplication, 
    QVBoxLayout, QDialog, QLabel ,QMenu,QSystemTrayIcon)
from PySide6.QtGui import *

import utils

DATA_DIR = 'data'
SNOOZE_TIME_MINS = 15 #mins
JOBS = ['One', 'Two', 'Three', 'Four']

class TimeForm(QDialog):
    

    def __init__(self, parent=None):
        super(TimeForm, self).__init__(parent)

        self.setWindowTitle("Timmy")
        #self.setMouseTracking(True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.last_dismiss_time = datetime.now()
        # Create widgets
        #self.setStyleSheet('background-color: grey;')

        
        self.taskEdit = QLineEdit(self)
        self.taskLabel = QLabel(self)
        self.taskLabel.setBuddy(self.taskEdit)

        self.jobCombo = QComboBox(self)
        self.jobLabel = QLabel(self)
        self.jobLabel.setText('Work job:')
        self.jobLabel.setBuddy(self.jobLabel)
        self.jobCombo.addItems(JOBS)

        self.button = QPushButton(f"Goodbye, for {SNOOZE_TIME_MINS} minutes")
        self.button.setDisabled(True)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.taskLabel)
        layout.addWidget(self.taskEdit)
        layout.addWidget(self.jobLabel)
        layout.addWidget(self.jobCombo)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)

       

        # Add button signal to greetings slot
        self.button.clicked.connect(self.snooze)
        self.taskEdit.textChanged.connect(self.validate_task)

        self.snoozeTimer=QTimer()
        self.snoozeTimer.timeout.connect(self.ping)

        
        self.snooze()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        print(event)
        return super().mouseMoveEvent(event)    

    def ping(self):
        self.taskLabel.setText(f'What you been doing since {self.last_dismiss_time.strftime("%I:%M %p")}')
        self.validate_task()
        self.show()

    def validate_task(self):
        if not self.taskEdit.text() or len(self.taskEdit.text().replace(" ", ""))==0:
            self.button.setDisabled(True)
        else:
            self.button.setDisabled(False)

    def startSnoozeTimer(self):
        self.snoozeTimer.start(SNOOZE_TIME_MS)

    def snooze(self):

        filename = 'wc_' +str(utils.week_start_stop()[0]) + '.csv'
        newfile = False
        if not os.path.isfile(os.path.join(DATA_DIR,filename)):
            newfile = True
        
        with open(os.path.join(DATA_DIR,filename), 'a') as the_file:
            if newfile:
                the_file.write('start,finish,task\n')
            the_file.write(f'{self.last_dismiss_time},{datetime.now()},{self.taskEdit.text()}\n')

        if DEBUG:
            print(f"Snoozing for {SNOOZE_TIME_MS} ms")
        self.hide()
        self.last_dismiss_time = datetime.now()

        self.startSnoozeTimer()

if __name__ == '__main__':

    me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
    
    DEBUG =False
    SNOOZE_TIME_MS = int((5/60 if DEBUG else SNOOZE_TIME_MINS)* 60 * 1000)

    # Create the Qt Application

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

     # Create and show the form
    form = TimeForm()

    # Adding an icon
    icon = QIcon("timmy.png")
        
    # Adding item on the menu bar
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.activated.connect(form.ping)
    # Creating the options
    menu = QMenu()
    
    # To quit the app
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    
    # Adding options to the System Tray
    tray.setContextMenu(menu)

    # Run the main Qt loop
    sys.exit(app.exec())
import sys, os
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import json
from pprint import pprint
from functools import partial

PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

def start_project(project):
    global PATH
    commands = ""
    if 'fields' in project:
        for field, value in project['fields'].items():
            commands += field + "=" + value + ";\n"

    if 'terminals' in project:
        for terminal, spec in project['terminals'].items():
            rcpath = PATH + "rc"
            # cd = "cd " + spec['location'] + "; "
            commands += "gnome-terminal --working-directory " + spec['location'] + \
                    " -e \"bash -c \\\" " + spec['command'] + \
                    "; exec bash --rcfile \\\"" + rcpath + "\\\" \\\"\"\n"

    if 'windows' in project:
        for window, command in project['windows'].items():
            commands += command + ";\n"

    print(commands)

    os.system(commands)
    QApplication.instance().quit()

class Starter(QWidget):

    def __init__(self):
        super().__init__()

        with open(PATH + 'projects.json') as f:
            self.projects = json.load(f)

        self.initUI()
        self.searchText = ""

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        counter = 0
        self.buttons = []

        sorted(self.projects['projects'], key=lambda project: project['name'])

        for project in self.projects['projects']:
            if project["enabled"]:
                btn = QPushButton(project['name'], self)
                btn.clicked.connect(partial(start_project, project))
                btn.resize(100, 30)
                btn.move(0, (counter+1)*30)
                btn.setStyleSheet("background-color: " + project['color'])
                self.buttons.append({"button": btn, "color": project['color'], "name": project["name"]})
                counter += 1

        lineedit = QLineEdit(self)
        lineedit.textChanged.connect(self.updateSearchText)
        lineedit.move(0, 0)
        lineedit.setFocus()
        lineedit.show()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Float')
        self.show()

    def updateSearchText(self, data):
        self.searchText = data.lower()

        for data in self.buttons:
            if self.searchText not in data["name"].lower():
                data["button"].setStyleSheet("background-color: #595959;");
            else:
                data["button"].setStyleSheet("background-color:" + data["color"] +";");

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            filtered = [project for project in self.projects['projects']
                    if self.searchText in project['name'].lower()]

            if len(filtered) > 0:
                start_project(filtered[0])
        elif event.key() == QtCore.Qt.Key_Escape:
            QApplication.instance().quit()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Starter()
    sys.exit(app.exec_())

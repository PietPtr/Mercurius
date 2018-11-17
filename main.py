import sys, os
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLineEdit, QLabel)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import json
from pprint import pprint
from functools import partial


class Starter(QWidget):

    def __init__(self):
        super().__init__()

        self.PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

        self.initUI()
        self.searchText = ""

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        counter = 0
        self.buttons = []

        error = None
        with open(self.PATH + 'projects.json') as f:
            try:
                self.config = json.load(f)
            except Exception as e:
                error = e

        if error == None:
            windowHeight = len(self.config['projects']) * 30 + 30
            self.config['projects'] = \
                    sorted(self.config['projects'], key=lambda project: project['name'])
            pprint(self.config)

            for project in self.config['projects']:
                if "enabled" in project and project["enabled"]:
                    btn = QPushButton(project['name'], self)
                    btn.clicked.connect(partial(self.start_project, project))
                    btn.resize(300, 30)
                    btn.move(0, (counter+1)*30)
                    btn.setStyleSheet("background-color: " + project['color'])
                    self.buttons.append({"button": btn, "color": project['color'], "name": project["name"]})
                    counter += 1

            lineedit = QLineEdit(self)
            lineedit.textChanged.connect(self.updateSearchText)
            lineedit.resize(200, 20)
            lineedit.move(50, 0)
            lineedit.setFocus()
            lineedit.show()
            self.setGeometry(1920/2 - 150, 1080 / 2 - windowHeight/2, 300, windowHeight)
        else:
            self.setGeometry(300, 300, 400, 300)

            print(error)
            errLabel = QLabel(self)
            errLabel.setText("Something is wrong with your configuration: \n" + str(error))
            errLabel.setMinimumSize(400, 0)
            errLabel.setWordWrap(True)

            pass

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
            filtered = [project for project in self.config['projects']
                    if self.searchText in project['name'].lower()]

            if len(filtered) > 0:
                self.start_project(filtered[0])
        elif event.key() == QtCore.Qt.Key_Escape:
            QApplication.instance().quit()

    def start_project(self, project):
        commands = ""
        globalFields = self.config['globalfields']

        for field, value in globalFields.items():
            commands += field + "=" + value + ";\n"

        if 'fields' in project:
            for field, value in project['fields'].items():
                commands += field + "=" + value + ";\n"

        if 'terminals' in project:
            for terminal, spec in project['terminals'].items():
                rcpath = self.PATH + "rc"
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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Starter()
    sys.exit(app.exec_())

# ChangeNames.py
# Written By: DJH
# Creation Date: 23 May 2016

# This program will search for all files within a folder that contain the "old String" and
# replace that portion of the filename with a "New String". Checkbox allows option to preview changes

import sys
import os
from PyQt4 import QtCore, QtGui
from ui_ChangeNames import Ui_MainWindow
import glob


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.home()  # contains links to functions for clicked buttons, etc.

    # use home(self) to handle all the signals that are sent from interacting with GUI
    def home(self):
        self.pushButton_FP.clicked.connect(self.browse_folderpath)
        self.pushButton_Run.clicked.connect(self.rename_files)
        self.pushButton_Clear.clicked.connect(self.clear_display)

    def browse_folderpath(self):
        # launch dialog to select folder that you want to change filenames in (if 'Browse' button is clicked)
        starting_dir = os.getcwd()
        # In order to get folders AND files to be shown. had to use the '.DontUseNativeDialog' in the last argument.
        # this makes the pop-up file broswer a little bit uglier (non-windows), but will show both files and folders
        # for native windows look, change to '.ShowDirsOnly' in the last argument
        folder_path = QtGui.QFileDialog.getExistingDirectory(None, "Select Folder That Contains Files To Be Re-Named",
                                                             starting_dir, QtGui.QFileDialog.DontUseNativeDialog)

        self.textEdit_FP.setText(folder_path)

    def clear_display(self):
        # allows user to clear the terminal display in case it's getting busy
        self.textBrowser_Terminal.clear()

    def rename_files(self):
        # this runs if 'Change Names' button is pressed. Will preview changes or change filenames depending on if 'preview' is checked
        fp = str(self.textEdit_FP.toPlainText())
        old = str(self.textEdit_Old.toPlainText())
        new = str(self.textEdit_New.toPlainText())
        files = []
        string_lengths = []
        filecount = 0

        # print out a header to the 'terminal' window of the app with some basic info for each time program runs
        self.textBrowser_Terminal.append("****************************************************************************")
        self.textBrowser_Terminal.append("****************************************************************************")
        self.textBrowser_Terminal.append("Folder:   " + fp)
        self.textBrowser_Terminal.append("Old String:   " + old)
        self.textBrowser_Terminal.append("New String:   " + new)
        self.textBrowser_Terminal.append("****************************************************************************" + '\n')

        # create list of all file names in selected directory which contain the 'old' string
        os.chdir(fp)  # needed if fp is different than working directory
        for file in glob.glob("*" + old + "*"):
            if file.find(old) != -1:
                files.append(file)
                string_lengths.append(len(file))

        # Catch if there are no file names with 'old' string and return message
        if len(files) == 0:
            self.textBrowser_Terminal.append("There are no Files in the selected directory which contain the Old String that was entered")
            self.textBrowser_Terminal.append("Note: Changes to file names are case-sensitive")

        elif len(files) != 0:
            max_length = max(string_lengths)
            print(max_length)

            if self.checkBox_Preview.isChecked() == True:
                # preview filename changes in the textBrowser window without actually renaming files
                for i in range(0, len(files)):
                    filename_old = files[i]
                    filename_new = filename_old.replace(old, new)
                    # display preview of filename changes
                    self.textBrowser_Terminal.append(filename_old.ljust(max_length) + "    >>>    " + filename_new + "\t***PREVIEW***")
                    filecount += 1

                self.textBrowser_Terminal.append('\n' + str(filecount) + "  Total files found containing the old string")
                self.textBrowser_Terminal.append("To make previewed changes to filenames, un-check the 'preview' box and \nre-click the 'change names' button")
                self.textBrowser_Terminal.append("****************************************************************************" + '\n\n')

            elif self.checkBox_Preview.isChecked() != True:
                for i in range(0, len(files)):
                    filename_old = files[i]
                    filename_new = filename_old.replace(old, new)
                    os.rename(filename_old, filename_new)
                    # display file renaming to terminal window
                    self.textBrowser_Terminal.append(filename_old.ljust(max_length) + "    >>>    " + filename_new)
                    filecount += 1

                # display output summary message
                self.textBrowser_Terminal.append('\n' + str(filecount) + "  Total files renamed in the selected folder:")
                self.textBrowser_Terminal.append(fp)
                self.textBrowser_Terminal.append("****************************************************************************" + '\n\n')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

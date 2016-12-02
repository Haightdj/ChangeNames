# ChangeNames.py
# Dependencies: ui_ChangeNames.py
# Written By: DJH
# Creation Date: 23 May 2016

# Edited 12/2/206
# --> Added error handling during renaming to account for attempts to over-write files [WinError 183]
# --> Added more defined paths to os.rename portion of script to avoid issues with path errors
# --> Made loops more pythonic

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

        else:
            max_length = max(string_lengths)

            if self.checkBox_Preview.isChecked():
                # preview filename changes in the textBrowser window without actually renaming files
                for filename_old in files:
                    filename_new = filename_old.replace(old, new)
                    # display preview of filename changes
                    self.textBrowser_Terminal.append(filename_old.ljust(max_length) + "    >>>    " + filename_new + "\t***PREVIEW***")
                    filecount += 1

                self.textBrowser_Terminal.append('\n' + str(filecount) + "  Total files found containing the old string")
                self.textBrowser_Terminal.append("To make previewed changes to filenames, un-check the 'preview' box and \nre-click the 'change names' button")
                self.textBrowser_Terminal.append("Note: changes will not be made if new file name already exists")
                self.textBrowser_Terminal.append("****************************************************************************" + '\n\n')

            else:
                # if preview is not checked, we will actually rename files!
                # added error handling to account for user trying to over-write files
                for filename_old in files:
                    filename_new = filename_old.replace(old, new)
                    # os.rename(filename_old, filename_new) #old line of code
                    # os.rename(os.path.join(fp, filename_old), os.path.join(fp, filename_new))  # new does this fix bug??

                    # Don't know how to use exceptions yet....
                    try:
                        os.rename(os.path.join(fp, filename_old), os.path.join(fp, filename_new))
                        self.textBrowser_Terminal.append(filename_old.ljust(max_length) + "    >>>    " + filename_new)
                        filecount += 1
                    except OSError as e:
                        # error_message = e
                        print('Exception Thrown')
                        print(e)
                        self.textBrowser_Terminal.append('Exception Thrown: Cannot overwrite file that already exists')
                        self.textBrowser_Terminal.append(filename_old.ljust(max_length) + "    >>>    " + filename_new + "\t ***ERROR***")

                # display output summary message
                self.textBrowser_Terminal.append('\n' + str(filecount) + "  Total files renamed in the selected folder:")
                self.textBrowser_Terminal.append(fp)
                self.textBrowser_Terminal.append("****************************************************************************" + '\n\n')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

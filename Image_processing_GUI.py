"""

"""
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys

from Image_processing_functions import *


class MainWindow(qtw.QWidget):

    page_select = qtc.pyqtSignal([str], ['QObject'])

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()

        # Configure the window -------------------------------------------------------
        self.setWindowTitle('IMAGE PROCESSING APP')
        self.resize(800, 600)

        # Create out widgets ---------------------------------------------------------
        self.path_entry = qtw.QLineEdit(cwd, self, maxLength=99)
        self.dpi_spin = qtw.QSpinBox(self, value=dpi, maximum=300, minimum=100, singleStep=50)
        self.filename0_entry = qtw.QLineEdit(filename0, self)
        self.filename1_entry = qtw.QLineEdit(filename1, self)
        self.format_entry = qtw.QComboBox(self)
        self.grayscale_check = qtw.QCheckBox('grayscale', self)
        self.page_off_check = qtw.QCheckBox('page_off', self)
        self.page_length_entry = qtw.QLineEdit('', self, placeholderText='Int only...')
        self.separation_spin = qtw.QSpinBox(self, value=separation)
        self.page_select_entry = qtw.QLineEdit('', self,  placeholderText='Enter page numbers...', maxLength=50)

        self.pdf2image_btn = qtw.QPushButton(
            'pdf2image',
            clicked=self.pdf2image_exe
        )
        self.pdf2image_dir_btn = qtw.QPushButton(
            'pdf2image_dir',
            clicked=self.pdf2image_dir_exe
        )
        self.add_image_tiff_btn = qtw.QPushButton(
            'add_image_tiff',
            clicked=self.add_image_tif_exe
        )

        self.pageSelectBtn = qtw.QPushButton('PageSelect', clicked=self.onPageSelect)

        # Configure widgets -------------------------------------------------------------
        # Add event categories
        self.format_entry.addItems(
            ['TIFF', 'JPEG', 'PNG']
        )

        # Arrange the widgets -----------------------------------------------------------
        # Create main_layout
        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)
        # result_layout = xxx


        # params_layout
        params_layout = qtw.QVBoxLayout()
        main_layout.addLayout(params_layout)
        params_layout.addWidget(qtw.QLabel('Image_processing_functions.py\n'
                                           'Image_processing_GUI.py'))
        # Execute
        execute_form = qtw.QGroupBox('Execute')
        params_layout.addWidget(execute_form)
        # execute_form_layout
        execute_form_layout = qtw.QGridLayout()
        execute_form_layout.addWidget(qtw.QLabel('# execute_form', self), 1, 1, 1, 10)
        execute_form_layout.addWidget(self.pdf2image_btn, 2, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># pdf2image()</b> :pdf -> image (jpg/png/tif)', self), 2, 2, 1, 1)
        execute_form_layout.addWidget(self.pdf2image_dir_btn, 3, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># pdf2image_dir()</b> :Convert all pdf files to images in the directory.', self), 3, 2, 1, 1)
        execute_form_layout.addWidget(self.add_image_tiff_btn, 4, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># add_image_tiff()</b> :Add filename1 to filename0 (pdf -> tif).', self), 4, 2, 1, 1)
        # execute_form_layout.addWidget(self.pageSelectBtn, 3, 1, 1, 1)
        # execute_form_layout.addWidget(qtw.QLabel('<b># onPageSelect()</b>', self), 3, 2, 1, 1)
        # Set GridLayout to execute_form_layout
        execute_form.setLayout(execute_form_layout)
        # Settings
        settings_form = qtw.QGroupBox('Settings')
        params_layout.addWidget(settings_form)
        # settings_form_layout
        settings_form_layout = qtw.QGridLayout()
        settings_form_layout.addWidget(qtw.QLabel('# settings_form', self), 1, 1, 1, 10)
        settings_form_layout.addWidget(self.path_entry, 2, 1, 1, 9)  # (row, column, row span, column span)
        settings_form_layout.addWidget(qtw.QLabel('<b># path</b>', self, margin=10), 2, 10, 1, 1)
        settings_form_layout.addWidget(self.dpi_spin, 3, 1, 1, 1)
        settings_form_layout.addWidget(qtw.QLabel('<b># dpi</b>', self), 3, 2, 1, 1)
        settings_form_layout.addWidget(self.format_entry, 3, 3, 1, 1)
        settings_form_layout.addWidget(qtw.QLabel('<b># format</b>', self), 3, 4, 1, 1)
        settings_form_layout.addWidget(self.filename0_entry, 4, 1, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename0</b>', self), 4, 4, 1, 1)
        settings_form_layout.addWidget(self.filename1_entry, 4, 5, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename1</b>', self), 4, 8, 1, 1)
        # Set GridLayout to settings_form_layout
        settings_form.setLayout(settings_form_layout)
        # Optional
        optional_form = qtw.QGroupBox('Optional')
        params_layout.addWidget(optional_form)
        # optional_form_layout
        optional_form_layout = qtw.QGridLayout()
        optional_form_layout.addWidget(qtw.QLabel('# optional_form', self), 1, 1, 1, 10)
        optional_form_layout.addWidget(self.grayscale_check, 2, 1, 1, 1)
        optional_form_layout.addWidget(self.page_off_check, 2, 3, 1, 1)
        optional_form_layout.addWidget(self.page_length_entry, 3, 1, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># page_length</b>', self), 3, 2, 1, 1)
        optional_form_layout.addWidget(self.separation_spin, 3, 3, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># separation</b>', self), 3, 4, 1, 1)
        optional_form_layout.addWidget(self.page_select_entry, 3, 5, 1, 2)
        optional_form_layout.addWidget(qtw.QLabel('<b># page_select</b>', self), 3, 7, 1, 1)
        # Set GridLayout to optional_form_layout
        optional_form.setLayout(optional_form_layout)

        # Connect Events --------------------------------------------------------------

        # grayscale_check -> True
        self.grayscale_check.setChecked(True)
        # page_off_check -> True
        self.page_off_check.setChecked(True)
        self.page_off_check.toggled.connect(self.page_length_entry.setDisabled)
        self.page_off_check.toggled.connect(self.separation_spin.setDisabled)
        self.page_off_check.toggled.connect(self.page_select_entry.setDisabled)
        # page_length_entry -> False
        self.page_length_entry.setDisabled(True)
        # separation_spin -> False
        self.separation_spin.setDisabled(True)
        # page_select_entry -> False
        self.page_select_entry.setDisabled(True)
        # On going
        self.pageSelectBtn.setDisabled(True)

        # End main UI code
        self.show()

    # Slots
    def onPageSelect(self):
        # self.page_select[str].emit(self.page_select_entry.text())
        print('type:', type(self.page_select))
        print('page_select:', self.page_select_entry.text())

    # Functions
    def pdf2image_exe(self):
        # self.page_select[str].connect()
        # text = self.page_select_entry.text()
        # print('text:', text)
        # text = text.replace(' ', '')
        # intlist = [int(x) for x in text]
        # self.page_select[str].emit(intlist)
        # LOG #
        print('path:', self.path_entry.text())
        print('dpi:', self.dpi_spin.text())
        print('filename:', self.filename0_entry.text())
        print('format:', self.format_entry.currentText())
        print('page_off:', self.page_off_check.isChecked())
        print('page_length:', self.page_length_entry.text())
        print('separation:', self.separation_spin.text())
        print('grayscale:', self.grayscale_check.isChecked())

        pdf2image(
            path=self.path_entry.text(),
            dpi=self.dpi_spin.text(),
            filename=self.filename0_entry.text(),
            format=self.format_entry.currentText(),
            page_off=self.page_off_check.isChecked(),
            page_length=self.page_length_entry.text(),
            separation=self.separation_spin.text(),
            page_select=self.page_select_entry.text(),
            grayscale=self.grayscale_check.isChecked()
        )

    def pdf2image_dir_exe(self):
        # LOG #
        print('path:', self.path_entry.text())
        print('dpi:', self.dpi_spin.text())
        print('format:', self.format_entry.currentText())
        print('page_off:', self.page_off_check.isChecked())
        print('grayscale:', self.grayscale_check.isChecked())

        pdf2image_dir(
            path=self.path_entry.text(),
            dpi=self.dpi_spin.text(),
            format=self.format_entry.currentText(),
            page_off=self.page_off_check.isChecked(),
            grayscale=self.grayscale_check.isChecked()
        )

    def add_image_tif_exe(self):
        # LOG #
        print('path:', self.path_entry.text())
        print('filename0', self.filename0_entry.text())
        print('filename1', self.filename1_entry.text())
        print('grayscale:', self.grayscale_check.isChecked())

        add_image_tif(
            path=self.path_entry.text(),
            filename0=self.filename0_entry.text(),
            filename1=self.filename1_entry.text(),
            grayscale=self.grayscale_check.isChecked()
        )


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())






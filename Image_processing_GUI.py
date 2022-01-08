"""
2021/12/31 Properties: "size/page_sel" were added to pdf2image. "add_image" launched.
2021/01/04 "Qsettings" synced. "imshow" added (image2image). "INPUT/OUTPUT" radio button added (image2image).
2021/01/08 "q_jpg" added (image2image). saved_info added (image_processing_GUI.py).
"""

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys
from Image_processing_functions import *


# INITIAL SETTINGS #
# True: Load QSettings info.
saved_info = True


class MainWindow(qtw.QWidget):
    # Store settings
    settings = qtc.QSettings('my_python', 'Image_processing_GUI')
    print('settings file directory: ', settings.fileName())
    # Clear settings
    if not saved_info:
        settings.clear()

    # SETTINGS #
    # ---- #
    # tab0 #
    path0 = settings.value('path0')
    dpi = settings.value('dpi')
    format = settings.value('format')
    filename = settings.value('filename')
    filename0 = settings.value('filename0')
    filename1 = settings.value('filename1')
    grayscale = settings.value('grayscale', False, type=bool)
    page_off = settings.value('page_off', False, type=bool)
    page_sel0 = settings.value('page_sel0', False, type=bool)
    page_sel1 = settings.value('page_sel1', False, type=bool)
    size_off = settings.value('size_off', False, type=bool)
    size0 = settings.value('size0')
    size1 = settings.value('size1')
    thread = settings.value('thread')
    # ---- #
    # tab1 #
    path1 = settings.value('path1')
    in_tif = settings.value('in_tif', False, type=bool)
    in_png = settings.value('in_png', False, type=bool)
    in_jpg = settings.value('in_jpg', False, type=bool)
    in_bmp = settings.value('in_bmp', False, type=bool)
    out_tif = settings.value('out_tif', False, type=bool)
    out_png = settings.value('out_png', False, type=bool)
    out_jpg = settings.value('out_jpg', False, type=bool)
    out_bmp = settings.value('out_bmp', False, type=bool)
    point_dic, range_dic = {}, {}
    point_exe0 = settings.value('point_exe0', False, type=bool)
    b0, g0, r0 = settings.value('b0'), settings.value('g0'), settings.value('r0')
    point_exe1 = settings.value('point_exe1', False, type=bool)
    b1, g1, r1 = settings.value('b1'), settings.value('g1'), settings.value('r1')
    range_exe0 = settings.value('range_exe0', False, type=bool)
    b0_from, g0_from, r0_from = settings.value('b0_from'), settings.value('g0_from'), settings.value('r0_from')
    b0_to, g0_to, r0_to = settings.value('b0_to'), settings.value('g0_to'), settings.value('r0_to')
    range_exe1 = settings.value('range_exe1', False, type=bool)
    b1_from, g1_from, r1_from = settings.value('b1_from'), settings.value('g1_from'), settings.value('r1_from')
    b1_to, g1_to, r1_to = settings.value('b1_to'), settings.value('g1_to'), settings.value('r1_to')
    imshow = settings.value('imshow', False, type=bool)
    q_jpg = settings.value('q_jpg')


    def __init__(self):
        """MainWindow constructor"""
        super().__init__()

        # Configure the window -------------------------------------------------------
        self.setWindowTitle('IMAGE PROCESSING APP')
        self.resize(800, 600)

        # Create widgets -------------------------------------------------------------
        # ---- #
        # tab0 #
        self.path0_ent = qtw.QLineEdit(self.path0, self, maxLength=99, placeholderText='Enter file path...')
        self.dpi_spn = qtw.QSpinBox(self, maximum=400, minimum=100, singleStep=50)
        self.format_cmb = qtw.QComboBox(self)
        self.filename_ent = qtw.QLineEdit(self.filename, self, placeholderText='Enter filename...')
        self.filename0_ent = qtw.QLineEdit(self.filename0, self, placeholderText='Enter filename...')
        self.filename1_ent = qtw.QLineEdit(self.filename1, self, placeholderText='Enter filename...')
        self.grayscale_chk = qtw.QCheckBox('grayscale', self)
        self.page_off_chk = qtw.QCheckBox('page_off', self)
        self.page_sel0_spn = qtw.QSpinBox(self, value=self.page_sel0)
        self.page_sel1_spn = qtw.QSpinBox(self, value=self.page_sel1)
        self.size_off_chk = qtw.QCheckBox('size_off', self)
        self.size0_spn = qtw.QSpinBox(self, value=self.size0, maximum=9999, minimum=9, singleStep=10)
        self.size1_spn = qtw.QSpinBox(self, value=self.size1, maximum=9999, minimum=9, singleStep=10)
        self.thread_spn = qtw.QSpinBox(self, value=self.thread, maximum=8, minimum=1)
        self.pdf2image_btn = qtw.QPushButton(
            'pdf2image',
            clicked=self.pdf2image_exe
        )
        self.pdf2image_dir_btn = qtw.QPushButton(
            'pdf2image_dir',
            clicked=self.pdf2image_dir_exe
        )
        self.add_image_tif_btn = qtw.QPushButton(
            'add_image_tif',
            clicked=self.add_image_tif_exe
        )
        self.add_BefAft_btn = qtw.QPushButton(
            'add_BefAft',
            clicked=self.add_BefAft_exe
        )
        # ---- #
        # tab1 #
        self.path1_ent = qtw.QLineEdit(self.path1, self, maxLength=99, placeholderText='Enter file path...')
        self.image2image_btn = qtw.QPushButton(
            'image2image',
            clicked=self.image2image_exe
        )
        self.in_tif_rad = qtw.QRadioButton('.tif')
        self.in_png_rad = qtw.QRadioButton('.png')
        self.in_jpg_rad = qtw.QRadioButton('.jpg')
        self.in_bmp_rad = qtw.QRadioButton('.bmp')
        self.out_tif_rad = qtw.QRadioButton('.tif')
        self.out_png_rad = qtw.QRadioButton('.png')
        self.out_jpg_rad = qtw.QRadioButton('.jpg')
        self.out_bmp_rad = qtw.QRadioButton('.bmp')
        self.point_exe0_chk = qtw.QCheckBox('Execute', self)
        self.b0_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.g0_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.r0_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.point_exe1_chk = qtw.QCheckBox('Execute', self)
        self.b1_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.g1_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.r1_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.range_exe0_chk = qtw.QCheckBox('Execute', self)
        self.b0_from_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.g0_from_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.r0_from_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.b0_to_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.g0_to_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.r0_to_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.range_exe1_chk = qtw.QCheckBox('Execute', self)
        self.b1_from_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.g1_from_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.r1_from_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.b1_to_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.g1_to_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.r1_to_spn = qtw.QSpinBox(self, minimum=0, maximum=255)
        self.imshow_chk = qtw.QCheckBox('imshow', self)
        self.q_jpg_spn = qtw.QSpinBox(self, value=100, minimum=1, maximum=100)

        # Configure widgets -------------------------------------------------------------
        # ---- #
        # tab0 #
        # Add event categories
        self.format_cmb.addItems(['.tif', '.jpg', '.png', '.bmp'])
        # ---- #
        # tab1 #

        # Arrange the widgets -----------------------------------------------------------
        # Create main_layout
        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)

        self.tabs = qtw.QTabWidget()
        self.tab0 = qtw.QWidget()
        self.tab1 = qtw.QWidget()

        self.tabs.addTab(self.tab0, 'pdf2image')
        self.tabs.addTab(self.tab1, 'image2image')

        # Tab layout ---------------------------------------------------------------------
        # ---- #
        # tab0 #
        self.tab0.layout = qtw.QVBoxLayout()
        self.tab0.layout.addWidget(qtw.QLabel('Image_processing_functions.py\n'
                                              'Image_processing_GUI.py'))
        # Execute box #
        execute_form = qtw.QGroupBox('Execute')
        self.tab0.layout.addWidget(execute_form)
        # execute_form_layout
        execute_form_layout = qtw.QGridLayout()
        execute_form_layout.addWidget(qtw.QLabel('# execute_form', self), 1, 1, 1, 10)
        execute_form_layout.addWidget(self.pdf2image_btn, 2, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># pdf2image()</b> :pdf -> image (jpg/png/tif). Be careful with "grayscale" checkbox.', self), 2, 2, 1, 1)
        execute_form_layout.addWidget(self.pdf2image_dir_btn, 3, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># pdf2image_dir()</b> :Convert all the pdf files to images (jpg/png/tif) in the path.', self), 3, 2, 1, 1)
        execute_form_layout.addWidget(self.add_image_tif_btn, 4, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># add_image_tif()</b> :Add filename1 on filename0 (tif -> tif).', self), 4, 2, 1, 1)
        execute_form_layout.addWidget(self.add_BefAft_btn, 5, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># add_BefAft()</b> :Add filename1 on filename0 (tif -> tif). Previous: Cyan. Changed: Magenta', self), 5, 2, 1, 1)
        # Set GridLayout to execute_form_layout
        execute_form.setLayout(execute_form_layout)

        # Settings box #
        settings_form = qtw.QGroupBox('Settings')
        self.tab0.layout.addWidget(settings_form)
        # settings_form_layout
        settings_form_layout = qtw.QGridLayout()
        settings_form_layout.addWidget(qtw.QLabel('# settings_form', self), 1, 1, 1, 10)
        settings_form_layout.addWidget(self.path0_ent, 2, 1, 1, 9)  # (row, column, row span, column span)
        settings_form_layout.addWidget(qtw.QLabel('<b># path0</b>', self), 2, 10, 1, 1)
        settings_form_layout.addWidget(self.dpi_spn, 3, 1, 1, 1)
        settings_form_layout.addWidget(qtw.QLabel('<b># dpi</b>', self), 3, 2, 1, 1)
        settings_form_layout.addWidget(self.format_cmb, 3, 3, 1, 1)
        settings_form_layout.addWidget(qtw.QLabel('<b># format</b>', self), 3, 4, 1, 1)
        settings_form_layout.addWidget(self.filename_ent, 5, 1, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename</b> :filename used for pdf2image', self), 5, 4, 1, 3)
        settings_form_layout.addWidget(self.filename0_ent, 6, 1, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename0</b>', self), 6, 4, 1, 1)
        settings_form_layout.addWidget(self.filename1_ent, 6, 5, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename1</b>', self), 6, 8, 1, 1)
        # Set GridLayout to settings_form_layout
        settings_form.setLayout(settings_form_layout)

        # Optional box #
        optional_form = qtw.QGroupBox('Optional')
        self.tab0.layout.addWidget(optional_form)

        # optional_form_layout
        optional_form_layout = qtw.QGridLayout()
        optional_form_layout.addWidget(qtw.QLabel('# optional_form', self), 1, 1, 1, 10)
        optional_form_layout.addWidget(self.grayscale_chk, 2, 1, 1, 1)
        optional_form_layout.addWidget(self.thread_spn, 2, 3, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># thread_count</b>(pdf2image)', self, alignment=qtc.Qt.AlignRight), 2, 4, 1, 1)
        # optional_form_layout.addWidget(qtw.QLabel('(pdf2image)', self), 2, 5, 1, 1)
        optional_form_layout.addWidget(self.page_off_chk, 3, 1, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('(pdf2image)', self), 3, 2, 1, 1)
        optional_form_layout.addWidget(self.size_off_chk, 3, 6, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('(pdf2image)', self), 3, 7, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('from', self, alignment=qtc.Qt.AlignRight), 4, 2, 1, 1)
        optional_form_layout.addWidget(self.page_sel0_spn, 4, 3, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># page_sel</b>', self), 4, 4, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('width', self, alignment=qtc.Qt.AlignRight), 4, 7, 1, 1)
        optional_form_layout.addWidget(self.size0_spn, 4, 8, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('to', self, alignment=qtc.Qt.AlignRight), 5, 2, 1, 1)
        optional_form_layout.addWidget(self.page_sel1_spn, 5, 3, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># page_sel</b> :Don\'t select the same page', self), 5, 4, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('height', self, alignment=qtc.Qt.AlignRight), 5, 7, 1, 1)
        optional_form_layout.addWidget(self.size1_spn, 5, 8, 1, 1)
        # Set GridLayout to optional_form_layout
        optional_form.setLayout(optional_form_layout)
        # Set tab0.layout to tab0
        self.tab0.setLayout(self.tab0.layout)

        # ---- #
        # tab1 #
        self.tab1.layout = qtw.QVBoxLayout()
        self.tab1.layout.addWidget(qtw.QLabel('Image_processing_functions.py\n'
                                              'Image_processing_GUI.py'))
        # Set tab1.layout
        self.tab1.setLayout(self.tab1.layout)

        # image2image_layout #
        image2image_layout = qtw.QGridLayout()
        # qtw.addWidget(self, row, column, row span, column span)
        image2image_layout.addWidget(qtw.QLabel('# image2image_layout', self), 1, 1, 1, 10)
        image2image_layout.addWidget(self.path1_ent, 2, 1, 1, 9)  # (row, column, row span, column span)
        image2image_layout.addWidget(qtw.QLabel('<b># path1</b>', self), 2, 10, 1, 1)
        image2image_layout.addWidget(self.image2image_btn, 3, 1, 1, 1)
        image2image_layout.addWidget(qtw.QLabel('# Convert all the image in the directory to arbitrary format'),
                                     3, 2, 1, 8)
        image2image_layout.addWidget(self.imshow_chk, 4, 1, 1, 1)
        image2image_layout.addWidget(self.q_jpg_spn, 4, 2, 1, 1)
        image2image_layout.addWidget(qtw.QLabel('<b># q_jpg</b> :Property for IMWRITE_JPEG_QUALITY. int: 1 - 100.', self), 4, 3, 1, 1)
        # Set image2image_layout to tab1.layout
        self.tab1.layout.addLayout(image2image_layout)

        # Input format #
        input_form = qtw.QGroupBox('Input')
        self.tab1.layout.addWidget(input_form)
        # input_form_layout
        input_form_layout = qtw.QGridLayout()
        # qtw.addWidget(self, row, column, row span, column span)
        input_form_layout.addWidget(self.in_tif_rad, 1, 1, 1, 1)
        input_form_layout.addWidget(self.in_png_rad, 1, 2, 1, 1)
        input_form_layout.addWidget(self.in_jpg_rad, 1, 3, 1, 1)
        input_form_layout.addWidget(self.in_bmp_rad, 1, 4, 1, 1)
        # Set input_form_layout to tab1.layout
        input_form.setLayout(input_form_layout)

        # Output format #
        output_form = qtw.QGroupBox('Output')
        self.tab1.layout.addWidget(output_form)
        # output_form_layout
        output_form_layout = qtw.QGridLayout()
        output_form_layout.addWidget(self.out_tif_rad, 1, 1, 1, 1)
        output_form_layout.addWidget(self.out_png_rad, 1, 2, 1, 1)
        output_form_layout.addWidget(self.out_jpg_rad, 1, 3, 1, 1)
        output_form_layout.addWidget(self.out_bmp_rad, 1, 4, 1, 1)
        # Set output_Form_layout to tab1.layout
        output_form.setLayout(output_form_layout)

        # point_form box #
        point_form = qtw.QGroupBox('Point Conversion')
        self.tab1.layout.addWidget(point_form)
        # point_form_layout
        point_form_layout = qtw.QGridLayout()
        # qtw.addWidget(self, row, column, row span, column span)
        # point_exe0
        point_form_layout.addWidget(qtw.QLabel('# point_form\nMake selected color transparent. \nOnly works for output: .png/.tif', self),
                                     1, 1, 1, 10)
        point_form_layout.addWidget(self.point_exe0_chk, 2, 1, 1, 1)
        point_form_layout.addWidget(self.b0_spn, 2, 2, 1, 1)
        point_form_layout.addWidget(qtw.QLabel('B', self), 2, 3, 1, 1)
        point_form_layout.addWidget(self.g0_spn, 2, 4, 1, 1)
        point_form_layout.addWidget(qtw.QLabel('G', self), 2, 5, 1, 1)
        point_form_layout.addWidget(self.r0_spn, 2, 6, 1, 1)
        point_form_layout.addWidget(qtw.QLabel('R', self), 2, 7, 1, 1)
        # point_exe1
        point_form_layout.addWidget(self.point_exe1_chk, 3, 1, 1, 1)
        point_form_layout.addWidget(self.b1_spn, 3, 2, 1, 1)
        point_form_layout.addWidget(qtw.QLabel('B', self), 3, 3, 1, 1)
        point_form_layout.addWidget(self.g1_spn, 3, 4, 1, 1)
        point_form_layout.addWidget(qtw.QLabel('G', self), 3, 5, 1, 1)
        point_form_layout.addWidget(self.r1_spn, 3, 6, 1, 1)
        point_form_layout.addWidget(qtw.QLabel('R', self), 3, 7, 1, 1)
        # Set point_form_layout to point_form
        point_form.setLayout(point_form_layout)

        # range_form box #
        range_form = qtw.QGroupBox('Range Conversion')
        self.tab1.layout.addWidget(range_form)
        # point_form_layout
        range_form_layout = qtw.QGridLayout()
        # qtw.addWidget(self, row, column, row span, column span)
        # range_exe0
        range_form_layout.addWidget(qtw.QLabel('# range_form\nMake selected color transparent. \nOnly works for output: .png/.tif.', self),
                                       1, 1, 1, 10)
        range_form_layout.addWidget(self.range_exe0_chk, 2, 1, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('from', self, alignment=qtc.Qt.AlignRight), 2, 2, 1, 1)
        range_form_layout.addWidget(self.b0_from_spn, 2, 3, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('B', self), 2, 4, 1, 1)
        range_form_layout.addWidget(self.g0_from_spn, 2, 5, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('G', self), 2, 6, 1, 1)
        range_form_layout.addWidget(self.r0_from_spn, 2, 7, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('R', self), 2, 8, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('to', self, alignment=qtc.Qt.AlignRight), 3, 2, 1, 1)
        range_form_layout.addWidget(self.b0_to_spn, 3, 3, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('B', self), 3, 4, 1, 1)
        range_form_layout.addWidget(self.g0_to_spn, 3, 5, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('G', self), 3, 6, 1, 1)
        range_form_layout.addWidget(self.r0_to_spn, 3, 7, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('R', self), 3, 8, 1, 1)
        # range_exe1
        range_form_layout.addWidget(self.range_exe1_chk, 4, 1, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('from', self, alignment=qtc.Qt.AlignRight), 4, 2, 1, 1)
        range_form_layout.addWidget(self.b1_from_spn, 4, 3, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('B', self), 4, 4, 1, 1)
        range_form_layout.addWidget(self.g1_from_spn, 4, 5, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('G', self), 4, 6, 1, 1)
        range_form_layout.addWidget(self.r1_from_spn, 4, 7, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('R', self), 4, 8, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('to', self, alignment=qtc.Qt.AlignRight), 5, 2, 1, 1)
        range_form_layout.addWidget(self.b1_to_spn, 5, 3, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('B', self), 5, 4, 1, 1)
        range_form_layout.addWidget(self.g1_to_spn, 5, 5, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('G', self), 5, 6, 1, 1)
        range_form_layout.addWidget(self.r1_to_spn, 5, 7, 1, 1)
        range_form_layout.addWidget(qtw.QLabel('R', self), 5, 8, 1, 1)
        # Set range_form_layout to range_form
        range_form.setLayout(range_form_layout)

        # Connect Events --------------------------------------------------------------
        # Sync to Checkbox
        # ---- #
        # tab0 #
        self.page_off_chk.toggled.connect(self.page_sel0_spn.setDisabled)
        self.page_off_chk.toggled.connect(self.page_sel1_spn.setDisabled)
        self.size_off_chk.toggled.connect(self.size0_spn.setDisabled)
        self.size_off_chk.toggled.connect(self.size1_spn.setDisabled)
        self.page_off_chk.setChecked(True)
        self.size_off_chk.setChecked(True)
        # Sync to Qsettings
        if saved_info == True:
            # ---- #
            # tab0 #
            self.dpi_spn.setValue(self.dpi)
            self.format_cmb.setCurrentText(self.format)
            self.grayscale_chk.setChecked(self.grayscale)
            self.page_off_chk.setChecked(self.page_off)
            self.page_sel0_spn.setValue(self.page_sel0)
            self.page_sel1_spn.setValue(self.page_sel1)
            self.size_off_chk.setChecked(self.size_off)
            self.size0_spn.setValue(self.size0)
            self.size1_spn.setValue(self.size1)
            self.thread_spn.setValue(self.thread)
            # ---- #
            # tab1 #
            # Sync to Qsettings
            self.in_tif_rad.setChecked(self.in_tif)
            self.in_png_rad.setChecked(self.in_png)
            self.in_jpg_rad.setChecked(self.in_jpg)
            self.in_bmp_rad.setChecked(self.in_bmp)
            self.out_tif_rad.setChecked(self.out_tif)
            self.out_png_rad.setChecked(self.out_png)
            self.out_jpg_rad.setChecked(self.out_jpg)
            self.out_bmp_rad.setChecked(self.out_bmp)
            self.point_exe0_chk.setChecked(self.point_exe0)
            self.b0_spn.setValue(self.b0)
            self.g0_spn.setValue(self.g0)
            self.r0_spn.setValue(self.r0)
            self.point_exe1_chk.setChecked(self.point_exe1)
            self.b1_spn.setValue(self.b1)
            self.g1_spn.setValue(self.g1)
            self.r1_spn.setValue(self.r1)
            self.range_exe0_chk.setChecked(self.range_exe0)
            self.b0_from_spn.setValue(self.b0_from)
            self.g0_from_spn.setValue(self.g0_from)
            self.r0_from_spn.setValue(self.r0_from)
            self.b0_to_spn.setValue(self.b0_to)
            self.g0_to_spn.setValue(self.g0_to)
            self.r0_to_spn.setValue(self.r0_to)
            self.range_exe1_chk.setChecked(self.range_exe1)
            self.b1_from_spn.setValue(self.b1_from)
            self.g1_from_spn.setValue(self.g1_from)
            self.r1_from_spn.setValue(self.r1_from)
            self.b1_to_spn.setValue(self.b1_to)
            self.g1_to_spn.setValue(self.g1_to)
            self.r1_to_spn.setValue(self.r1_to)
            self.imshow_chk.setChecked(self.imshow)
            self.q_jpg_spn.setValue(self.q_jpg)
        # Set tabs to main_layout ------------------------------------------------------
        main_layout.addWidget(self.tabs)
        # End main UI code -------------------------------------------------------------
        self.show()

    # Functions -------------------------------------------------------------------------
    # ---- #
    # tab0 #
    def pdf2image_exe(self):
        page_sel = [self.page_sel0_spn.value(), self.page_sel1_spn.value()]
        # size
        if self.size_off_chk.isChecked():
            size = None
        elif not self.size_off_chk.isChecked():
            size = (self.size0_spn.value(), self.size1_spn.value())
        else:
            Exception('Exception occurred in size')

        pdf2image(
            path=self.path0_ent.text(),
            dpi=self.dpi_spn.value(),
            filename=self.filename_ent.text(),
            format=self.format_cmb.currentText(),
            page_off=self.page_off_chk.isChecked(),
            page_sel=page_sel,
            grayscale=self.grayscale_chk.isChecked(),
            size=size,
            thread_count=self.thread_spn.value()
        )

    def pdf2image_dir_exe(self):
        pdf2image_dir(
            path=self.path0_ent.text(),
            dpi=self.dpi_spn.text(),
            format=self.format_cmb.currentText(),
            page_off=self.page_off_chk.isChecked(),
            grayscale=self.grayscale_chk.isChecked()
        )

    def add_image_tif_exe(self):
        add_image_tif(
            path=self.path0_ent.text(),
            filename0=self.filename0_ent.text(),
            filename1=self.filename1_ent.text(),
            grayscale=self.grayscale_chk.isChecked()
        )

    def add_BefAft_exe(self):
        add_BefAft(
            path=self.path0_ent.text(),
            filename0=self.filename0_ent.text(),
            filename1=self.filename1_ent.text(),
        )

    # ---- #
    # tab1 #
    def image2image_exe(self):
        # Put number in dictionary when Execute checked.
        if self.point_exe0_chk:
            self.point_dic['b0'] = self.b0_spn.value()
            self.point_dic['g0'] = self.g0_spn.value()
            self.point_dic['r0'] = self.g0_spn.value()
        if self.point_exe1_chk:
            self.point_dic['b1'] = self.b1_spn.value()
            self.point_dic['g1'] = self.g1_spn.value()
            self.point_dic['r1'] = self.r1_spn.value()
        if self.range_exe0_chk:
            self.range_dic['b0_from'] = self.b0_from_spn.value()
            self.range_dic['g0_from'] = self.g0_from_spn.value()
            self.range_dic['r0_from'] = self.r0_from_spn.value()
            self.range_dic['b0_to'] = self.b0_to_spn.value()
            self.range_dic['g0_to'] = self.g0_to_spn.value()
            self.range_dic['r0_to'] = self.r0_to_spn.value()
        if self.range_exe1_chk:
            self.range_dic['b1_from'] = self.b1_from_spn.value()
            self.range_dic['g1_from'] = self.g1_from_spn.value()
            self.range_dic['r1_from'] = self.r1_from_spn.value()
            self.range_dic['b1_to'] = self.b1_to_spn.value()
            self.range_dic['g1_to'] = self.g1_to_spn.value()
            self.range_dic['r1_to'] = self.r1_to_spn.value()
        # INPUT file format
        if self.in_tif_rad.isChecked():
            input = '.tif'
        elif self.in_png_rad.isChecked():
            input = '.png'
        elif self.in_jpg_rad.isChecked():
            input = '.jpg'
        elif self.in_bmp_rad.isChecked():
            input = '.bmp'
        else:
            Exception('"input" unselected!!')
        # OUTPUT file format
        if self.out_tif_rad.isChecked():
            output = '.tif'
        elif self.out_png_rad.isChecked():
            output = '.png'
        elif self.out_jpg_rad.isChecked():
            output = '.jpg'
        elif self.out_bmp_rad.isChecked():
            output = '.bmp'
        else:
            Exception('"output" unselected!!')
        print('Execute image2image_exe.')

        image2image(
            path=self.path1_ent.text(),
            point_exe0=self.point_exe0_chk.isChecked(),
            point_exe1=self.point_exe1_chk.isChecked(),
            range_exe0=self.range_exe0_chk.isChecked(),
            range_exe1=self.range_exe1_chk.isChecked(),
            input=input,
            output=output,
            point_dic=self.point_dic,
            range_dic=self.range_dic,
            imshow=self.imshow_chk.isChecked(),
            q_jpg=self.q_jpg_spn.value()
        )


    def closeEvent(self, e):
        self.saveSettings()

    # Save settings info
    def saveSettings(self):
        # settings = qtc.QSettings('my_python', 'Image_processing_GUI')
        # ---- #
        # tab0 #
        self.settings.setValue('path0', self.path0_ent.text())
        self.settings.setValue('dpi', self.dpi_spn.value())
        self.settings.setValue('format', self.format_cmb.currentText())
        self.settings.setValue('filename', self.filename_ent.text())
        self.settings.setValue('filename0', self.filename0_ent.text())
        self.settings.setValue('filename1', self.filename1_ent.text())
        self.settings.setValue('grayscale', self.grayscale_chk.isChecked())
        self.settings.setValue('page_off', self.page_off_chk.isChecked())
        self.settings.setValue('page_sel0', self.page_sel0_spn.value())
        self.settings.setValue('page_sel1', self.page_sel1_spn.value())
        self.settings.setValue('size_off', self.size_off_chk.isChecked())
        self.settings.setValue('size0', self.size0_spn.value())
        self.settings.setValue('size1', self.size1_spn.value())
        self.settings.setValue('thread', self.thread_spn.value())
        # ---- #
        # tab1 #
        self.settings.setValue('path1', self.path1_ent.text())
        self.settings.setValue('in_tif', self.in_tif_rad.isChecked())
        self.settings.setValue('in_png', self.in_png_rad.isChecked())
        self.settings.setValue('in_jpg', self.in_jpg_rad.isChecked())
        self.settings.setValue('in_bmp', self.in_bmp_rad.isChecked())
        self.settings.setValue('out_tif', self.out_tif_rad.isChecked())
        self.settings.setValue('out_png', self.out_png_rad.isChecked())
        self.settings.setValue('out_jpg', self.out_jpg_rad.isChecked())
        self.settings.setValue('out_bmp', self.out_bmp_rad.isChecked())
        self.settings.setValue('point_exe0', self.point_exe0_chk.isChecked())
        self.settings.setValue('b0', self.b0_spn.value())
        self.settings.setValue('g0', self.g0_spn.value())
        self.settings.setValue('r0', self.r0_spn.value())
        self.settings.setValue('point_exe1', self.point_exe1_chk.isChecked())
        self.settings.setValue('b1', self.b1_spn.value())
        self.settings.setValue('g1', self.g1_spn.value())
        self.settings.setValue('r1', self.r1_spn.value())
        self.settings.setValue('range_exe0', self.range_exe0_chk.isChecked())
        self.settings.setValue('b0_from', self.b0_from_spn.value())
        self.settings.setValue('g0_from', self.g0_from_spn.value())
        self.settings.setValue('r0_from', self.r0_from_spn.value())
        self.settings.setValue('b0_to', self.b0_to_spn.value())
        self.settings.setValue('g0_to', self.g0_to_spn.value())
        self.settings.setValue('r0_to', self.r0_to_spn.value())
        self.settings.setValue('range_exe1', self.range_exe1_chk.isChecked())
        self.settings.setValue('b1_from', self.b1_from_spn.value())
        self.settings.setValue('g1_from', self.g1_from_spn.value())
        self.settings.setValue('r1_from', self.r1_from_spn.value())
        self.settings.setValue('b1_to', self.b1_to_spn.value())
        self.settings.setValue('g1_to', self.g1_to_spn.value())
        self.settings.setValue('r1_to', self.r1_to_spn.value())
        self.settings.setValue('imshow', self.imshow_chk.isChecked())
        self.settings.setValue('q_jpg', self.q_jpg_spn.value())


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())






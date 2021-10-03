"""
def image_output: Outputs image
def pdf2image: Convert a PDF to IMAGEs
def pdf2image_dir: Convert all pdf to image in the dir.
def saveTiffStack: Save multi-frame tiff file
def add_image: Add an img1 to an img0
def add_image_tif: Add an img1 to an img0 (multi-frame TIFF ver.)
def add_image_all: Add all the images to the another
def pdf2png_compare: Execute add_image_all to 2 pdf files
def pdf2tiff_compare: Execute add_image_tif to 2 pdf files
def bmp2png: Convert bmp image to png image

"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import glob
from pdf2image import convert_from_path
import os
import glob
import cv2 as cv


# Global settings -----------------------------------------------------------------
cwd = os.getcwd()

job_dir = 'pdf2image_compare wd'
dpi = 300
filename0 = 'Receipt Excel'
filename1 = 'Receipt Python3'
page_off = True
page_length = 60
separation = 10
grayscale = True

# ---------------------------------------------------------------------------------

def image_output(
        pages: list, outputDir, format='TIFF', filename='output file name'
):
    """
    :param pages: convert_from_path()
    :param outputDir: output file directory
    :param format: TIFF/JPEG/PNG
    :param filename: Select output file name
    :return:
    """
    # JPEG #
    if format == 'JPEG':
        cnt = 0
        for page in pages:
            myfile = outputDir + '/' + filename + '_' + str(cnt) + '.jpg'
            cnt += 1
            page.save(myfile, 'JPEG')
            print('Output: ', myfile)
    # PNG #
    elif format == 'PNG':
        cnt = 0
        for page in pages:
            myfile = outputDir + '/' + filename + '_' + str(cnt) + '.png'
            cnt += 1
            page.save(myfile, 'PNG')
            print('Output: ', myfile)
    # TIFF #
    elif format == 'TIFF':
        myfile = outputDir + '/' + filename + '.tif'
        pages[0].save(myfile, 'TIFF', compression='tiff_deflate', save_all=True, append_images=pages[1:])
        print('Output: ', myfile)


def pdf2image(
    path,
    dpi=300,
    filename='Receipt Python3',
    format='TIFF',
    page_off=False,
    page_length=1,
    separation=10,
    grayscale=False
):
    """
    :param path: PDF file path
    :param dpi: Select resolution
    :param filename: Input filename
    :param format: 'TIFF'/'PNG'/'JPEG'
    :param page_off: True/False. Whether manage pages or not.
    :param page_length: int. False. Convert every pages
    :param separation: Divide all pages into the selected number of pages
    :return:
    """
    # Settings #
    path = path.replace('\\', '/')
    pdf_path = path + '/' + filename + '.pdf'
    # Create ppm dir
    ppmData = path+'/PPM files/'
    if not page_off:
        quotient = page_length // separation
        remainder = page_length % separation
    # Create dir if path does not exist
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)

    # if page_off == True ----------------------------------------------------------
    if page_off:
        print('All pdf pages will be converted')
        # Convert #
        pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData, grayscale=grayscale)
        # Output #
        image_output(pages, path, format, filename)

    # if page_off == False ---------------------------------------------------------
    elif not page_off:
        print('page_length =', page_length)
        # Quotient
        for j in range(quotient):
            # Convert #
            pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData,
                                      first_page=j * separation + 1, last_page=(j + 1) * separation)
            # Output #
            image_output(pages, path, format,
                         filename+'_'+str(j*separation+1)+'_'+str((j+1)*separation))
        # Remainder
        # Convert #
        if remainder != 0:
            pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData,
                                      first_page=j * separation + 1, last_page=(j + 1) * separation + remainder)

            # Output #
            image_output(pages, path, format,
                         filename + '_' + str((j+1) * separation + 1) + '_' + str((j + 1) * separation + remainder))

    else:
        raise Exception('page_length must be int')


def pdf2image_dir(
    path='pdf2image_compare wd',
    dpi=300,
    format='TIFF',
    page_off=True,
    grayscale=False
):
    """
    Convert all pdf to image in the dir.
    :param path: PDF file path
    :param dpi: Select resolution
    :param format: 'TIFF'/'PNG'/'JPEG'
    :param page_off: True/False. Whether manage pages or not.
    """
    # Settings #
    # path = path.replace('\\', '/')
    filelist = os.listdir(path)
    filelist = list(filter(lambda x: x.endswith('.pdf'), filelist))
    # Create ppm dir
    ppmData = path+'/PPM files/'
    # Create dir if path does not exist
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)

    # if page_off == True ----------------------------------------------------------
    if page_off:
        for i in range(len(filelist)):
            print('All pdf pages will be converted')
            # Convert #
            pages = convert_from_path(pdf_path=path+'\\'+filelist[i], dpi=dpi, output_folder=ppmData, grayscale=grayscale)
            # Output #
            image_output(pages, path, format, filelist[i].split('.pdf')[0])

    else:
        raise Exception('Only work when page_off=True')


def saveTiffStack(
        save_path=cwd+'\\saveTiffStack result tiff.tif',
        imgs: 'list' = None
):
    stack = []
    for img in imgs:
        stack.append(Image.fromarray(img))
    stack[0].save(save_path, compression='tiff_deflate', save_all=True, append_images=stack[1:])


def add_image(
        job_dir='pdf2image_compare wd/image/',
        filename0='Receipt Excel',  # pdf, filename0 must be bigger than filename1
        filename1='Receipt Python3', # pdf
        out_filename='add_image result',
):
    """
    Add img1 on img0
    """
    # Read
    img0 = cv.imread(job_dir + filename0 + '.jpg')  # flags=-1: alpha mode
    img1 = cv.imread(job_dir + filename1 + '.jpg')  # flags=-1: alpha mode

    # img0 => img0_r
    img0_r = np.zeros(img0.shape, dtype='uint8')
    img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
    ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # White-out
    img0_r[:, :, :2] = 255  # White BG
    img0_r[:, :, 2] = mask0  # img0 => img0_r

    # I want to put logo on top-left corner, So I create a ROI (Region of Interest)
    rows, cols, channels = img1.shape
    roi = img0_r[0:rows, 0:cols]

    # Now create a mask of img1 and create its inverse mask also
    img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # White-out
    mask_inv = cv.bitwise_not(mask1)

    # White-out the BG in ROI
    img0_bg = cv.bitwise_and(roi, roi, mask=mask1)

    # Take only region of Mask from img1
    img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)

    # Put img1 in ROI and modify the img0
    dst = cv.add(img0_bg, img1_fg)  # ROI
    img0[0:rows, 0:cols] = dst  # Full Image

    # Output
    print('Output: ' + cwd + out_filename)
    cv.imwrite(job_dir + out_filename + '.png', img0)

    # Show
    cv.imshow('Out', img0)
    cv.waitKey(0)

    return img0, img1


def add_image_tif(
        path=cwd,
        filename0='Receipt Excel_gray',  # tiff, !filename0 must be bigger than filename1 (pixel size)
        filename1='Receipt Python3_gray', # tiff
        grayscale=True
):
    path = path.replace('\\', '/')
    """
    Add img1 on img0. img0 is changed to cyan.
    :param path:
    :param filename0:
    :param filename1:
    :param grayscale: True/False
    :return:
    """
    f0_list, f1_list = [], []
    for file in os.listdir(path):
        if file.startswith(filename0) and file.endswith('.tif'):
            f0_list.append(file)
        if file.startswith(filename1) and file.endswith('.tif'):
            f1_list.append(file)

    for f0, f1 in zip(f0_list, f1_list):
        # Output filename
        out_filename = '{} on {}'.format(f1.split('.')[0], f0.split('.')[0])
        # Read (Multi-frame Tiff file)
        ret0, imgs0 = cv.imreadmulti(path + '/' + f0)
        ret1, imgs1 = cv.imreadmulti(path + '/' + f1)
        # Add img1 on img0
        cnt = 0
        for img0, img1 in zip(imgs0, imgs1):

            # img0 => img0_color
            # Convert gray to RGB (img0)
            img0_color = np.zeros((img0.shape[0], img0.shape[1], 3), dtype='uint8')

            if grayscale:
                ret0, mask0 = cv.threshold(img0, 240, 255, cv.THRESH_BINARY)  # white -> out
                ret1, mask1 = cv.threshold(img1, 240, 255, cv.THRESH_BINARY)  # white -> out

                rows, cols = img1.shape

            else:
                img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
                img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # white -> out
                ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # white -> out

                rows, cols, channels = img1.shape

            img0_color[:, :, 0:] = 255  # Black to White
            img0_color[:, :, 0] = mask0  # White to Color  # Color select is here

            # Create a ROI (Region of Interest)
            roi = img0_color[0:rows, 0:cols]

            # White-out the BG in ROI
            img1_on_img0 = cv.bitwise_and(roi, roi, mask=mask1)
            # Turned out to be unnecessary lines
            # img0_bg = cv.bitwise_and(roi, roi, mask=mask1)
            # Take only region of Mask from img1
            # mask_inv = cv.bitwise_not(mask1)
            # img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)
            # Put img1 in ROI and modify the img0
            # dst = cv.add(img0_bg, img1_fg)  # ROI
            # img0[0:rows, 0:cols] = dst  # Full Image
            imgs0[cnt] = img1_on_img0
            cnt += 1

        # Output #
        print('Output: ', path + '\\' + out_filename + '.tif')
        saveTiffStack(save_path=path + '\\' + out_filename + '.tif', imgs=imgs0)


def add_image_all(
    filename0='Receipt Excel',  # pdf, filename0 must be equal/bigger than filename1
    filename1='Receipt Python3', # pdf
    out_filename='add_image_all result',
    job_dir='pdf2image_compare wd/'
):
    """
    Add img1 on img0 (for PNG/JPEG)
    """
    file_dir = job_dir + 'image/'
    file0s, file1s = [], []

    # Split files to file0s and file1s
    for filename in os.listdir(file_dir):
        if filename0 in filename and 'jpg' in filename:
            file0s.append(filename)
        elif filename1 in filename and 'jpg' in filename:
            file1s.append(filename)

    cnt = 0
    for i in range(len(file0s)):

        # Read
        img0 = cv.imread(file_dir + file0s[i])  # flags=-1: alpha mode
        img1 = cv.imread(file_dir + file1s[i])  # flags=-1: alpha mode

        # img0 => img0_r
        img0_r = np.zeros(img0.shape, dtype='uint8')
        img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
        ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # White-out
        img0_r[:, :, :2] = 255  # White BG
        img0_r[:, :, 2] = mask0  # img0 => img0_r

        # I want to put logo on top-left corner, So I create a ROI (Region of Interest)
        rows, cols, channels = img1.shape
        roi = img0_r[0:rows, 0:cols]

        # Now create a mask of img1 and create its inverse mask also
        img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # White-out
        mask_inv = cv.bitwise_not(mask1)

        # White-out the BG in ROI
        img0_bg = cv.bitwise_and(roi, roi, mask=mask1)

        # Take only region of Mask from img1
        img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)

        # Put img1 in ROI and modify the img0
        dst = cv.add(img0_bg, img1_fg)  # ROI
        img0[0:rows, 0:cols] = dst  # Full Image

        # Output
        print('Output: ', cwd + file_dir + out_filename + '_' + str(cnt) + '.png')
        cv.imwrite(job_dir + out_filename + '_' + str(cnt) + '.png', img0)

        cnt += 1


def pdf2png_compare(
        job_dir='pdf2image_compare wd/',
        filename0='Receipt Excel',
        filename1='Receipt Python3',
        page_off=True,
        page_length=1,
        separation=10
):
    """
    Execute add_image_all to 2 pdf files
    """

    # First file #
    pdf2image(path=job_dir + filename0 + '.pdf', outputDir=job_dir, filename=filename0,
              page_off=page_off, page_length=page_length, separation=separation)

    # Second file #
    pdf2image(path=job_dir + filename1 + '.pdf', outputDir=job_dir, filename=filename1,
              page_off=page_off, page_length=page_length, separation=separation)

    # Output #
    add_image_all(filename0=filename0, filename1=filename1, job_dir=job_dir)


def pdf2tiff_compare(
        path='pdf2image_compare wd/',
        filename0='Receipt Excel',
        filename1='Receipt Python3',
        page_off=True,
        page_length=1,
        separation=10,
        grayscale=True,
):
    # First file #
    pdf2image(path=path + filename0 + '.pdf', outputDir=path, filename=filename0, format='TIFF',
              page_off=page_off, page_length=page_length, separation=separation,
              grayscale=grayscale)

    # Second file #
    pdf2image(path=path + filename1 + '.pdf', outputDir=path, filename=filename1, format='TIFF',
              page_off=page_off, page_length=page_length, separation=separation,
              grayscale=grayscale)

    # Output #
    add_image_tif(path=path, filename0=filename0, filename1=filename1, grayscale=grayscale)


def bmp2png(out_dir=''):
    """
    out_dir: output directory name
    """
    cnt = 0
    for img in glob.glob('images/*.bmp'):
        Image.open(img).resize((300,300)).save(os.path.join(out_dir, str(cnt) + '.png'))
        cnt += 1







"""
def image_output: Outputs image
def pdf2image: Convert a PDF to IMAGEs
def saveTiffStack: Save multi-frame tiff file
def add_image: Add an img1 to an img0
def add_image_tif: Add an img1 to an img0 (multi-frame TIFF ver.)
def add_image_all: Add all the images to the another
def pdf2png_compare: Execute add_image_all to 2 pdf files
def pdf2tiff_compare: Execute add_image_tif to 2 pdf files
def bmp2png: Convert bmp image to png image

"""

import numpy as np
from PIL import Image
import glob
from pdf2image import convert_from_path
import os
import cv2 as cv


# Global settings -----------------------------------------------------------------
cwd = os.getcwd()

# ---------------------------------------------------------------------------------

def image_output(
        pages=[], outputDir='', format='TIFF', filename='output file name'
):
    """
    :param pages:
    :param outputDir:
    :param format:
    :param filename: Select output file name
    :return:
    """
    if format == 'JPEG':
        # JPEG #
        cnt = 0
        for page in pages:
            myfile = outputDir + filename + str(cnt) + '.jpg'
            cnt += 1
            page.save(myfile, 'JPEG')
            print('Output: ', myfile)
    elif format == 'TIFF':
        # TIFF #
        myfile = outputDir + filename + '.tif'
        pages[0].save(myfile, 'TIFF', compression='tiff_deflate', save_all=True, append_images=pages[1:])
        print('Output: ', myfile)


def pdf2image(
    path='pdf2image_compare wd/Receipt Python3.pdf',
    dpi=300,
    outputDir='pdf2image_compare wd/',
    filename='Receipt Python3',
    format='TIFF',
    page_length=2,
    separation=10,
    page_select=False
):
    """
    :param path: PDF file path
    :param dpi: Select resolution
    :param outputDir: Output directory name
    :param filename: Input filename
    :param format: 'TIFF' or 'JPEG'
    :param page_length: int/'select'/False. False: Convert every pages
    :param separation: Divide all pages into the selected number of pages
    :param page_select: []. Select necessary pages.
    odd: first_page, even: last_pages. e.g. [1,2, 4,6, 9,9]
    :return:
    """
    # Settings #
    ppmData = outputDir+'PPM files/'
    quotient = page_length // separation
    remainder = page_length % separation

    # Create dir if path does not exist
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)

    # if page_length unselected -----------------------------------------------------
    if page_length == False:

        if page_select == False:
            page_select = [1, page_length]
            print('All pdf pages will be converted')

        # Convert #
        pages = []
        for i in range(len(page_select)//2):
            print(i)
            pages.extend(convert_from_path(pdf_path=path, dpi=dpi, output_folder=ppmData,
                                               first_page=page_select[i*2], last_page=page_select[i*2+1]))

        # Output #
        image_output(pages, outputDir, format, filename)

    # if page_length = int ---------------------------------------------------------
    elif type(page_length) == int:
        print('page_length =', page_length)

        # Quotient
        for j in range(quotient):

            # Convert #
            pages = convert_from_path(pdf_path=path, dpi=dpi, output_folder=ppmData,
                                      first_page=j * separation + 1, last_page=(j + 1) * separation)

            # Output #
            image_output(pages, outputDir, format,
                         filename+'_'+str(j*separation+1)+'_'+str((j+1)*separation))

        # Remainder
        # Convert #
        if remainder != 0:
            pages = convert_from_path(pdf_path=path, dpi=dpi, output_folder=ppmData,
                                      first_page=j * separation + 1, last_page=(j + 1) * separation + remainder)

            # Output #
            image_output(pages, outputDir, format,
                         filename + '_' + str((j+1) * separation + 1) + '_' + str((j + 1) * separation + remainder))

    else:
        raise Exception('page_length must be int/False')


def saveTiffStack(
        save_path='pdf2image_compare wd/saveTiffStack result tiff.tif',
        imgs=[np.array([])]
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
        job_dir='pdf2image_compare wd/',
        filename0='Receipt Excel',  # pdf, filename0 must be bigger than filename1
        filename1='Receipt Python3', # pdf
):
    """
    Add img1 on img0
    """
    f0_list, f1_list = [], []
    for file in os.listdir(cwd + '\\pdf2image_compare wd'):
        if file.startswith(filename0) and file.endswith('.tif'):
            f0_list.append(file)
        if file.startswith(filename1) and file.endswith('.tif'):
            f1_list.append(file)


    for f0, f1 in zip(f0_list, f1_list):

        out_filename = '{} on {}'.format(f1.split('.')[0], f0.split('.')[0])

        # Read (Multi-frame Tiff file) #
        ret0, imgs0 = cv.imreadmulti(job_dir + f0)
        ret1, imgs1 = cv.imreadmulti(job_dir + f1)

        cnt = 0
        for img0, img1 in zip(imgs0, imgs1):

            # img0 => img0_r #
            img0_b = np.zeros(img0.shape, dtype='uint8')
            img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
            ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # White-out
            img0_b[:, :, 0:] = 255  # White BG
            img0_b[:, :, 0] = mask0  # img0 => img0_b

            # I want to put logo on top-left corner, So I create a ROI (Region of Interest) #
            rows, cols, channels = img1.shape
            roi = img0_b[0:rows, 0:cols]

            # Now create a mask of img1 and create its inverse mask also #
            img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # White-out
            mask_inv = cv.bitwise_not(mask1)

            # White-out the BG in ROI #
            img0_bg = cv.bitwise_and(roi, roi, mask=mask1)

            # Take only region of Mask from img1 #
            img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)

            # Put img1 in ROI and modify the img0 #
            dst = cv.add(img0_bg, img1_fg)  # ROI
            img0[0:rows, 0:cols] = dst  # Full Image
            imgs0[cnt] = img0

            cnt += 1

        # Output #
        print('Output: ', cwd + job_dir + out_filename + '.tif')
        saveTiffStack(save_path=job_dir + out_filename + '.tif', imgs=imgs0)


def add_image_all(
    filename0='Receipt Excel',  # pdf, filename0 must be equal/bigger than filename1
    filename1='Receipt Python3', # pdf
    out_filename='add_image_all result',
    job_dir='pdf2image_compare wd/'
):
    """
    Add img1 on img0
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
        page_length=False,
        separation=10
):
    """
    Execute add_image_all to 2 pdf files
    """
    file_dir = 'pdf2image_compare wd/image/'

    # First file #
    pdf2image(path=job_dir + filename0 + '.pdf', outputDir=file_dir, filename=filename0,
              page_length=page_length, separation=separation)

    # Second file #
    pdf2image(path=job_dir + filename1 + '.pdf', outputDir=file_dir, filename=filename1)

    # Output #
    add_image_all(filename0=filename0, filename1=filename1, job_dir=job_dir)


def pdf2tiff_compare(
        job_dir='pdf2image_compare wd/',
        filename0='Receipt Excel',
        filename1='Receipt Python3',
        page_length=False
):
    # First file #
    pdf2image(path=job_dir + filename0 + '.pdf', outputDir=job_dir, filename=filename0, format='TIFF',
              page_length=page_length)

    # Second file #
    pdf2image(path=job_dir + filename1 + '.pdf', outputDir=job_dir, filename=filename1, format='TIFF')

    # Output #
    add_image_tif(job_dir=job_dir, filename0=filename0, filename1=filename1)


def bmp2png(out_dir=''):
    """
    out_dir: output directory name
    """
    cnt = 0
    for img in glob.glob('images/*.bmp'):
        Image.open(img).resize((300,300)).save(os.path.join(out_dir, str(cnt) + '.png'))
        cnt += 1







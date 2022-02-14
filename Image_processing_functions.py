"""
2021/12/31 Properties: size/page_sel were added (pdf2image).
2022/01/02 image2image launched.
2022/01/04 imshow added (image2image).
2022/01/08 "q_jpg" added (image2image).
2022/02/12 Upper letter format enabled (e.g. PNG).
NEXT...

def image_output: Outputs image. Works in .tif/.png/.jpg.
def pdf2image: Convert a PDF to IMAGEs. Works in .tif/.png/.jpg.
def pdf2image_dir: Convert all pdf to image in the dir. Works in .tif/.png/.jpg.
def saveTiffStack: Save multi-frame tiff file.
def add_image: Add an img1 to an img0. Works in .png/.jpg.
def add_image_tif: Add an img1 to an img0 (multi-frame TIFF ver.).
def add_BefAft: Add an img1 to an img0 (Add Before/After with different color). Only works in .tif.
def image2pdf: Convert image to pdf file.
def image2image: Convert images to images. Works in .tif/.png/.jpg/.bmp.
"""
import inspect
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import img2pdf
import os
import glob
import cv2 as cv
import matplotlib.pyplot as plt
from time import gmtime, strftime

# Global settings -----------------------------------------------------------------
path = r'C:\Users\A\Desktop\pythonProject\opencvProject\pdf2imageProject'
dpi = 100
filename = 'Receipt Python3'
filename0 = 'Receipt Python3'
filename1 = 'Receipt Excel'
out_filename = '{}on{}'.format(filename1, filename0)
format = '.tif'
page_off = False  # True: All pdf pages will be converted.
page_sel = [1, 2]  # Select pages you want to convert. From list[0] to list[1]. Same page may not be selected.
grayscale = True  # Convert pdf file to grayscale image
size = None  # (xx, xx), Image size converted from pdf file
coloring = 0  # Color select for add_image()/add_image_tif()
# ---------------------------------------------------------------------------------

def image_output(
        pages: list, outputDir: str, format='.tif', filename='output file name'
):
    """
    :param pages: convert_from_path()
    :param outputDir: output file directory
    :param format: .tif/.jpg/.png
    :param filename: Select output file name
    """
    print('Execute image_output().', 'Output file format is', format)
    # JPEG #
    if format == '.jpg':
        print('format = .jpg')
        cnt = 0
        for page in pages:
            myfile = outputDir + '/' + filename + '_' + str(cnt) + format
            cnt += 1
            page.save(myfile, 'JPEG')
            print('Output: ', myfile)
    # PNG #
    elif format == '.png':
        print('format = .png')
        cnt = 0
        for page in pages:
            myfile = outputDir + '/' + filename + '_' + str(cnt) + format
            cnt += 1
            newdata = []
            data_pcs = page.getdata()
            for data in data_pcs:
                if data[0] == 255 and data[1] == 255 and data[2] == 255:  # finding White color by its RGB value
                    # Sorting a transparent value when you find a White color.
                    newdata.append((255, 255, 255, 0))
                # Other colors remain unchanged.
                else:
                    newdata.append(data)
            data_pcs.putdata(newdata)
            page.save(myfile, 'PNG', transparent=0)
            print('Output: ', myfile)
    # TIFF #
    elif format == '.tif':
        print('format = .tif')
        myfile = outputDir + '/' + filename + '.tif'
        # Only 1 page
        if len(pages) == 1:
            print('len(pages) == 1')
            pages[0].save(myfile, 'TIFF', compression='tiff_deflate')
        # More than 2 pages
        elif len(pages) > 1:
            print('len(pages) =', len(pages))
            pages[0].save(myfile, 'TIFF', compression='tiff_deflate', save_all=True, append_images=pages[1:])
        print('Output: ', myfile)
    print('image_output() done!!')


def pdf2image(
    path=path,
    dpi=300,
    filename='Receipt Python3',
    format='.tif',
    page_off=True,
    page_sel=[1, 2],
    size=None,
    grayscale=False,
    thread_count=1,
):
    """
    :param path: PDF file path
    :param dpi: Select resolution
    :param filename: Input filename
    :param format: '.tif'/'.png'/'.jpg'
    :param page_off: True/False. True: All pdf pages will be converted.
    :param page_sel: list. page-select. Selected pages will be converted. Same page may not be selected.
    :param size: Converted image size. Must be (xx, xx).
    :param grayscale: Convert pdf file to grayscale image
    """
    print('Execute pdf2image()', '\ninspect.signature(pdf2image):\n', inspect.signature(pdf2image))

    # Settings #
    path = path.replace('\\', '/')
    pdf_path = path + '/' + filename + '.pdf'
    # Create ppm dir
    ppmData = path+'/PPM files/'
    # Create dir if path does not exist
    if not os.path.exists(path):
        os.mkdir(path)
        print(path, 'created')
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)
        print(ppmData, 'created')
    # if page_off == True ----------------------------------------------------------
    # (All pdf pages will be converted)
    if page_off:
        print('All pdf pages will be converted')
        # Convert #
        pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData,
                                  grayscale=grayscale, size=size, thread_count=thread_count)
        # Output #
        image_output(pages, path, format, filename)

    # if page_off == False ---------------------------------------------------------
    elif not page_off:
        print('page_off = False selected. page_sel =', page_sel)
        cnt = 0
        # Convert #
        print('page_sel[cnt] != page_sel[cnt+1]. Execute page-select mode.')
        pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData,
                                  grayscale=grayscale, size=size,
                                  first_page=page_sel[cnt], last_page=page_sel[cnt+1])
        # Output #
        image_output(pages, path, format,
                     filename+'_'+str(page_sel[cnt])+'-'+str(page_sel[cnt+1]))
    else:
        raise Exception('page_off must be boolean')
    print('pdf2image() done!!')


def pdf2image_dir(
    path: str,
    dpi=300,
    format='.tif',
    page_off=True,
    grayscale=False
):
    """
    Convert all pdf to image in the dir.
    :param path: PDF file path
    :param dpi: Select resolution
    :param format: '.tif'/'.png'/'.jpg'
    :param page_off: True/False. Whether manage pages or not.
    """
    print('Execute pdf2image_dir()', '\ninspect.signature(pdf2image_dir):\n', inspect.signature(pdf2image_dir))
    # Settings #
    # path = path.replace('\\', '/')
    filelist = os.listdir(path)
    filelist = list(filter(lambda x: x.endswith('.pdf'), filelist))
    # Create ppm dir
    ppmData = path+'/PPM files/'
    # Create dir if path does not exist
    if not os.path.exists(path):
        os.mkdir(path)
        print(path, 'created')
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)
        print(ppmData, 'created')

    # if page_off == True ----------------------------------------------------------
    print('page_off = True')
    if page_off:
        for f in filelist:
            print('All pdf pages will be converted')
            # Convert #
            pages = convert_from_path(pdf_path=path+'\\'+f, dpi=dpi, output_folder=ppmData, grayscale=grayscale)
            # Output #
            image_output(pages, path, format, f.split('.pdf')[0])
        print('image_output() done!!')

    else:
        raise Exception('Only works when page_off=True')


def saveTiffStack(
        save_path: str,
        imgs: 'list'
):
    print('Execute saveTiffStack().', '\ninspect.signature(saveTiffStack):\n', inspect.signature(saveTiffStack))
    stack = []
    for img in imgs:
        stack.append(Image.fromarray(img))
    stack[0].save(save_path, compression='tiff_deflate', save_all=True, append_images=stack[1:])
    print('saveTiffStack() done!!')


def add_image(
        path: str,
        filename0='Receipt Excel',  # pdf, filename_t must be bigger than filename1
        filename1='Receipt Python3', # pdf
        format=format,
        coloring=0
):
    """
    Add img1 on img0
    """
    print('Execute add_image()', '\ninspect.signature(add_image):\n', inspect.signature(add_image))
    path = path.replace('\\', '/')
    # Create .tif name
    f0 = filename0 + format
    f1 = filename1 + format
    # Output filename
    out_filename = '{}on{}'.format(filename1, filename0)
    print('out_filename will be ->', out_filename)
    # Read (Multi-frame Tiff file)
    # Imported image will be BGR (shape = (xx, xx, xx))
    ret0, img0 = cv.imread(path + '/' + f0)
    ret1, img1 = cv.imread(path + '/' + f1)
    # Add img1 on img0
    print('\nimg0', img0.shape, '\nimg1', img1.shape)
    # Create an roi (Region of Interest)
    # img0 => roi. Convert gray to RGB (if grayscale selected)
    roi = np.zeros((img0.shape[0], img0.shape[1], 3), dtype='uint8')  # All Black(0)

    if grayscale:
        print('grayscale = True')
        # Threshold select for transparent region
        ret0, mask0 = cv.threshold(img0, 240, 255, cv.THRESH_BINARY)  # white -> out
        ret1, mask1 = cv.threshold(img1, 240, 255, cv.THRESH_BINARY)  # white -> out
        # Error handling. In case of color image input.
        if len(img1.shape) == 2:
            rows, cols = img1.shape
        else:
            print('** Something is wrong with img1.shape!! Select grayscale unchecked. **')
    else:
        # Error handling. In case of gray image input.
        if len(img1.shape) == 3:
            img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
            img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # white -> out
            ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # white -> out
            rows, cols, channels = img1.shape
        else:
            print('Something is wrong with img1.shape!! Select grayscale checked')

    # Background Color (0) to White (255)
    roi[:, :, :] = 255
    # White to Color (mask region only)  # Color select is here
    roi[:, :, coloring] = mask0  # 0:yellow/1:magenta/2:cyan
    # White-out the BG in ROI
    img1_on_img0 = cv.bitwise_and(roi, roi, mask=mask1)

    # OUTPUT
    print('Output:', path + '/' + out_filename + format)
    cv.imwrite(path + '/' + out_filename + format, img1_on_img0)
    print('add_image() done!!')


def add_image_tif(
        path: str,
        filename0=filename0,  # tiff, filename0 must be bigger than filename1 (pixel size)
        filename1=filename1, # tiff
        grayscale=True,
        coloring=0
):
    """
    Add img1 on img0. img0 is changed to color:cyan.
    :param path: Working directory.
    :param filename0:
    :param filename1:
    :param grayscale: True/False. True if input image is.
    :param coloring: Coloring to appeal difference. 0:blue/1:green/2:red.
    :return: imgs0
    """
    print('Execute add_image_tif().', '\ninspect.signature(add_image_tif):\n', inspect.signature(add_image_tif))
    path = path.replace('\\', '/')
    # Create .tif name
    f0 = filename0 + '.tif'
    f1 = filename1 + '.tif'
    # Output filename
    out_filename = '{}on{}'.format(filename1, filename0)
    print('out_filename will be ->', out_filename)
    # Read (Multi-frame Tiff file)
    # Imported image will be BGR (shape = (xx, xx, xx))
    ret0, imgs0 = cv.imreadmulti(path + '/' + f0)
    ret1, imgs1 = cv.imreadmulti(path + '/' + f1)
    # Add img1 on img0
    cnt = 0
    for img0, img1 in zip(imgs0, imgs1):
        print('page', str(cnt) + '\nimg0', img0.shape, '\nimg1', img1.shape)
        # Create an roi (Region of Interest)
        # img0 => roi. Convert gray to RGB (if grayscale selected)
        roi = np.zeros((img0.shape[0], img0.shape[1], 3), dtype='uint8')  # All Black(0)

        if grayscale:
            print('grayscale = True')
            # Threshold select for transparent region
            ret0, mask0 = cv.threshold(img0, 240, 255, cv.THRESH_BINARY)  # white -> out
            ret1, mask1 = cv.threshold(img1, 240, 255, cv.THRESH_BINARY)  # white -> out
            # Error handling. In case of color image input.
            if len(img1.shape) == 2:
                rows, cols = img1.shape
            else:
                print('** Something is wrong with img1.shape!! Select grayscale unchecked. **')
        else:
            # Error handling. In case of gray image input.
            if len(img1.shape) == 3:
                img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
                img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # white -> out
                ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # white -> out
                rows, cols, channels = img1.shape
            else:
                print('Something is wrong with img1.shape!! Select grayscale checked')

        # Background Color (0) to White (255)
        roi[:, :, 0:] = 255
        # White to Color (mask region only)  # Color select is here
        roi[:, :, coloring] = mask0  # 0:yellow/1:magenta/2:cyan
        # White-out the BG in ROI
        img1_on_img0 = cv.bitwise_and(roi, roi, mask=mask1)
        # Turned out to be unnecessary lines ---------------
        # img0_bg = cv.bitwise_and(roi, roi, mask=mask1)
        # Take only region of Mask from img1
        # mask_inv = cv.bitwise_not(mask1)
        # img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)
        # Put img1 in ROI and modify the img0
        # dst = cv.add(img0_bg, img1_fg)  # ROI
        # img0[0:rows, 0:cols] = dst  # Full Image
        # --------------------------------------------------
        imgs0[cnt] = img1_on_img0
        cnt += 1

    # Output #
    print('Output: ', path + '/' + out_filename + '.tif')
    saveTiffStack(save_path=path + '/' + out_filename + '.tif', imgs=imgs0)
    print('add_image_tiff() done!!')


def add_BefAft(
        path: str,
        filename0=filename0,  # tif, !filename0 must be bigger than filename1 (pixel size)
        filename1=filename1,  # tif
):
    print('Execute add_BefAft()', '\ninspect.signature(add_BefAft):\n', inspect.signature(add_BefAft))
    path = path.replace('\\', '/')
    print('Execute add_image_tif() #1 : filename1 on filename0')
    add_image_tif(path=path,
                  filename0=filename0,  # tiff, !filename0 must be bigger than filename1 (pixel size)
                  filename1=filename1,  # tiff
                  coloring=2  # 2:cyan
    )
    print('Execute add_image_tif() #2 : filename0 on filename1')
    add_image_tif(path=path,
                  filename0=filename1,  # tiff, !filename0 must be bigger than filename1 (pixel size)
                  filename1=filename0,  # tiff
                  coloring=1  # 1:magenta
    )
    # Create .tif name
    f0 = '{}on{}.tif'.format(filename0, filename1)
    f1 = '{}on{}.tif'.format(filename1, filename0)
    # Read (Multi-frame Tiff file)
    ret0, imgs0 = cv.imreadmulti(path + '/' + f0)  #BGR
    ret1, imgs1 = cv.imreadmulti(path + '/' + f1)  #BGR
    # Add img1 on img0
    cnt = 0
    for img0, img1 in zip(imgs0, imgs1):
        print('page', str(cnt) + '\nimg0', img0.shape, '\nimg1', img1.shape)
        # img0 => img_colored(Convert gray to RGB. Blank image for now.)
        # img_colored = np.zeros((img0.shape[0], img0.shape[1], 3), dtype='int32')  # All Black(0)
        # Extract img0_only/img1_only
        # img1_only = np.where(np.all(imgs0[cnt] == (255, 255, 0), -1), 0, 255)
        # img0_only = np.where(np.all(imgs1[cnt] == (255, 255, 0), -1), 0, 255)

        # Add img1 on img0
        img1_on_img0 = cv.add(img0, img1)
        imgs0[cnt] = img1_on_img0
        cnt += 1

    # Output #
    print('Output: ', path + '/' + f0.split('.')[0] + '_final.tif')
    saveTiffStack(save_path=path + '/' + f0.split('.')[0] + '_final.tif', imgs=imgs0)
    print('add_BefAft() done!!')


def image2pdf(
        path: str,
        filename='Receipt Python3',
        format='.tif',
        img_folder=None
):
    pdf_FileName = path + "\\temp\\output.pdf" # 出力するPDFの名前
    png_Folder = path + "\\temp\\" # 画像フォルダ
    extension  = ".tif" # 拡張子がPNGのものを対象

    with open(pdf_FileName, "wb") as f:  # w: write, b: binary
        # 画像フォルダの中にある画像ファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(img_folder+j).filename for j in os.listdir(img_folder)if j.endswith(format)]))
        # 選択した画像ファイルをバイナリ形式でpdfファイルに書き込む
        f.write(img2pdf.convert(path + filename + format))


###########################################################################################################
###########################################################################################################

# matplot show
def matplot(img):
    # BGR to RGB
    if img.shape[2] == 3:
        mtplt = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    # BGRA to RGBA
    if img.shape[2] == 4:
        mtplt = cv.cvtColor(img, cv.COLOR_BGRA2RGBA)
    plt.figure(figsize=(8, 8))
    plt.imshow(mtplt)


# Mask image for making transparent image
def mask_image(img, b_from, g_from, r_from, b_to, g_to, r_to):
    # Threshold select
    color_lower = np.array([b_from, g_from, r_from, 255])
    color_upper = np.array([b_to, g_to, r_to, 255])
    # Create a mask for threshold color
    img_mask = cv.inRange(img, color_lower, color_upper)
    # Masked array to 0
    masked = cv.bitwise_not(img, img, mask=img_mask)
    return masked


def image2image(
        path=r'C:\Users\A\Desktop\pythonProject\opencvProject\image\temp',
        point_exe0=False,
        point_exe1=False,
        range_exe0=False,
        range_exe1=False,
        input='.bmp',
        output='.jpg',
        point_dic={'b0': 255, 'g0': 255, 'r0': 255,
                    'b1': 255, 'g1': 255, 'r1': 255,
                   },
        range_dic = {'b0_from': 255, 'g0_from': 255, 'r0_from': 255, 'b1_from': 255, 'g1_from': 255, 'r1_from': 255,
                     'b2_from': 255, 'g2_from': 255, 'r2_from': 255, 'b0_to': 255, 'g0_to': 255, 'r0_to': 255,
                     'b1_to': 255, 'g1_to': 255, 'r1_to': 255, 'b2_to': 255, 'g2_to': 255, 'r2_to': 255,
                     },
        imshow=True,
        q_jpg=100
):
    """
    path: Image path.
    point_exe0: True -> Execute point exclusion. Selected pixels will be transparent.
    point_exe1: True -> Execute point exclusion. Selected pixels will be transparent. Must be selected after point_exe0.
    range_exe0: True -> Execute range exclusion. Selected pixels will be transparent.
    range_exe1: True -> Execute range exclusion. Selected pixels will be transparent. Must be selected after point_exe0.
    input: Input image file format. .tif/.png/.jpg/.bmp
    output: Output image file format. .tif/.png/.jpg/.bmp
    point_dic: Variables that will be used in image conversion.
    range_dic: Variables that will be used in mask_image().
    imshow: Whether to show image or not. True -> Show image.
    q_jpg: Property for IMWRITE_JPEG_QUALITY. int: 1 - 100.
    """
    print('Execute image2image()', '\ninspect.signature(image2image):\n', inspect.signature(image2image))
    print('point_dic:\n', point_dic, '\nrange_dic:\n', range_dic)
    # SETTINGS #
    path = path.replace('\\', '/')
    # Job directory
    filelist = os.listdir(path)
    print('filelist:', filelist)
    # FILTERING #
    filtered = list(filter(lambda x: x.endswith(input), filelist))
    filtered.extend(list(filter(lambda x: x.endswith(input.upper()), filelist)))
    filelist = filtered
    print('filelist(filtered):', filelist)
    # Error handling
    if len(filelist) == 0:
        Exception('No files in filelist.')

    # OUTPUT #
    # Make image transparent
    if output == '.PNG' or output == '.png' or output == '.TIF' or output == '.tif':
        for f in filelist:
            img = cv.imread(path + '/' + f)
            # Add alpha channel to RGB
            print('img.shape:', img.shape)
            # BGR to BGRA
            if img.shape[2] == 3:
                print('img.shape[2] == 3. Convert BGR to BGRA.')
                img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
            elif img.shape[2] == 4:
                print('img.shape: ', img.shape)
            # Convert to transparent
            # point_exe0 (1st) #
            if point_exe0:
                print('point_exe0 = True.')
                img[:, :, 3] = np.where(np.all(img == (point_dic['b0'], point_dic['g0'], point_dic['r0']),
                                               axis=-1), 0, 255)  # 0: transparent, 255: opaque
                # point_exe1 (2nd) #
                if point_exe1:
                    print('point_exe1 = True.')
                    img[:, :, 3] = np.where(np.all(img == (point_dic['b1'], point_dic['g1'], point_dic['r1']),
                                                   axis=-1), 0, 255)  # 0: transparent, 255: opaque
            # range_exe0 (1st) #
            if range_exe0:
                print('range_exe0 = True.')
                img = mask_image(img,
                                 range_dic['b0_from'], range_dic['g0_from'], range_dic['r0_from'],
                                 range_dic['b0_to'], range_dic['g0_to'], range_dic['r0_to'],
                                 )
                # range_exe1 (2nd) #
                if range_exe1:
                    print('range_exe1 = True.')
                    img = mask_image(img,
                                     range_dic['b1_from'], range_dic['g1_from'], range_dic['r1_from'],
                                     range_dic['b1_to'], range_dic['g1_to'], range_dic['r1_to'],
                                     )
            # SAVE #
            cv.imwrite(path + '/' + f.split('.')[0] + '_' + strftime('%H%M%S') + output, img)
            print('cv.imwrite() done!! Output:', path + '/' + f.split('.')[0] + output)

    elif output == '.JPG' or output == '.jpg':
        for f in filelist:
            img = cv.imread(path + '/' + f)
            print('img.shape: ', img.shape)
            # SAVE #
            cv.imwrite(path + '/' + f.split('.')[0] + '_' + strftime('%H%M%S') + output, img, [cv.IMWRITE_JPEG_QUALITY, q_jpg])
            print('cv.imwrite() done!! Output:', path + '/' + f.split('.')[0] + output)

    elif output == '.BMP' or output == '.bmp':
        for f in filelist:
            img = cv.imread(path + '/' + f)
            print('img.shape: ', img.shape)
            # SAVE #
            cv.imwrite(path + '/' + f.split('.')[0] + '_' + strftime('%H%M%S') + output, img)
            print('cv.imwrite() done!! Output:', path + '/' + f.split('.')[0] + output)
    else:
        Exception('Error!! Output must be .tif/.png/.jpg/.bmp.')

    print('image2image() done!!')
    # SHOW #
    if imshow:
        matplot(img)



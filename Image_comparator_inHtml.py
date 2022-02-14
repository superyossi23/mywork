"""
Display all the image file in a directory. 1/2/3/4 columns ver. is currently available.
2022/02/02 Feature: <bgcolor> and <font size> and <font color> added.
2022/02/11 Format reorganized (Paragraph added). natsort added.
"""

from webbrowser import open_new_tab
import os
import sys
from natsort import natsorted
from htmlModule import *


# SETTINGS -----------------------------------------------------
wd = r'D:\stock_data'
col_num = 2
format = '.png'
filename = 'IMG_'  # (SORTING)

filelist = os.listdir(wd)  # Work file directory
filelist = list(filter(lambda x: x.endswith(format), filelist))  # Work file
img_dir = wd.split('\\')[-1]
path_select = '.'  # Output file directory. Absolute path ver.
out_filename = img_dir + '.html'  # Output file name
tab_name = img_dir  # Tab name for html file
# --------------------------------------------------------------

# SORTING
# print('Execute SORTING!!')
# filedict = sort_filelist(filelist, filename)
# print('\nfiledict:\n', filedict)
# filelist = sorted(filedict.values(), key=lambda x:x[0])

# natsort
filelist = natsorted(filelist)
# --------------------------------------------------------------
print('\nfilelist:\n', filelist)

# How to read html base file
# temp_wrapper = 'temp_wrapper.html'
# htmlFile = open(temp_wrapper, 'r', encoding='UTF-8')
# base = htmlFile.read()
base = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>%s</title>
    <style>
      table {
      table-layout: fixed;
      }
      table td {
      border: 3px solid #555555;
      padding-left: .5em;
      padding-right: .5em;
      }
    </style>
  </head>
  <body>
    <table border="1">
    </table>
  </body>
</html>
"""

body = ''
# 1 COLUMNS VER. -----------------------------------------------------------
if col_num == 1:
    # Repeat pattern
    wrapper = """
    <tr>
      <td bgcolor="ffffff">
        <font size="4">%s<br></font>
        <img src=%s>
      </td>
    </tr>
    """
    # Add wrapper (str) to <body>
    for i in range(len(filelist)):
        body = body + wrapper
    # Insert content between <table> and </table>
    index = base.find('</table>')
    base = base[:index] + body + base[index:]

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f in filelist:
        wrap_info.append(
        '''
        <!p1><font color='black'><br></font>
        <!p2><br>
        ''' + f)  # Title (%s)
        # Path select: Absolute or Relative
        # Path = Absolute
        wrap_info.append(path_select + '/' + img_dir + '/' + f)  # Image (%s)
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)
    print('\nwrap_info:\n', wrap_info)

# 2 COLUMNS VER. -----------------------------------------------------------
if col_num == 2:
    # Repeat pattern
    wrapper = """
    <tr>
      <td bgcolor="ffffff">
        <font size="4">%s<br></font>
        <img src=%s>
      </td>
      <td bgcolor="ffffff">
        <font size="4">%s<br></font>
        <img src=%s>
      </td>
    </tr>
    """
    # In the case of 1 column missing
    if len(filelist)%2 == 1:
        filelist.append('None')
    # Add wrapper (str) to <body>
    for i in range(len(filelist)//2):
        body = body + wrapper
    # Insert content between <table> and </table>
    index = base.find('</table>')
    base = base[:index] + body + base[index:]

    # Divide filelist into 2 filelists
    ## Upper/Lower ##
    # filelist0 = filelist[:len(filelist)//2]
    # filelist1 = filelist[len(filelist)//2:]
    ## Odd/Even ##
    filelist0, filelist1 = get_oddeven(filelist)
    print('\nfilelist0:\n', filelist0, '\nfilelist1:\n', filelist1)

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f0,f1 in zip(filelist0, filelist1):
        wrap_info.append(
        '''
        <!p1><font color='black'><br></font>
        <!p2><br>
        ''' + f0)  # Title (%s)
        # Path: Absolute or Relative
        # Path = Absolute
        wrap_info.append(path_select + '/' + img_dir + '/' + f0)  # Image
        wrap_info.append(
        '''
        <!p1><font color='black'><br></font>
        <!p2><br>
        ''' + f1)  # Title (%s)
        wrap_info.append(path_select + '/' + img_dir + '/' + f1)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)
    print('\nwrap_info:\n', wrap_info)

# 3 COLUMNS VER. -----------------------------------------------------------
elif col_num == 3:
    # Repeat pattern
    wrapper = """
    <tr>
      <td bgcolor="ffffff">
        <font size="4">%s<br></font>
        <img src=%s>
      </td>
      <td bgcolor="ffffff">
        <font size="4">%s<<br></font>
        <img src=%s>
      </td>
      <td bgcolor="ffffff">
        <font size="4">%s<<br></font>
        <img src=%s>
      </td>
    </tr>
    """
    # In the case of 1 column missing
    if len(filelist) % 3 == 1:
        filelist.append('None')
        filelist.append('None')
    # In the case of 2 column missing
    elif len(filelist) % 3 == 2:
        filelist.append('None')
    # Add wrapper (str) to <body>
    for i in range(len(filelist)//3):
        body = body + wrapper
    # Insert content to <table>
    index = base.find('</table>')
    base = base[:index] + body + base[index:]

    # Divide filelist into 3 filelists
    ## Upper/Middle/Lower ##
    # filelist0 = filelist[:len(filelist) * 1 // 3]
    # filelist1 = filelist[len(filelist) * 1 // 3:len(filelist) * 2 // 3]
    # filelist2 = filelist[len(filelist) * 2 // 3:]
    ## Left/Center/Right ##
    filelist0, filelist1, filelist2 = get_LCR(filelist)
    print('\nfilelist0:\n', filelist0, '\nfilelist1:\n', filelist1, '\nfilelist2:\n', filelist2)

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f0,f1,f2 in zip(filelist0, filelist1, filelist2):
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f0)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f0)  # Image
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f1)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f1)  # Image
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f2)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f2)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)
    print('\nwrap_info:\n', wrap_info)

# 3 COLUMNS VER. -----------------------------------------------------------
elif col_num == 4:
    # Repeat pattern
    wrapper = """
    <tr>
      <td bgcolor="ffffff">
        <font size="4">%s<br></font>
        <img src=%s>
      </td>
      <td bgcolor="ffffff">
        <font size="4">%s<<br></font>
        <img src=%s>
      </td>
      <td bgcolor="ffffff">
        <font size="4">%s<<br></font>
        <img src=%s>
      </td>
      <td bgcolor="ffffff">
        <font size="4">%s<<br></font>
        <img src=%s>
      </td>
    </tr>
    """
    # In the case of 1 column missing
    if len(filelist) % 4 == 1:
        filelist.append('None')
        filelist.append('None')
        filelist.append('None')
    # In the case of 2 column missing
    elif len(filelist) % 4 == 2:
        filelist.append('None')
        filelist.append('None')
        # In the case of 1 column missing
    elif len(filelist) % 4 == 3:
        filelist.append('None')
    # Add wrapper (str) to <body>
    for i in range(len(filelist)//4):
        body = body + wrapper
    # Insert content to <table>
    index = base.find('</table>')
    base = base[:index] + body + base[index:]

    # Divide filelist into 3 filelists
    # Upper/Middle/Lower
    filelist0 = filelist[:len(filelist) * 1 // 4]
    filelist1 = filelist[len(filelist) * 1 // 4:len(filelist) * 2 // 4]
    filelist2 = filelist[len(filelist) * 2 // 4:len(filelist) * 3 // 4]
    filelist3 = filelist[len(filelist) * 3 // 4:]
    ## LL/L/R/RR ##
    filelist0, filelist1, filelist2, filelist3 = get_LLRR(filelist)
    print('\nfilelist0:\n', filelist0, '\nfilelist1:\n', filelist1, '\nfilelist2:\n', filelist2)

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f0,f1,f2,f3 in zip(filelist0, filelist1, filelist2, filelist3):
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f0)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f0)  # Image
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f1)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f1)  # Image
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f2)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f2)  # Image
        wrap_info.append(
        """
        <!p1><font color='black'><br></font>
        <!p2><br>
        """ + f3)  # Title
        wrap_info.append(path_select + '/' + img_dir + '/' + f3)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)
    print('\nwrap_info:\n', wrap_info)

# --------------------------------------------------------------------------
else:
    print('wrap_info was not created. Undefined col_num selected.')
# --------------------------------------------------------------------------


# WRAPPER
main = base % wrap_info
# Explanation
# main = base % (filelist0[0], filelist1[0],
#                filelist0[1], filelist1[1],
#                   :
#                   )

# OUTPUT
output = '/'.join(wd.split('\\')[:-1]) + '/' + out_filename
f = open(output, 'w')
f.write(main)
f.close()
print('\nOUTPUT:\n', output)

# SHOW
open_new_tab(output)


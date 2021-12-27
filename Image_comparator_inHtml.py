"""
Display all the image file in a directory.
2/3/4 columns ver. is currently available.
"""

from webbrowser import open_new_tab
import os
import sys
from htmlModule import *


# SETTINGS -----------------------------------------------------
wd = r'D:\stock_data'
cwd = sys.path[-1]
filelist = os.listdir(wd)  # Work file directory
filelist = list(filter(lambda x: x.endswith('.png'), filelist))  # Work file
path_select = '.'  # Output file directory. Absolute path ver.
out_filename = 'Image_comparator.html'  # Output file name
tab_name = 'Image Comparator'  # Tab name for html file
col_num = 4  # The number of columns
# --------------------------------------------------------------


# Read html base file
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
        td {
        background-color: #ffffff;
        border: 1px solid #000000;
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
# 2 COLUMNS VER. -----------------------------------------------------------
if col_num == 2:
    # Repeat pattern
    wrapper = """
    <tr>
      <td>%s<img src=%s></td>
      <td>%s<img src=%s></td>
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
    # Upper/Lower
    filelist0 = filelist[:len(filelist)//2]
    filelist1 = filelist[len(filelist)//2:]
    # Odd/Even
    # filelist0, filelist1 = get_oddeven(filelist)

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f0,f1 in zip(filelist0, filelist1):
        wrap_info.append(f0 + '<br>')  # Title
        # Path: Absolute or Relative
        # Path = Absolute
        wrap_info.append(path_select + '/' + f0)  # Image
        wrap_info.append(f1 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f1)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)

# 3 COLUMNS VER. -----------------------------------------------------------
elif col_num == 3:
    # Repeat pattern
    wrapper = """
    <tr>
      <td>%s<img src=%s></td>
      <td>%s<img src=%s></td>
      <td>%s<img src=%s></td>
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
    # Upper/Middle/Lower
    filelist0 = filelist[:len(filelist) * 1 // 3]
    filelist1 = filelist[len(filelist) * 1 // 3:len(filelist) * 2 // 3]
    filelist2 = filelist[len(filelist) * 2 // 3:]
    # Remainder == 0/1/2
    # TBD

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f0,f1,f2 in zip(filelist0, filelist1, filelist2):
        wrap_info.append(f0 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f0)  # Image
        wrap_info.append(f1 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f1)  # Image
        wrap_info.append(f2 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f2)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)

# 3 COLUMNS VER. -----------------------------------------------------------
elif col_num == 4:
    # Repeat pattern
    wrapper = """
    <tr>
      <td>%s<img src=%s></td>
      <td>%s<img src=%s></td>
      <td>%s<img src=%s></td>
      <td>%s<img src=%s></td>
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

    # Make a tuple for wrapper
    wrap_info = [tab_name]
    for f0,f1,f2,f3 in zip(filelist0, filelist1, filelist2, filelist3):
        wrap_info.append(f0 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f0)  # Image
        wrap_info.append(f1 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f1)  # Image
        wrap_info.append(f2 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f2)  # Image
        wrap_info.append(f3 + '<br>')  # Title
        wrap_info.append(path_select + '/' + f3)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)

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
f = open(wd + '/' + out_filename, 'w')
f.write(main)
f.close()

# SHOW
open_new_tab(wd + '/' + out_filename)


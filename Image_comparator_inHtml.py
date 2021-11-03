from webbrowser import open_new_tab
import os
import sys
from htmlModule import *


# SETTINGS
wd = 'C:/Users/A/Desktop/stock_data'
cwd = sys.path[-1]
filelist = os.listdir(wd)  # Work file directory
filelist = list(filter(lambda x: x.endswith('.png'), filelist))  # Work file
out_file = cwd  # Output file directory
out_filename = 'Image_comparator.html'  # Output file name
tab_name = 'Image Comparator'  # Tab name for html file
col_num = 3  # The number of columns

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
    # Insert content to <table>
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
        wrap_info.append(f0)  # Title
        wrap_info.append(wd + '/' + f0)  # Image
        wrap_info.append(f1)  # Title
        wrap_info.append(wd + '/' + f1)  # Image
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
        wrap_info.append(f0)  # Title
        wrap_info.append(wd + '/' + f0)  # Image
        wrap_info.append(f1)  # Title
        wrap_info.append(wd + '/' + f1)  # Image
        wrap_info.append(f2)  # Title
        wrap_info.append(wd + '/' + f2)  # Image
    # List to tuple (for wrapper)
    wrap_info = tuple(wrap_info)

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
f = open(out_file + '/' + out_filename, 'w')
f.write(main)
f.close()

# SHOW
open_new_tab(out_file + '/' + out_filename)


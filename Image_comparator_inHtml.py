from webbrowser import open_new_tab
import os

# IMPORT
wd = 'C:/Users/A/Desktop/stock_data'
filelist = os.listdir(wd)
filelist = list(filter(lambda x: x.endswith('.png'), filelist))

out_file = 'out_file.html'

# Read html wrapper file
# temp_wrapper = 'temp_wrapper.html'
# htmlFile = open(temp_wrapper, 'r', encoding='UTF-8')
# wrapper = htmlFile.read()

wrapper = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
</body>
</html>
"""

base = '<img src=%s title=%s>'

body = ''
# 2 columns ver.
for i in range(len(filelist)):
    if i == 0:  # for the first image
        body = base
    elif i%2 == 1:  # column 0
        body = body + base
    elif i >= 1 and i%2 == 0:  # column 1
        body = body + base + '<br>'
    else:
        print('Something is wrong')
# Insert body to html
index = wrapper.find('</body>')
wrapper = wrapper[:index] + body + wrapper[index:]

# Make tuple for wrapper
wrap_info = []
for f in filelist:
    wrap_info.append(wd + '/' + f)
    wrap_info.append(f)
wrap_info = tuple(wrap_info)

# WRAPPER
main = wrapper % wrap_info
# main = wrapper % (wd +'/' + filelist[0], filelist[0],
#                   wd +'/' + filelist[1], filelist[1],
#                   :
#                   )

# OUTPUT
f = open(out_file, 'w')
f.write(main)
f.close()

# SHOW
open_new_tab(out_file)


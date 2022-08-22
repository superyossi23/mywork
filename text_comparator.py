"""
22.08.22 txtcomp_linebyline_html: startswith added. reGex added.

def txtcomp_linebyline: Compare txt file line by line
def txtcomp_linebyline_html: Compare txt file line by line & Output in html <https://www.youtube.com/watch?v=UfTxOjdM9Bg&t=2s: Comparing Two Text Files using Python>
def txtcomp_lineandfile: Compare txt file, line and file

"""

import difflib
import sys
import re
import time

path = r"C:\Users\fx33403\Desktop\temp"
filename_1 = 'teraterm_v271_nvmwritten_220819.txt'
filename_2 = 'teraterm_v281_nvmwritten_220819.txt'
# Output only lines that has differences
DIFFERENCES_ONLY = False
# For Debug
verbose = True

def txtcomp_linebyline(
        path,
        filename_1,
        filename_2
):
    t1 = time.time()

    first_file = path + "\\" + filename_1
    second_file = path + "\\" + filename_2
    # \ 2 txt file lists must be the same length
    f1 = open(first_file, "r").readlines()
    f2 = open(second_file, "r").readlines()

    i = 0
    f1_only, f2_only = [], []
    new_f = open(path + "\\" + 'txtcomp_linebyline.txt', 'w')

    for line_a in f1:
        i += 1
        for line_b in f2:
            # \ matching line 1 from both files
            if line_a != line_b:
                if verbose:
                    print("Mismatch at Line ", i, ":")
                    # \ Print a line from both files
                    print("\tf1: ", line_a, end='')
                    print("\tf2: ", line_b, end='')
                # \ Extract mismatched lines
                new_f.write('Line' + str(i) + '\n' + line_a + '\n' + line_b + '\n')
                # \ Extract to a list
                f1_only.append(line_a)
                f2_only.append(line_b)
            break

    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"Elapsed time : {round(elapsed_time, 3)} sec")

    return f1_only, f2_only



def txtcomp_linebyline_html(
        path,
        filename_1,
        filename_2
):
    t1 = time.time()

    first_file = path + "\\" + filename_1
    second_file = path + "\\" + filename_2
    # \ 2 txt file lists must be the same length
    f1 = open(first_file, "r").readlines()
    f2 = open(second_file, "r").readlines()

    # \ Removal of unnecsesary lines
    f_reGex = re.compile(r'R\d+\s\w\w\w\w\w\w\w\w\w')
    for f in f1:
        mo = f_reGex.search(f)
        if f.startswith('readnvm'):
            f1.remove(f)
        elif f == mo.group():
            f1.remove(f)
    for f in f2:
        mo = f_reGex.search(f)
        if f.startswith('readnvm'):
            f2.remove(f)
        elif f == mo.group():
            f1.remove(f)

    # \ reGex ver.
    # f_reGex = re.compile(r'\w+\s\w+')
    # for f in f1:
    #     mo = f_reGex.search(f)  # Matched Object
    #     if f == mo.group():  # mo.group() returns the matched string
    #         f1.remove(f)
    # for f in f2:
    #     mo = f_reGex.search(f)  # Matched Object
    #     if f == mo.group():  # mo.group() returns the matched string
    #         f2.remove(f)

    # \ Make HTML (str)
    print('Execute "difflib.HtmlDiff().make_file(f1, f2, first_file, second_file)"')
    diff = difflib.HtmlDiff().make_file(f1, f2, first_file, second_file)

    # \ If you want to extract "only differences" from tbody_list --------------------------------
    if DIFFERENCES_ONLY:
        print('"DIFFERENCES_ONLY = True"')
        # \ Extract tbody-sentence from diff
        tbody = diff[diff.find('<tbody>') + len('<tbody>'): diff.find('</tbody>')]
        tbody_list = tbody.split('\n')

        # \ Remove unnecessary data from tbody_list
        # \ Extract diff_add (added) / diff_chg (changed) / diff_sub (subtracted)
        for line in tbody_list:
            if 'diff_add' not in line:
                if 'diff_chg' not in line:
                    if 'diff_sub' not in line:
                        tbody_list.remove(line)

        if verbose:
            print('"tbody_list" changed to ->\n', tbody_list)

        n = 1 # \ n must start with 1
        for line in tbody_list[12:]: # \ 12 is the space unwanted
            no1 = re.search('id="from(\d*)_(\d*)">(\d*)<', line).group(1)
            no2 = re.search('id="from(\d*)_(\d*)">(\d*)<', line).group(2)
            line = line.replace('id="from' + str(no1) + '_' + str(no2) + '">' + str(no2) + '<',
                                'id="from' + str(no1) + '_' + str(n) + '">' + str(n) + '<', 1)
            tbody_list[n] = line.replace('id="to' + str(no1) + '_' + str(no2) + '">' + str(no2) + '<',
                                         'id="to' + str(no1) + '_' + str(n) + '">' + str(n) + '<', 1)
            n += 1

        # \ tbody           : txt file info
        tbody = '\n'.join(tbody_list)
        # \ diff_split[1]   : legends info
        diff_split = diff.split('</tbody>')
        # \ diff_split_2[0] : html settings info & file path info
        diff_split_2 = diff_split[0].split('<tbody>')

        if verbose:
            print('tbody : ', tbody,
                  '\ndiff_split :', diff_split,
                  '\ndiff_split_2 :', diff_split_2)

        diff = diff_split_2[0] + tbody + '</tbody>' + diff_split[1]
        # \ END of "if DIFFERENCES_ONLY:" ---------------------------------------------------------

    # \ Output html file
    with open(path + "\\" + 'txtcomp_linebyline.html', 'w') as f:
        f.write(diff)

    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"Elapsed time : {round(elapsed_time, 3)} sec")

    return diff



def txtcomp_lineandfile(
    path,
    filename_1,
    filename_2
):

    first_file = path + "\\" + filename_1
    second_file = path + "\\" + filename_2
    # \ 2 txt file lists must be the same length
    f1 = open(first_file, "r").readlines()
    f2 = open(second_file, "r").readlines()

    new_f = open('resources/txtcomp_lineandfile.txt', 'w')
    new_f.write('f1: ' + first_file + '\nf2: ' + second_file +
                '\nString not in f1 but f2...\n\n')

    f1_joined = ''.join(f1)
    for string in f2:
        if string not in f1_joined:
            print('string not in f1: ', string)
            new_f.write(string + '\n')

    # \ closing files
    new_f.close()

    return


if __name__ == "__main__":
    # txtcomp_linebyline_html(path, filename_1, filename_2)
    # txtcomp_linebyline(path, filename_1, filename_2)

    print('text_comparator.py done!')


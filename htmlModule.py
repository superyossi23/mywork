
# Divide filelist into odd/even
def get_oddeven(filelist):
    filelist0, filelist1 = [], []
    for i in range(len(filelist)):
        if i % 2 == 0:
            filelist0.append(filelist[i])
        elif i % 2 == 1:
            filelist1.append(filelist[i])
        else:
            Exception('Something went wrong while executing get_oddeven')
    return filelist0, filelist1


# Divide filelist into Left/Center/Right
def get_LCR(filelist):
    filelist0, filelist1, filelist2 = [], [], []
    for i in range(len(filelist)):
        if i % 3 == 0:
            filelist0.append(filelist[i])
        elif i % 3 == 1:
            filelist1.append(filelist[i])
        elif i % 3 == 2:
            filelist2.append(filelist[i])
        else:
            Exception('Something went wrong while executing get_LCR')
    return filelist0, filelist1, filelist2


# Divide filelist into LL/L/R/RR
def get_LLRR(filelist):
    filelist0, filelist1, filelist2, filelist3 = [], [], [], []
    for i in range(len(filelist)):
        if i % 4 == 0:
            filelist0.append(filelist[i])
        elif i % 4 == 1:
            filelist1.append(filelist[i])
        elif i % 4 == 2:
            filelist2.append(filelist[i])
        elif i % 4 == 3:
            filelist3.append(filelist[i])
        else:
            Exception('Something went wrong while executing get_LCR')
    return filelist0, filelist1, filelist2, filelist3


def sort_filelist(filelist, lastname):
    filedict = {}
    for f in filelist:
        num = f.split('.')[0].split(lastname)[1]
        if num == '':
            num = 0
        else:
            num = int(num)
        filedict[num] = f
    return filedict




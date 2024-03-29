"""
22.08.19 Create a script for read register or nvm value.

"""
import pandas as pd


wd = r"C:\Users\fx33403\PycharmProjects\pycProject\Scripts"
mode = "nvm"  # "fpga" or "nvm"


# This is for readfpga cmd
if mode == "fpga":
    adr = 0x80031000
    cnt = 1

    with open(wd + '\\terascript.txt', 'w') as f:  # x: overwrite
        f.write('\n\n')

        while adr <= 0x80031130:
            f.write('readfpga ' + hex(adr).split('x')[1] + '\n')
            print('readfpga', hex(adr).split('x')[1])
            adr += 0x4

# This is for readnvm cmd
elif mode == "nvm":
    cnt = 0
    data = pd.read_csv(r"C:\Users\fx33403\ILS(C)\ILSDP\002.Zynq\Debug\nvmlist_koOlina-SMG_k92.csv", encoding='shift_jis')

    with open(wd + '\\terascript.txt', 'w') as f:  # x: overwrite
        f.write('\n\n')

        # This is for readnvm cmd
        while cnt <= len(data)-1:
            f.write('readnvm ' + str(data.iloc[cnt][1]) + '\n')
            print('readnvm ' + str(data.iloc[cnt][1]) + ' written')

            cnt += 1


print("\ncreate_read_script.py done !! \nfile saved at : ", wd + '\\terascript.txt')

import argparse
import os
import requests
import subprocess

url = 'https://api.esmatlas.com/foldSequence/v1/pdb/'

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("input_folder", type=str, help="input folder containing subfolders with pdb files")
parser.add_argument("-o", "--outfa_path", type=str, default="", help="output directory for outfa file")
args = parser.parse_args()

input_folder = args.input_folder
outfa_path = args.outfa_path
flag = True


def aa3toaa1(threecode):
    aamap = {'ALA': 'A', 'CYS': 'C', 'CYD': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
             'LYS': 'K', 'LEU': 'L', 'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', 'SER': 'S', 'THR': 'T',
             'VAL': 'V', 'TRP': 'W', 'TYR': 'Y', 'MSE': 'M', 'CSO': 'C', 'SEP': 'S'}
    return aamap[threecode]


def pdb2fa(pdb, outfa='',outfa_path='', gap=True):
    if outfa == '':
        #outfa = pdb[0:-4] + ".fa"
        outfa ="lengthover400.fa"
    if outfa_path != '':
        outfa = os.path.join(outfa_path, outfa)
    cont = open(pdb)
    pdb_filename = os.path.basename(pdb)
    pdb_name = os.path.splitext(pdb_filename)[0]

    savecont = ['>%s\n' % pdb_name]
    #savecont = ['>%s\n' % pdb[:-4]]
    print(savecont)
    char = ''
    prvres = -999

    for line in cont:
        if line[:4] != 'ATOM':
            continue

        resno = int(line[22:26])

        if resno == prvres:
            continue

        if resno - prvres > 1 and prvres != -999 and gap:
            char += '-' * (resno - prvres - 1)

        seq = line[16:20].strip()
        char += aa3toaa1(seq)
        prvres = resno
    char += '\n'
    savecont.append(char)
    line2 = savecont[1]
    # savefile = open(outfa, 'w')
    # savefile.writelines(line2)

    line2 = line2.replace('\n', '')
    output_file = savecont[0][1:]+".pdb"  # 定义输出文件名
    output_file = output_file.replace('\n', '')
    print(output_file)

    output_file = os.path.join(outfa_path, output_file)
    if len(line2) < 400:
        curl_command = f"curl -X POST --data '{line2}' {url} > {output_file}"  # 使用重定向操作符将输出重定向到文件
        print(curl_command)
        #subprocess.run(curl_command, shell=True)
    else:
        print("lengthover400:",output_file)
        savefile = open(outfa, 'a')
        savefile.writelines(savecont)


if not os.path.isdir(input_folder):
    print("Input folder does not exist.")
    flag = False
    exit()

if outfa_path != '':
    os.makedirs(outfa_path, exist_ok=True)


for root, dirs, files in os.walk(input_folder):
    for file in files:
        if len(file) > 6 and file[-4:] == ".pdb" and file[-6] == ".":
            pdb_file = os.path.join(root, file)
            pdb2fa(pdb_file, outfa_path=outfa_path)
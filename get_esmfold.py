import argparse
import os
import requests
import subprocess
from multiprocessing import Pool

url = 'https://api.esmatlas.com/foldSequence/v1/pdb/'

fa_file = 'input.fa'
out_path = 'ESM_DB'

flag = True

if out_path != '':
    os.makedirs(out_path, exist_ok=True)


def download_fa(fasta, outfa_path):
    if len(fasta) < 400:
        curl_command = f"curl -X POST --data '{fasta}' {url} > {outfa_path}"  # 使用重定向操作符将输出重定向到文件
        print(curl_command)
        # subprocess.run(curl_command, shell=True)
    else:
        print("lengthover400:", outfa_path)


if __name__ == '__main__':
    p = Pool(20)  # 创建含有十个10个进程的进程池
    with open(fa_file) as f:
        content = f.read().split('\n')

    for i in range(int(len(content) / 2)):  # 启动10个进程
        name = content[2 * i][1:] + '.pdb'
        outfa_path = os.path.join(out_path, name)
        fasta = content[2 * i + 1]
        p.apply_async(download_fa, args=(fasta, outfa_path,))  # 产生一个非同步进程，函数newsin的参数用args传递
    p.close()  # 关闭进程池
    p.join()  # 结束

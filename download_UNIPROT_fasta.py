import requests
from lxml import etree
import urllib.request
import multiprocessing
'''
    Xpath 以一种类似于文件访问的方式 来读取网页页面上的内容
'''

pdb_uniport_dict = {}

def download_fasta_from_uniprot(index, pdbName):
    # pdb的网页路径
    pdb_url = "https://www.rcsb.org/structure/" + pdbName
    pdb_resp = requests.get(pdb_url)
    # 获取网页对象
    pdb_html = etree.HTML(pdb_resp.text)

    # 拿到div ( 网页上的每一个对象 )
    elements = pdb_html.xpath('//*[@id="table_macromolecule-protein-entityId-1"]/tbody/tr[5]/td/div[3]/span/a')

    # 遍历获取到的对象
    uniprot_name = ''
    for element in elements:
        # uniprot 代号
        uniprot_name = element.text
        print(uniprot_name)

    # 做字典映射
    pdb_uniport_dict[pdbName] = uniprot_name
    pdb_resp.close()

    # 拼接出 uniprot的网页路径
    uniprot_url = 'https://rest.uniprot.org/uniprotkb/' + uniprot_name + '.fasta'
    print(uniprot_url)
    # 访问该路径并获得内容
    uniprot_resp = urllib.request.urlopen(uniprot_url, timeout=6)
    # 拼接出 fasta文件 的名字
    fname = 'D:\pycharm\mySeqDesign\dataset\扩充数据集\\uniprot_fastas\\' + uniprot_name + '.fasta'
    # 写文件
    with open(fname, "wb") as g:
        g.write(uniprot_resp.read())
        print(uniprot_name + " done")

    uniprot_resp.close()


# pdbName = '1aqt'
# download_from_uniprot(pdbName)


if __name__ == "__main__":
    pool = multiprocessing.Pool(10)
    testPDBNames = "D:\pycharm\mySeqDesign\dataset\扩充数据集\下载cif\\test.txt"
    with open(testPDBNames, "r") as namesFile:
        nameList = namesFile.readlines()
    for index, pdb_name in enumerate(nameList):
        pdb_name = pdb_name.replace("\n", '')
        pool.apply_async(download_fasta_from_uniprot, args=(index, pdb_name))

    pool.close()
    pool.join()

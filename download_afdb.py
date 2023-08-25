import multiprocessing
import requests
import os


db_folder = 'af_db'
if not os.path.exists(db_folder):
    os.mkdir(db_folder)


def deal(uniprot_name):
    url = f'https://www.alphafold.ebi.ac.uk/api/prediction/{uniprot_name}?key=AIzaSyCeurAJz7ZGjPQUtEaerUkBZ3TaBkXrY94'
    pdb_resp = requests.get(url, timeout=2)
    pdb_resp.close()
    json_data = pdb_resp.json()
    af_url = json_data[0]['pdbUrl']
    af_name = af_url.split('/')[-1]
    af_resp = requests.get(af_url, timeout=2)
    with open(os.path.join(db_folder, af_name), 'w') as f:
        f.write(af_resp.text)
    af_resp.close()


if __name__ == "__main__":
    pool = multiprocessing.Pool(50)
    with open ("uniport.txt","r") as f:
        content = f.readlines()
        for line in content:
            words = line.strip().split()
            if len(words) > 1:
                uniprot_name = words[1]
                pool.apply_async(deal, (uniprot_name, ))
        pool.close()
        pool.join()
        

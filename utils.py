import subprocess
import os
import requests
from colorama import Fore, Back, Style


from tqdm import tqdm

def call(command):
    return subprocess.Popen(command, shell=True, cwd=os.path.dirname(os.path.realpath(__file__)), stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def download_file(url, name):
    # local_filename = name
    # with requests.get(url, stream=True) as r:
    #     r.raise_for_status()
    #     with open(local_filename, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=8192): 
    #             f.write(chunk)
    
    response = requests.get(url, stream=True)

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, ncols=75, bar_format=Fore.YELLOW+name + Fore.BLUE+' {l_bar}'+ Fore.GREEN +'{bar}'+ Fore.BLUE+'|'+ Style.RESET_ALL +' {n_fmt}/{total_fmt} {unit} Remaining: [{remaining}]')

    with open(name, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()


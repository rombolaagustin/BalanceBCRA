import os

from urllib import request
from datetime import datetime

def downloadFile(url: str, filename: str, hours: float, return_msg=False):
    """DOWNLOAD FILE

    Args:
        url (str): URL to download
        filename (str): filename to save
        hours (float): hours to download 
    """
    try: 
        creation_date = os.path.getctime(filename)
        now = datetime.now().timestamp()
        if hours*60*60 < now - creation_date:
            print(f'Downloading {filename} ...')
            request.urlretrieve(url, filename)
            if return_msg:
                return 'Descargado correctamente'
        else:
            print('OK: File is up to date')
            if return_msg:
                return 'Archivo ya actualizado'
    except:
        print(f'{filename} does not exist. Downloading...')
        request.urlretrieve(url, filename)
        if return_msg:
            return 'Descargado correctamente'
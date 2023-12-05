import os

from urllib import request
from datetime import datetime

def downloadFile(url: str, filename: str, hours: float, return_msg=False):
    """DOWNLOAD FILE

    Args:
        url (str): URL to download
        filename (str): filename to save
        hours (float): hours to download 
        return_msg (bool): return message
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
            print(f'OK: File {filename} is up to date')
            if return_msg:
                return 'Archivo ya actualizado'
    except:
        print(f'{filename} does not exist. Downloading...')
        request.urlretrieve(url, filename)
        if return_msg:
            return 'Descargado correctamente'


def selectElementsDict(d: dict, elements: list, keyOrValue = True):
    ad = {v:k for k, v in d.items()}
    try: 
        # keyOrValue = True --> elements are keys
        if keyOrValue:
            r = [d[e] for e in elements]
        # keyOrValue = False --> elements are values
        else:
            r = [ad[e] for e in elements]
        return r
    except:
        return []
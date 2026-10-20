"""Fetch pinned public tools, verifying each release checksum before use."""
from pathlib import Path
import hashlib,json,urllib.request,sys
ROOT=Path(__file__).resolve().parents[1]
def fetch(destination=None):
    destination=Path(destination or ROOT/'.tools').resolve();destination.mkdir(parents=True,exist_ok=True)
    for item in json.loads((ROOT/'config/tools.lock.json').read_text()):
        path=destination/item['file']
        if not path.exists():
            print('Downloading',item['file'],flush=True)
            request=urllib.request.Request(item['url'],headers={'User-Agent':'StayX-build-tools/1.0'})
            with urllib.request.urlopen(request,timeout=120) as response,path.open('wb') as out:
                while chunk:=response.read(1024*1024):out.write(chunk)
        digest=hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
        if digest!=item['sha256']:raise RuntimeError(f'Checksum mismatch: {path}; remove it and retry')
        print('Verified',item['file'],flush=True)
    return destination
if __name__=='__main__':fetch(sys.argv[1] if len(sys.argv)>1 else None)

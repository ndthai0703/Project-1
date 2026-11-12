from pathlib import Path
import urllib.request
import hashlib
from src.utils.config import ROOT
URL="https://github.com/RuiyangJu/Bone_Fracture_Detection_YOLOv8/releases/download/Trained_model/best.pt"

def main():
    path=ROOT/"checkpoints/fracture_yolov8.pt";path.parent.mkdir(exist_ok=True)
    if not path.exists():
        tmp=path.with_suffix(".partial")
        try:
            with urllib.request.urlopen(URL,timeout=120) as r,tmp.open("wb") as f:
                while chunk:=r.read(1024*1024):f.write(chunk)
            if tmp.stat().st_size<100000:raise RuntimeError("Download too small to be a checkpoint")
            tmp.replace(path)
        finally:tmp.unlink(missing_ok=True)
    print(path)
    print("SHA256:",hashlib.sha256(path.read_bytes()).hexdigest())
if __name__=="__main__":main()

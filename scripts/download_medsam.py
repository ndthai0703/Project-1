from pathlib import Path
import urllib.request
import time
from src.utils.config import ROOT

URL = "https://huggingface.co/SansuiHan/medical_models/resolve/main/medsam_vit_b.pth"

def main():
    dest = ROOT / "checkpoints" / "medsam_vit_b.pth"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 350 * 1024 * 1024:
        print(f"Checkpoint already exists: {dest} ({dest.stat().st_size} bytes)")
        return

    tmp = dest.with_suffix(".partial")
    print(f"Downloading MedSAM from {URL} to {dest}...")
    start = time.time()
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=300) as r, tmp.open("wb") as f:
            total_size = int(r.headers.get("Content-Length", 0))
            downloaded = 0
            while chunk := r.read(1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    pct = (downloaded / total_size) * 100
                    print(f"\rProgress: {downloaded / 1024 / 1024:.1f}/{total_size / 1024 / 1024:.1f} MB ({pct:.1f}%)", end="", flush=True)
            print()
        if tmp.stat().st_size < 300 * 1024 * 1024:
            raise RuntimeError(f"File too small ({tmp.stat().st_size} bytes)")
        tmp.replace(dest)
        print(f"Downloaded MedSAM successfully in {time.time() - start:.1f}s: {dest}")
    finally:
        tmp.unlink(missing_ok=True)

if __name__ == "__main__":
    main()

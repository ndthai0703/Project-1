from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[2]

def load_config(path=None):
    path=Path(path) if path else ROOT/"configs/medical_vqa.yaml"
    with path.open(encoding="utf-8") as f: cfg=yaml.safe_load(f)
    m,i=cfg["model"],cfg["inference"]
    if m["backend"] not in ("qwen","smolvlm"): raise ValueError("Unknown model backend")
    if m["device"] not in ("auto","cpu","cuda"): raise ValueError("device: auto/cpu/cuda")
    if i["language"] not in ("vi","en"): raise ValueError("language: vi/en")
    if m["backend"]=="smolvlm" and i["language"]!="en":
        raise ValueError("SmolVLM profile supports English only; use Qwen for Vietnamese experiments")
    if not 1 <= i["max_new_tokens"] <= 512: raise ValueError("max_new_tokens: 1..512")
    if not 128 <= i["max_image_side"] <= 1536: raise ValueError("max_image_side: 128..1536")
    return cfg

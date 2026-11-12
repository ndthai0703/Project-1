import importlib
import sys

def main():
    print("Python:",sys.version)
    failed=False
    for name in ("torch","torchvision","transformers","accelerate","PIL","yaml","streamlit"):
        try:
            m=importlib.import_module(name);print(name,getattr(m,"__version__","OK"))
        except Exception as e: print(name,"ERROR",str(e));failed=True
    if not failed:
        import torch
        from transformers import Qwen3VLForConditionalGeneration, AutoModelForVision2Seq
        print("CUDA:",torch.cuda.is_available())
        if torch.cuda.is_available(): print("GPU:",torch.cuda.get_device_name(0))
        print("Model classes: OK; weights have not been downloaded by this check")
    return int(failed)
if __name__=="__main__": raise SystemExit(main())

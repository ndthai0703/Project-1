import argparse
import json
from pathlib import Path
from src.utils.config import load_config
from src.engine.pipeline import MedicalVQAPipeline

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--config",default="configs/medical_vqa.yaml")
    p.add_argument("--image",required=True)
    p.add_argument("--question",default="")
    p.add_argument("--task",choices=["vqa","caption","both"],default="vqa")
    p.add_argument("--answer-type",choices=["open","closed"],default="open")
    p.add_argument("--output")
    a=p.parse_args()
    result=MedicalVQAPipeline(load_config(a.config)).predict(a.image,a.question,a.task,a.answer_type)
    text=json.dumps(result,ensure_ascii=False,indent=2)
    print(text)
    if a.output:
        path=Path(a.output); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding="utf-8")
if __name__=="__main__": main()

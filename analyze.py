import argparse,json
from pathlib import Path
import yaml
from src.utils.config import load_config,ROOT
from src.engine.full_pipeline import FullPipeline

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--image",required=True)
    p.add_argument("--question",default="")
    p.add_argument("--scope",required=True,choices=["pediatric_wrist","other","unknown"])
    p.add_argument("--config",default=str(ROOT/"configs/medical_vqa.yaml"))
    p.add_argument("--vision-config",default=str(ROOT/"configs/vision.yaml"))
    p.add_argument("--task",default="both",choices=["vqa","caption","both"])
    p.add_argument("--output",default="results/analysis.json")
    a=p.parse_args()
    cfg=yaml.safe_load(Path(a.vision_config).read_text())
    result=FullPipeline(load_config(a.config),cfg).predict(a.image,a.question,a.scope,Path(a.output).parent,a.task)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(out)
if __name__=="__main__":main()

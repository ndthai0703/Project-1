import argparse
import json
from pathlib import Path
from src.utils.config import load_config
from src.utils.metrics import score
from src.engine.pipeline import MedicalVQAPipeline

def main():
    p=argparse.ArgumentParser(description="Zero-shot evaluation; never trains a model")
    p.add_argument("--config",default="configs/medical_vqa.yaml")
    p.add_argument("--data",required=True)
    p.add_argument("--image-dir",default="data/images")
    p.add_argument("--output",default="results/evaluation.json")
    a=p.parse_args()
    rows=json.loads(Path(a.data).read_text(encoding="utf-8"))
    if not isinstance(rows,list) or not rows: raise ValueError("Evaluation data must be a nonempty list")
    root=Path(a.image_dir).resolve()
    # Validate entire input before expensive model loading.
    for r in rows:
        refs=r.get("answers",[r.get("answer","")])
        if not isinstance(refs,list) or not refs or any(not isinstance(x,str) or not x.strip() for x in refs): raise ValueError("Each record needs answer or answers")
        if not isinstance(r.get("question"),str) or not r["question"].strip(): raise ValueError("Missing question")
        path=(root/r["image"]).resolve()
        if not path.is_relative_to(root) or not path.is_file(): raise ValueError(f"Invalid image: {r['image']}")
    pipeline=MedicalVQAPipeline(load_config(a.config)); outputs=[]
    for r in rows:
        result=pipeline.predict(root/r["image"],r["question"])
        refs=r.get("answers",[r.get("answer","")])
        outputs.append({**r,**result,**score(result["answer"],refs)})
    report={"count":len(outputs),"metrics":{k:sum(r[k] for r in outputs)/len(outputs) for k in ("exact_match","token_f1")},"predictions":outputs}
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report["metrics"],indent=2))
if __name__=="__main__": main()

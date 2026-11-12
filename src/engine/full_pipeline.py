import json
from src.engine.vision_pipeline import VisionPipeline
from src.engine.pipeline import MedicalVQAPipeline

class FullPipeline:
    def __init__(self,vqa_cfg,vision_cfg,vision=None,vqa=None):
        self.vision=vision or VisionPipeline(vision_cfg)
        self.vqa=vqa or MedicalVQAPipeline(vqa_cfg)
    def predict(self,source,question,scope,output_dir,task="both",answer_type="open"):
        # Validate question before running costly vision inference.
        if task!="caption" and not question.strip():raise ValueError("Vui lòng nhập câu hỏi")
        vision=self.vision.run(source,scope,output_dir)
        context={k:vision[k] for k in ("status","scope","detections","warning")}
        context["detections"]=[{k:v for k,v in d.items() if k!="mask_path"} for d in context["detections"]]
        context["instruction"]="These are unverified detector/segmentation outputs. Do not infer a diagnosis or normality from them. Never treat mask pixels as real physical lesion size."
        answer=self.vqa.predict(source,question,task,answer_type,vision_context=json.dumps(context,ensure_ascii=False))
        return {**answer,"vision":vision}

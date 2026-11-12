from pathlib import Path
import uuid
import numpy as np
from PIL import Image,ImageDraw
from src.data.preprocessing import prepare_image

class VisionPipeline:
    def __init__(self,cfg,detector=None,segmenter=None):
        self.cfg,self.detector,self.segmenter=cfg,detector,segmenter
    def run(self,source,scope,output_dir):
        if scope!=self.cfg["supported_scope"]:
            return {"status":"unsupported_scope","scope":scope,"detections":[],"artifacts":{},
                "warning":"Detector supports pediatric wrist only; no automatic anatomy verification."}
        image=prepare_image(source,max_side=2048)
        if self.detector is None:
            from src.models.fracture_detector import FractureDetector
            self.detector=FractureDetector(self.cfg)
        detections=self.detector.predict(image)
        w,h=image.size
        clean=[]
        for item in detections:
            b=np.asarray(item["box"],dtype=float)
            if b.shape!=(4,) or not np.isfinite(b).all():continue
            b=np.clip(b,[0,0,0,0],[w,h,w,h])
            if b[2]<=b[0] or b[3]<=b[1]:continue
            clean.append({**item,"box":b.tolist()})
        detections=clean
        out=Path(output_dir)/uuid.uuid4().hex;out.mkdir(parents=True,exist_ok=False)
        original=out/"input.png";image.save(original)
        result={"status":"no_detection","scope":scope,"image_size":[w,h],"coordinate_system":"processed_image_pixels",
            "detections":detections,"artifacts":{"input":str(original.resolve())},
            "warning":"No detection does not mean normal. Masks are experimental regions, not validated fracture boundaries."}
        if not detections:return result
        if self.segmenter is None:
            from src.models.medsam_segmenter import MedSAMSegmenter
            self.segmenter=MedSAMSegmenter(self.cfg)
        masks=self.segmenter.predict(image,[d["box"] for d in detections])
        if len(masks)!=len(detections):raise RuntimeError("Mask count mismatch")
        union=np.zeros((h,w),dtype=bool)
        for index,(d,m) in enumerate(zip(detections,masks)):
            m=np.asarray(m,dtype=bool)
            if m.shape!=(h,w):raise RuntimeError("Mask coordinate mismatch")
            union |=m
            mask_path=out/f"mask_{index}.png";Image.fromarray(m.astype(np.uint8)*255).save(mask_path)
            d["mask_path"]=str(mask_path.resolve());d["mask_pixels"]=int(m.sum())
            d["segmentation_status"]="candidate_region" if m.any() else "empty_mask"
        arr=np.asarray(image).copy();arr[union]=(arr[union]*.55+np.array([255,40,40])*.45).astype(np.uint8)
        overlay=Image.fromarray(arr);draw=ImageDraw.Draw(overlay)
        for d in detections:draw.rectangle(d["box"],outline="yellow",width=3)
        path=out/"overlay.png";overlay.save(path)
        merged=out/"mask_union.png";Image.fromarray(union.astype(np.uint8)*255).save(merged)
        result["artifacts"].update(overlay=str(path.resolve()),mask=str(merged.resolve()))
        result["status"]="detected" if union.any() else "segmentation_empty"
        return result

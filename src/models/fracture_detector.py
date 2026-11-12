from pathlib import Path

class FractureDetector:
    def __init__(self,cfg):
        from ultralytics import YOLO
        from src.utils.config import ROOT
        path=Path(cfg["weights"])
        if not path.is_absolute(): path=ROOT/path
        if not path.is_file(): raise FileNotFoundError(f"Missing detector weights: {path}. Run python -m scripts.download_detector")
        self.model=YOLO(str(path),task="detect")
        self.cfg=cfg
        self.classes=[int(i) for i,n in self.model.names.items() if str(n).strip().casefold()=="fracture"]
        if not self.classes: raise ValueError(f"Checkpoint has no fracture class: {self.model.names}")
    def predict(self,image):
        c=self.cfg
        r=self.model.predict(source=image,conf=c["confidence"],iou=c["iou"],
            classes=self.classes,max_det=c["max_detections"],imgsz=c["image_size"],device=c["device"],verbose=False)[0]
        if r.boxes is None: return []
        return [{"box":b,"score":float(s),"label":"suspected_fracture"} for b,s in
            zip(r.boxes.xyxy.cpu().tolist(),r.boxes.conf.cpu().tolist())]

from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F

class MedSAMSegmenter:
    def __init__(self,cfg):
        from segment_anything import sam_model_registry
        from src.utils.config import ROOT
        path=Path(cfg["medsam_weights"])
        if not path.is_absolute():path=ROOT/path
        if not path.is_file():raise FileNotFoundError(f"Missing MedSAM checkpoint: {path}. See docs/SETUP_VISION.md")
        self.device=cfg["device"]
        self.model=sam_model_registry["vit_b"](checkpoint=None)
        state_dict=torch.load(path,map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device).eval()
    @torch.inference_mode()
    def predict(self,image,boxes):
        if not boxes:return []
        from skimage.transform import resize
        # MedSAM official inference uses square resize and min-max normalization,
        # NOT the standard SAM predictor's longest-side/ImageNet preprocessing.
        a=np.asarray(image.convert("RGB"));h,w=a.shape[:2]
        a=resize(a,(1024,1024),order=3,preserve_range=True,anti_aliasing=True).astype(np.uint8)
        a=(a-a.min())/max(float(a.max())-float(a.min()),1e-8)
        tensor=torch.as_tensor(a,dtype=torch.float32,device=self.device).permute(2,0,1)[None]
        embedding=self.model.image_encoder(tensor)
        masks=[]
        for box in boxes:
            b=np.asarray(box,dtype=np.float32)/np.array([w,h,w,h])*1024
            sparse,dense=self.model.prompt_encoder(points=None,boxes=torch.tensor(b,dtype=torch.float32,device=self.device)[None,None],masks=None)
            logits,_=self.model.mask_decoder(image_embeddings=embedding,image_pe=self.model.prompt_encoder.get_dense_pe(),
                sparse_prompt_embeddings=sparse,dense_prompt_embeddings=dense,multimask_output=False)
            prob=F.interpolate(torch.sigmoid(logits),size=(h,w),mode="bilinear",align_corners=False)
            masks.append((prob[0,0].cpu().numpy()>.5))
        return masks

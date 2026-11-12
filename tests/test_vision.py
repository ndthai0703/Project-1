import numpy as np
from PIL import Image
from src.engine.vision_pipeline import VisionPipeline
from src.engine.full_pipeline import FullPipeline

CFG={'supported_scope':'pediatric_wrist'}
class Detector:
    def predict(self,image):return [{'box':[-1,2,15,18],'score':.8,'label':'suspected_fracture'}]
class Segmenter:
    def predict(self,image,boxes):
        assert boxes==[[0.,2.,15.,18.]]
        m=np.zeros((image.height,image.width),bool);m[4:10,3:9]=True
        return [m]
def test_unsupported_never_loads_models(tmp_path):
    pipe=VisionPipeline(CFG)
    assert pipe.run(None,'other',tmp_path)['status']=='unsupported_scope'
    assert pipe.detector is None and pipe.segmenter is None

def test_masks_and_coordinates(tmp_path):
    result=VisionPipeline(CFG,Detector(),Segmenter()).run(Image.new('RGB',(30,20)),'pediatric_wrist',tmp_path)
    assert result['status']=='detected'
    assert result['detections'][0]['mask_pixels']==36
    assert Image.open(result['artifacts']['mask']).size==(30,20)
    assert np.asarray(Image.open(result['artifacts']['mask'])).sum()==36*255

def test_no_box_skips_segmentation(tmp_path):
    class Empty:
        def predict(self,image):return []
    pipe=VisionPipeline(CFG,Empty())
    out=pipe.run(Image.new('RGB',(30,20)),'pediatric_wrist',tmp_path)
    assert out['status']=='no_detection' and pipe.segmenter is None
    assert 'mask' not in out['artifacts']

def test_context_passes_to_vqa(tmp_path):
    class VQA:
        def predict(self,*args,**kwargs):
            assert 'mask_pixels' in kwargs['vision_context']
            return {'answer':'test'}
    full=FullPipeline({},CFG,VisionPipeline(CFG,Detector(),Segmenter()),VQA())
    out=full.predict(Image.new('RGB',(30,20)),'test','pediatric_wrist',tmp_path)
    assert out['vision']['status']=='detected'

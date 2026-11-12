import io
import pytest
from PIL import Image
from src.utils.config import load_config,ROOT
from src.engine.pipeline import MedicalVQAPipeline
from src.data.preprocessing import prepare_image
from src.utils.metrics import score
from src.utils.prompts import make_prompt

class FakeModel:
    def generate(self,image,prompt,max_new_tokens):
        assert image.mode=="RGB"
        assert "Câu hỏi:" in prompt or "Mô tả" in prompt
        return "Đây là câu trả lời giả chỉ dành cho unit test."

def test_resize_preserves_ratio():
    im=prepare_image(Image.new("RGB",(1600,800)),512)
    assert im.size==(512,256)
def test_bad_bytes():
    with pytest.raises(ValueError): prepare_image(b"not an image")
def test_upload_limit():
    with pytest.raises(ValueError): prepare_image(b"x"*2000,max_mb=.001)
def test_rgba():
    b=io.BytesIO();Image.new("RGBA",(20,20)).save(b,format="PNG")
    assert prepare_image(b.getvalue()).mode=="RGB"
def test_empty_question_before_model_load():
    pipe=MedicalVQAPipeline(load_config())
    with pytest.raises(ValueError):pipe.predict(Image.new("RGB",(10,10)),"")
    assert pipe.model is None
def test_pipeline_metadata():
    pipe=MedicalVQAPipeline(load_config(),FakeModel())
    out=pipe.predict(Image.new("L",(100,100)),"Đây là gì?")
    assert out["confidence"] is None and out["task"]=="vqa"
    assert out["processed_image_size"]==[100,100]
def test_caption():
    pipe=MedicalVQAPipeline(load_config(),FakeModel())
    assert pipe.predict(Image.new("RGB",(100,100)),task="caption")["task"]=="caption"
def test_metrics():
    assert score("PHỔI.",["phổi"])["exact_match"]==1
    assert score("phổi trái",["phổi phải"])["token_f1"]==.5
def test_smol_config():
    assert load_config(ROOT/"configs/smolvlm.yaml")["inference"]["language"]=="en"
def test_prompt_limit():
    with pytest.raises(ValueError):make_prompt("a"*1501)


def test_both_branches():
    class Recorder:
        def __init__(self): self.prompts=[]
        def generate(self,image,prompt,max_new_tokens):
            self.prompts.append(prompt)
            return "Có" if "Câu hỏi:" in prompt else "Mô tả độc lập"
    m=Recorder();pipe=MedicalVQAPipeline(load_config(),m)
    out=pipe.predict(Image.new("RGB",(20,20)),"Có phổi không?",task="both",answer_type="closed")
    assert out["answer"]=="Có" and out["caption"]=="Mô tả độc lập"
    assert len(m.prompts)==2 and "Có phổi không?" not in m.prompts[1]

def test_closed_ambiguous():
    from src.utils.postprocessing import format_answer
    assert format_answer("Có thể có", "closed", "vi")=="Không đủ thông tin"
    assert format_answer("Không.", "closed", "vi")=="Không"

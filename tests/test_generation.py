import threading
import torch
import pytest
from PIL import Image
from src.models.pretrained_vlm import PretrainedVLM

class Processor:
    def apply_chat_template(self,messages,**kw):
        if kw.get('tokenize'):
            assert isinstance(messages[0]['content'][0]['image'],Image.Image)
            return self.tensors()
        return 'formatted prompt'
    def __call__(self,**kw):
        assert kw['text']=='formatted prompt'
        return self.tensors()
    def tensors(self):
        return {'input_ids':torch.tensor([[10,11,12]]),'attention_mask':torch.ones(1,3,dtype=torch.long),'pixel_values':torch.ones(1,3,16,16)}
    def batch_decode(self,ids,**kw):
        assert ids.tolist()==[[20,21]]  # input prompt must not leak into answer
        return ['test answer']

class Model:
    def generate(self,**kw):
        assert kw['input_ids'].dtype==torch.long
        assert kw['pixel_values'].dtype==torch.float32
        assert not torch.is_grad_enabled()
        assert kw['do_sample'] is False
        return torch.tensor([[10,11,12,20,21]])

@pytest.mark.parametrize('backend',['qwen','smolvlm'])
def test_generation_contract(backend):
    model=PretrainedVLM.__new__(PretrainedVLM)
    model.backend=backend;model.device='cpu';model.dtype=torch.float32
    model.processor=Processor();model.model=Model();model.lock=threading.Lock()
    assert model.generate(Image.new('RGB',(32,32)),'question',32)=='test answer'

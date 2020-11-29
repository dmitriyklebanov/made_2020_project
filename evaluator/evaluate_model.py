import torch
torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True

from .run_generation import sample_sequence
from .yt_encoder import YTEncoder
from transformers import GPT2LMHeadModel
import re
import argparse
import os

class ModelEvaluator(object):
  @staticmethod
  def _load_tokenizer(path: str):
    return YTEncoder.from_pretrained(path)

  @staticmethod
  def _load_model(path: str, device: str):
    model = GPT2LMHeadModel.from_pretrained(path)
    model.to(device)
    model.eval()
    return model

  def __init__(self, model_path: str, temperature: int = 1.0, top_k: int = 0, top_p: int = 0.9, fp16: bool = False, fp16_opt_level: str = "O2", device: str = "cpu"):
    self.tokenizer = self._load_tokenizer(model_path)
    self.model = self._load_model(model_path, device)
    if fp16:
        from apex import amp
        [self.model] = amp.initialize([self.model], opt_level=fp16_opt_level)
    self.device = device
    self.temperature = temperature
    self.top_k = top_k
    self.top_p = top_p

  def tokenizer_encode(self, string: str) -> list:
    return self.tokenizer.encode(string)

  def tokenizer_decode(self, lst: list) -> str:
    return [self.tokenizer.decode(item) for item in lst]

  def sample(self, prompt: str, length: int, num_samples: int = 1, allow_linebreak:bool = True):
    filter_n = self.tokenizer.encode('\n')[-1:]
    filter_single = [1] + self.tokenizer.encode('[')[-1:] + self.tokenizer.encode('(')[-1:]
    filter_single += [] if allow_linebreak else filter_n

    context_tokens = self.tokenizer.encode(prompt)
    out = sample_sequence(
        model=self.model,
        context=context_tokens,
        length=length,
        temperature=self.temperature,
        top_k=self.top_k,
        top_p=self.top_p,
        device=self.device,
        filter_single=filter_single,
        filter_double=filter_n,
        num_samples=num_samples
    ).to('cpu')

    prompt = self.tokenizer.decode(context_tokens)
    len_prompt = len(prompt)

    replies = [out[item, :].tolist() for item in range(len(out))]
    text = [self.tokenizer.decode(item)[len_prompt:] for item in replies]
    reg_text = [re.match(r'[\w\W]*[\.!?]\n', item) for item in text]
    reg_text2 = [re.match(r'[\w\W]*[\.!?]', item) for item in text]
    result = [reg_item[0] if reg_item else reg_item2[0] if reg_item2 else item for reg_item, reg_item2, item in zip(reg_text, reg_text2, text)]
    return result

def print_sample(samples):
  for index, sample in enumerate(samples):
      print(sample)
      print(f"-------SAMPLE {index} END-------")


def create_evaluator(model_path="./model"):
    return ModelEvaluator(
        model_path=model_path,
        temperature=float(os.environ["TEMPERATURE"]),
        top_k=0,
        top_p=0.9,
        device="cpu"
    )


def predict(evaluator, prompt):
    print('predicting with prompt:', prompt)
    result = evaluator.sample(prompt, length=int(os.environ["LENGTH"]))[0]
    if result.split('\n')[0].strip() != "":
        result = prompt + result
    result = result.strip()
    print('predicted:', result, sep='\n')
    return result


def main():
    evaluator = create_evaluator()
    predict(evaluator, "Олег")

if __name__ == "__main__":
    main()

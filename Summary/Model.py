import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

def model_load(model_name):
    tokenizer = PreTrainedTokenizerFast.from_pretrained(f"{model_name}/kobart-summarization")
    model = BartForConditionalGeneration.from_pretrained(f"{model_name}/kobart-summarization")
    return model, tokenizer

def preprocessing(text):
    text = text.replace('[[0-9]]', '')
    text = text.replace('\n', ' ')
    text = text.replace('\'', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text[:1024]
    return text

def summarizing(text, model, tokenizer):
    if len(text) < 20:
        return text
    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)
    summarized = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
    return summarized

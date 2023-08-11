from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

MODEL_NAME_OR_PATH = "TheBloke/WizardLM-1.0-Uncensored-Llama2-13B-GPTQ"
DEVICE = "cuda:0"

def download_model() -> tuple:
    """Download the model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH, use_fast=True)
    model = AutoGPTQForCausalLM.from_quantized(MODEL_NAME_OR_PATH,
            use_safetensors=True,
            trust_remote_code=False,
            device="cuda:0",
            use_triton=False,
            quantize_config=None)
    return model, tokenizer

if __name__ == "__main__":
    download_model()
    
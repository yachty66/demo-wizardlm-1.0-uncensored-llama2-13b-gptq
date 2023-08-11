from potassium import Potassium, Request, Response
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

MODEL_NAME_OR_PATH = "TheBloke/WizardLM-1.0-Uncensored-Llama2-13B-GPTQ"
DEVICE = "cuda:0"

app = Potassium("WizardLM-1.0-Uncensored-Llama2-13B-GPTQ")

@app.init
def init() -> dict:
    """Initialize the application with the model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH, use_fast=True)

    model = AutoGPTQForCausalLM.from_quantized(MODEL_NAME_OR_PATH,
            use_safetensors=True,
            trust_remote_code=False,
            device="cuda:0",
            use_triton=False,
            quantize_config=None)

    return {
        "model": model,
        "tokenizer": tokenizer
    }
    
@app.handler()
def handler(context: dict, request: Request) -> Response:
    """Handle a request to generate text from a prompt."""
    model = context.get("model")
    tokenizer = context.get("tokenizer")
    max_new_tokens = request.json.get("max_new_tokens", 512)
    temperature = request.json.get("temperature", 0.7)
    prompt = request.json.get("prompt")
    prompt_template=f'''You are a helpful AI assistant.

    USER: {prompt}
    ASSISTANT:
    '''
    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=temperature, max_new_tokens=max_new_tokens)
    result = tokenizer.decode(output[0])
    return Response(json={"outputs": result}, status=200)

if __name__ == "__main__":
    app.serve()
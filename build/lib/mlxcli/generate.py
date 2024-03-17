from mlx_lm.utils import load, generate_step
import mlx.core as mx
import re
import time

temperature = 0
context_length = 1000
stop_words = ["<|im_start|>", "<|im_end|>", "<s>", "</s>"]

def generate_chat_steps(the_prompt, the_model, tokenizer):
    tokens = []
    skip = 0

    for (token, prob), n in zip(generate_step(mx.array(tokenizer.encode(the_prompt)), the_model, temperature),
                                range(context_length)):

        if token == tokenizer.eos_token_id:
            break

        tokens.append(token.item())
        text = tokenizer.decode(tokens)

        trim = None

        for sw in stop_words:
            if text[-len(sw):].lower() == sw:
                return
            else:
                for i, _ in enumerate(sw, start=1):
                    if text[-i:].lower() == sw[:i]:
                        trim = -i

        yield text[skip:trim]
        skip = len(text)


def convert_chat(messages, role_mapping = None):
    default_role_mapping = {
        "system_prompt": "A chat between a curious user and an artificial intelligence assistant. The assistant follows the given rules no matter what.",
        "system": "ASSISTANT's RULE: ",
        "user": "USER: ",
        "assistant": "ASSISTANT: ",
        "stop": "\n",
    }
    role_mapping = role_mapping if role_mapping is not None else default_role_mapping

    prompt = ""
    for line in messages:
        role_prefix = role_mapping.get(line["role"], "")
        stop = role_mapping.get("stop", "")
        content = line.get("content", "")
        prompt += f"{role_prefix}{content}{stop}"

    prompt += role_mapping.get("assistant", "")
    return prompt.rstrip()

def chat(messages, model, tokenizer, verbose):
    prompt = convert_chat(messages)
    response = ''
    tokens = 0

    start_time = time.time()

    for chunk in generate_chat_steps(prompt, model, tokenizer):
        tokens += 1
        chunk = re.sub(r"^/\*+/", "", chunk)
        chunk = re.sub(r"^:+", "", chunk)
        chunk = chunk.replace('�', '')
        response = response + chunk
        print(chunk, end="", flush=True)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    if verbose: 
        print("\n \n======================")
        print(f"TPS: {round((tokens/execution_time), 2)}tok/s, Execution Time: {round(execution_time,2)}s")
        
    return response

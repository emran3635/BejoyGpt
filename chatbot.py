from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from utils import load_memory, save_memory, translate_text

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

chat_history_ids = None
conversation = load_memory()

print("🤖 MyGPT ready! Type 'exit' to quit. Supports English & Bengali.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        save_memory(conversation)
        break

    user_input_en = translate_text(user_input, dest='en')
    new_input_ids = tokenizer.encode(user_input_en + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids else new_input_ids
    output_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    response = tokenizer.decode(output_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    response_bn = translate_text(response, dest='bn')

    print(f"Chatbot: {response_bn}")
    chat_history_ids = output_ids
    conversation.append({"You": user_input, "Chatbot": response_bn})

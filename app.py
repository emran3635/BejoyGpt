import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from utils import load_memory, save_memory, translate_text

st.set_page_config(page_title="MyGPT", layout="centered")
st.title("🤖 MyGPT — Personal Chatbot (English + Bengali)")

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

if "history" not in st.session_state:
    st.session_state.history = load_memory()
    st.session_state.chat_ids = None

user_input = st.text_input("You:", key="input")

if user_input:
    user_input_en = translate_text(user_input, dest='en')
    new_input_ids = tokenizer.encode(user_input_en + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([st.session_state.chat_ids, new_input_ids], dim=-1) if st.session_state.chat_ids else new_input_ids

    output_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(output_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    response_bn = translate_text(response, dest='bn')

    st.session_state.chat_ids = output_ids
    st.session_state.history.append({"You": user_input, "Chatbot": response_bn})
    save_memory(st.session_state.history)

for chat in reversed(st.session_state.history[-10:]):
    st.markdown(f"**You:** {chat['You']}")
    st.markdown(f"**Chatbot:** {chat['Chatbot']}")

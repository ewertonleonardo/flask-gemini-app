# utils.py

import os
import logging
import json

def load_system_prompt():
    prompt_path = os.path.join(os.getcwd(), 'prompts', 'system_prompt.txt')
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"system_prompt.txt not found at {prompt_path}. Using default prompt.")
        return "Você é um assistente útil."

def load_faq():
    faq_path = os.path.join(os.getcwd(), 'prompts', 'faq.txt')
    try:
        with open(faq_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"faq.txt not found at {faq_path}.")
        return ""

def is_question_about_goformance(pergunta):
    keywords = ['goformance', 'serviços', 'agência', 'marketing', 'empresa']
    return any(keyword in pergunta.lower() for keyword in keywords)

def save_conversation(session_id, historico):
    directory = 'conversations'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, f"{session_id}.json")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Erro ao salvar a conversa: {e}")

def load_conversation(session_id):
    filepath = os.path.join('conversations', f"{session_id}.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar a conversa: {e}")
            return []
    return []

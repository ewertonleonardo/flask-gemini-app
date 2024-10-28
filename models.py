# models.py

import os
import logging
import google.generativeai as genai
from groq import Groq
import markdown
import bleach
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Obtain API keys
GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODELO_SELECIONADO = os.getenv('MODELO_SELECIONADO', 'gemini').lower()

# LLM Parameters
TEMPERATURA = float(os.getenv('TEMPERATURA', 0.1))
MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', 8192))
TOP_P = float(os.getenv('TOP_P', 1.0))
TOP_K = int(os.getenv('TOP_K', 1))

# Configure LLM clients
if GEMINI_API_KEY and MODELO_SELECIONADO == 'gemini':
    genai.configure(api_key=GEMINI_API_KEY)
    groq_client = None
elif GROQ_API_KEY and MODELO_SELECIONADO == 'groq':
    groq_client = Groq(api_key=GROQ_API_KEY)
    genai = None
else:
    groq_client = None
    genai = None
    logging.error("No valid API key or model selected.")

def gerar_resposta_com_gemini(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        generation_config = genai.types.GenerationConfig(
            temperature=TEMPERATURA,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            top_p=TOP_P,
            top_k=TOP_K
        )
        response = model.generate_content(
            prompt_text, generation_config=generation_config
        )
        return response.text.strip()
    except Exception as e:
        logging.error(f"Erro ao gerar resposta com Gemini: {e}")
        return 'Desculpe, ocorreu um erro ao gerar a resposta.'

def gerar_resposta_com_groq(prompt_text):
    try:
        if groq_client is None:
            raise ValueError("Cliente Groq não está configurado.")
        stream = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt_text}
            ],
            model="llama3-8b-8192",
            temperature=TEMPERATURA,
            max_tokens=MAX_OUTPUT_TOKENS,
            top_p=TOP_P,
            stop=None,
            stream=True,
        )
        resposta = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                resposta += chunk.choices[0].delta.content
        return resposta.strip()
    except Exception as e:
        logging.error(f"Erro ao gerar resposta com Groq: {e}")
        return 'Desculpe, ocorreu um erro ao gerar a resposta.'

def gerar_resposta(pergunta, historico_conversa, system_prompt, faq_content):
    # Limit the history to a maximum number of messages
    max_messages = 5
    historico_conversa = historico_conversa[-max_messages*2:]

    # Build the conversation history to include in the prompt
    historico_texto = ''
    for entrada in historico_conversa:
        if entrada['tipo'] == 'user':
            historico_texto += f"Usuário: {entrada['conteudo']}\n"
        else:
            historico_texto += f"Assistente: {entrada['conteudo']}\n"

    # Check if the question is about Goformance
    if is_question_about_goformance(pergunta):
        prompt_text = f"{system_prompt}\n\n{faq_content}\n\n{historico_texto}\nUsuário: {pergunta}\nAssistente:"
    else:
        prompt_text = f"{system_prompt}\n\n{historico_texto}\nUsuário: {pergunta}\nAssistente:"

    logging.debug(f"Prompt enviado ao modelo ({MODELO_SELECIONADO}):\n{prompt_text}")

    # Generate response based on the selected model
    if MODELO_SELECIONADO == "gemini" and GEMINI_API_KEY:
        resposta_markdown = gerar_resposta_com_gemini(prompt_text)
    elif MODELO_SELECIONADO == "groq" and GROQ_API_KEY:
        resposta_markdown = gerar_resposta_com_groq(prompt_text)
    else:
        logging.error(f"Modelo desconhecido ou chave de API não configurada: {MODELO_SELECIONADO}")
        return "Modelo desconhecido ou chave de API não configurada."

    # Convert Markdown to HTML
    resposta_html = markdown.markdown(resposta_markdown)
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
        ['p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']
    )
    resposta_html = bleach.clean(resposta_html, tags=allowed_tags, strip=True)
    return resposta_html

# Import the function to avoid circular imports
from utils import is_question_about_goformance

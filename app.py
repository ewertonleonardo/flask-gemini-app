from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import google.generativeai as genai
import markdown
import bleach
import secrets
import logging
from datetime import datetime
from dotenv import load_dotenv
import os
from groq import Groq

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as chaves de API do Gemini e Groq
GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY', None)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Selecionar o modelo a ser usado: 'gemini' ou 'groq'
MODELO_SELECIONADO = os.getenv('MODELO_SELECIONADO', 'gemini').lower()

# Prioridade: Configurar a biblioteca do Google se a chave do Gemini estiver disponível e o modelo selecionado for 'gemini'
if GEMINI_API_KEY is not None and MODELO_SELECIONADO == 'gemini':
    genai.configure(api_key=GEMINI_API_KEY)
    groq_client = None
# Configurar o cliente do Groq se a chave do Groq estiver disponível e o modelo selecionado for 'groq'
elif GROQ_API_KEY and MODELO_SELECIONADO == 'groq':
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    GEMINI_API_KEY = None
    GROQ_API_KEY = None
    groq_client = None
    raise ValueError("Nenhuma API Key habilitada ou modelo inválido selecionado. Verifique o arquivo .env para as chaves de API do Gemini ou do Groq.")

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# Configuração de Logging para facilitar a depuração
logging.basicConfig(level=logging.DEBUG)

# Função para carregar o prompt de sistema a partir do arquivo
def load_system_prompt():
    prompt_path = os.path.join(os.getcwd(), 'prompts', 'system_prompt.txt')
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Arquivo system_prompt.txt não encontrado em {prompt_path}. Usando prompt padrão.")
        return "Você é um assistente útil."

# Função para carregar o FAQ
def load_faq():
    faq_path = os.path.join(os.getcwd(), 'prompts', 'faq.txt')
    try:
        with open(faq_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Arquivo faq.txt não encontrado em {faq_path}.")
        return ""

# Carregar o system_prompt e o FAQ
system_prompt = load_system_prompt()
faq_content = load_faq()

# Obter parâmetros do LLM do .env
TEMPERATURA = float(os.getenv('TEMPERATURA', 0.1))
MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', 8192))
TOP_P = float(os.getenv('TOP_P', 1.00))
TOP_K = int(os.getenv('TOP_K', 1))

# Função para verificar se a pergunta é sobre a Goformance
def is_question_about_goformance(pergunta):
    keywords = ['goformance', 'serviços', 'agência', 'marketing', 'empresa']
    return any(keyword in pergunta.lower() for keyword in keywords)

def gerar_resposta_com_gemini(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        generation_config = genai.types.GenerationConfig(
            temperature=TEMPERATURA,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            top_p=TOP_P,
            top_k=TOP_K
        )
        response = model.generate_content(prompt_text, generation_config=generation_config)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Erro ao gerar resposta com Gemini: {e}")
        return f'Desculpe, ocorreu um erro ao gerar a resposta: {str(e)}'

def gerar_resposta_com_groq(prompt_text):
    try:
        if groq_client is None:
            raise ValueError("Cliente Groq não está configurado.")
        stream = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt_text,
                }
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
        return f'Desculpe, ocorreu um erro ao gerar a resposta: {str(e)}'

# Função para gerar a resposta, escolhendo entre Gemini e Groq
def gerar_resposta(pergunta, historico_conversa):
    # Limitar o histórico a um número máximo de mensagens
    max_messages = 5
    historico_conversa = historico_conversa[-max_messages*2:]

    # Construir o histórico da conversa para incluir no prompt
    historico_texto = ''
    for entrada in historico_conversa:
        if entrada['tipo'] == 'user':
            historico_texto += f"Usuário: {entrada['conteudo']}\n"
        else:
            historico_texto += f"Assistente: {entrada['conteudo']}\n"

    # Verificar se a pergunta é sobre a Goformance
    if is_question_about_goformance(pergunta):
        prompt_text = f"{system_prompt}\n\n{faq_content}\n\n{historico_texto}\n\nPergunta: {pergunta}\nResposta em Markdown:"
    else:
        prompt_text = f"{system_prompt}\n\n{historico_texto}\n\nPergunta: {pergunta}\nResposta em Markdown:"

    logging.debug(f"Prompt enviado ao modelo ({MODELO_SELECIONADO}):\n{prompt_text}")

    if MODELO_SELECIONADO == "gemini" and GEMINI_API_KEY:
        return gerar_resposta_com_gemini(prompt_text)
    elif MODELO_SELECIONADO == "groq" and GROQ_API_KEY:
        return gerar_resposta_com_groq(prompt_text)
    else:
        logging.error(f"Modelo desconhecido ou chave de API não configurada: {MODELO_SELECIONADO}")
        return "Modelo desconhecido ou chave de API não configurada. Por favor, escolha entre 'gemini' e 'groq'."

def obter_resposta(pergunta):
    if not pergunta:
        return "Por favor, faça uma pergunta."

    # Incluir histórico da conversa
    historico_conversa = session.get('historico', [])

    resposta_markdown = gerar_resposta(pergunta, historico_conversa)
    resposta_html = markdown.markdown(resposta_markdown)
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(['p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
    resposta_html = bleach.clean(resposta_html, tags=allowed_tags, strip=True)
    return resposta_html

MAX_HISTORICO = 20  # Ajuste conforme necessário

@app.route('/', methods=['GET'])
def chat():
    session['historico'] = []  # Limpar o histórico ao recarregar a página
    timestamp = datetime.now().strftime("%H:%M")
    return render_template('index.html', timestamp=timestamp)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    pergunta = data.get('pergunta', '').strip()

    logging.info(f"Pergunta recebida: {pergunta} (Modelo: {MODELO_SELECIONADO})")

    if not pergunta:
        return jsonify({'erro': 'Por favor, faça uma pergunta.'})

    session['historico'] = session.get('historico', [])
    session['historico'].append({'tipo': 'user', 'conteudo': pergunta})
    session.modified = True

    resposta = obter_resposta(pergunta)

    # Adicionar a resposta do assistente ao histórico
    session['historico'].append({'tipo': 'assistant', 'conteudo': resposta})
    session.modified = True

    # Limitar o histórico geral
    if len(session['historico']) > MAX_HISTORICO:
        session['historico'] = session['historico'][-MAX_HISTORICO:]
        session.modified = True

    logging.info(f"Resposta enviada: {resposta}")

    return jsonify({'resposta': resposta})

@app.route('/limpar', methods=['POST'])
def limpar():
    session.pop('historico', None)
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
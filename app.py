# app.py

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import google.generativeai as genai
import markdown
import bleach
import secrets
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave de API do Gemini
GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')  # Alinhado com o .env

if GEMINI_API_KEY is None:
    raise ValueError("A chave de API do Gemini não foi encontrada. Verifique o arquivo .env.")

# Configurar a biblioteca do Google
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))  # Chave secreta para as sessões

# Configuração de Logging para facilitar a depuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # Nível INFO e formatação

# Definir uma função para carregar o prompt de sistema a partir do arquivo
def load_system_prompt():
    prompt_path = os.path.join(os.getcwd(), 'prompts', 'system_prompt.txt')
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Arquivo system_prompt.txt não encontrado em {prompt_path}. Usando prompt padrão.")
        return "Você é um assistente útil."

# Inicializa o prompt system
system_prompt = load_system_prompt()

# Obter temperatura do .env
TEMPERATURA = float(os.getenv('TEMPERATURA', 0.5))  # Valor padrão 0.5

# Implementação do cache (se necessário)
score_cache = {}

def gerar_resposta(pergunta, historico_conversa):
    # Definir parâmetros do modelo
    temperatura = TEMPERATURA  # Temperatura configurável

    # Limitar o histórico a um número máximo de mensagens
    max_messages = 10  # Aumentado para manter mais contexto
    historico_conversa = historico_conversa[-max_messages*2:]  # Mantém as últimas N mensagens

    # Construir o histórico da conversa para incluir no prompt com roles usando f-strings
    historico_texto = ''
    for entrada in historico_conversa:
        if entrada['tipo'] == 'user':
            historico_texto += f"User: {entrada['conteudo']}\n"
        else:
            historico_texto += f"Assistant: {entrada['conteudo']}\n"

    prompt_text = f"{system_prompt}\n\n{historico_texto}\nUser: {pergunta}\nAssistant:"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        generation_config = genai.types.GenerationConfig(
            temperature=temperatura
        )
        response = model.generate_content(prompt_text, generation_config=generation_config)
        return response.text.strip()
    except genai.APIError as e: # Tratar erros específicos da API Gemini
        logging.error(f"Erro na API Gemini: {e}")
        return f'Desculpe, ocorreu um erro na API Gemini: {str(e)}'
    except ValueError as e: # Tratar ValueErrors, como erros de configuração
        logging.error(f"Erro de valor: {e}")
        return f'Desculpe, ocorreu um erro de valor: {str(e)}'
    except Exception as e: # Captura outras exceções genéricas
        logging.error(f"Erro ao gerar resposta: {e}", exc_info=True) # Loga detalhes da exceção
        return f'Desculpe, ocorreu um erro inesperado ao gerar a resposta.'

def obter_resposta(pergunta):
    if not pergunta:
        return "Por favor, faça uma pergunta."

    # Incluir histórico da conversa
    historico_conversa = session.get('historico', [])

    # Gerar resposta usando a API do Google Gemini
    resposta_markdown = gerar_resposta(pergunta, historico_conversa)
    resposta_html = markdown.markdown(resposta_markdown)
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(['p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    resposta_html = bleach.clean(resposta_html, tags=allowed_tags, strip=True)
    return resposta_html

MAX_HISTORICO = 100  # Aumentado para permitir mais mensagens no histórico geral

@app.route('/', methods=['GET'])
def chat():
    if 'historico' not in session:
        session['historico'] = []
    timestamp = datetime.now().strftime("%H:%M")
    return render_template('index.html', timestamp=timestamp)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    pergunta = data.get('pergunta', '').strip()

    logging.info(f"Pergunta recebida: {pergunta}")

    if not pergunta: # Validação da pergunta no backend
        return jsonify({'erro': 'Por favor, faça uma pergunta.'})

    session['historico'] = session.get('historico', [])
    session['historico'].append({'tipo': 'user', 'conteudo': pergunta})

    # Adicionar a mensagem "Respondendo..." com animação
    session['historico'].append({'tipo': 'assistant', 'conteudo': 'Respondendo<span class="dot-animated"></span>'})
    session.modified = True

    resposta = obter_resposta(pergunta)

    # Atualizar a mensagem "Respondendo..." com a resposta real
    session['historico'] = session['historico'][:-1]
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

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Obtém a porta do ambiente ou usa 5000 como padrão
    app.run(host='0.0.0.0', port=port)  # Escuta em todas as interfaces de rede

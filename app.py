# app.py
import os
from flask import Flask, render_template, request, session, jsonify, redirect
from dotenv import load_dotenv
import markdown
import bleach
import logging
import json
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Read API key and parameters
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
TEMPERATURA = float(os.getenv('TEMPERATURA', 0.3))
MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', 256))
TOP_P = float(os.getenv('TOP_P', 1.0))
TOP_K = int(os.getenv('TOP_K', 1))

# Configure the generative AI client
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Read the system prompt
try:
    with open('prompts/system_prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
except FileNotFoundError:
    system_prompt = ""  # Or provide a default prompt
    logging.error("system_prompt.txt not found. Please ensure the file exists.")

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random secret key

@app.route('/')
def index():
    if 'historico' not in session:
        session['historico'] = []
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    pergunta = data.get('pergunta', '').strip()
    if not pergunta:
        return jsonify({'erro': 'Pergunta vazia.'})

    # Log pergunta no terminal
    print(f"Pergunta do usuário: {pergunta}")

    # Append user's message to history
    historico = session.get('historico', [])

    # Add system prompt as the first user message, if not added already
    if system_prompt and not historico:
        historico.append({'role': 'user', 'parts': [system_prompt]})

    # Add user's question to history
    mensagem_usuario = {'role': 'user', 'parts': [pergunta]}
    historico.append(mensagem_usuario)
    session['historico'] = historico

    # Log prompt enviado ao modelo
    prompt_para_envio = json.dumps(historico, ensure_ascii=False)
    logging.info(f"Prompt enviado ao modelo: {prompt_para_envio}")

    # Create the model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Start chat
    chat = model.start_chat(
        history=historico
    )

    # Send the user's message with generation configuration
    try:
        response = chat.send_message(
            pergunta,
            generation_config=genai.GenerationConfig(
                temperature=TEMPERATURA,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                top_p=TOP_P,
                top_k=TOP_K
            )
        )

        # Get the assistant's reply in markdown format
        resposta_markdown = response.text

        # Log resposta do modelo no terminal e no arquivo de log
        print(f"Resposta do modelo: {resposta_markdown}")
        logging.info(f"Resposta recebida do modelo: {resposta_markdown}")

        # Convert markdown to HTML
        resposta_html = markdown.markdown(resposta_markdown)

        # Sanitize the HTML to allow specific tags for formatting
        allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
            ['p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'a', 'br']
        )
        resposta_html = bleach.clean(
            resposta_html,
            tags=allowed_tags,
            attributes={'a': ['href']},
            strip=True
        )

        # Append assistant's message to history
        mensagem_assistente = {'role': 'model', 'parts': [resposta_html]}
        historico.append(mensagem_assistente)
        session['historico'] = historico

        return jsonify({'resposta': resposta_html})

    except Exception as e:
        logging.error("Erro ao tentar enviar mensagem ao modelo.", exc_info=True)
        return jsonify({'erro': 'Erro ao obter resposta do modelo.'})

@app.route('/limpar', methods=['POST'])
def limpar():
    session.clear()
    return redirect('/')

#if __name__ == '__main__':
#    app.run(debug=True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Obtém a porta do ambiente ou usa 5000 como padrão
    app.run(host='0.0.0.0', port=port)  # Escuta em todas as interfaces de rede
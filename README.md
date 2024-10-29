
# Aplicativo Flask com Integração ao Google Gemini API

Este é um aplicativo web desenvolvido com Flask para interagir com o modelo **Gemini 1.5 Flash** da API de Inteligência Artificial Generativa da Google. A aplicação permite que os usuários façam perguntas e recebam respostas geradas pela IA, com uma interface em HTML e configuração de variáveis de geração de conteúdo para controle de temperatura, tokens de saída, e outros parâmetros.

## Requisitos

- Python 3.8+
- Biblioteca do Google Gemini para Python
- Flask
- dotenv para gerenciamento de variáveis de ambiente
- bleach para sanitização de HTML
- markdown para renderização de texto em markdown

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto com o conteúdo:
   ```env
   GOOGLE_GEMINI_API_KEY=your_api_key
   TEMPERATURA=0.3
   MAX_OUTPUT_TOKENS=256
   TOP_P=1.0
   TOP_K=1
   ```

   Substitua `your_api_key` pela sua chave de API obtida no [Google AI Studio](https://aistudio.google.com/).

4. Adicione o prompt inicial:
   - Crie um arquivo `prompts/system_prompt.txt` e insira o texto desejado para o prompt inicial que o modelo deve considerar ao responder.

## Uso

1. Inicie o servidor Flask:
   ```bash
   python app.py
   ```

2. Acesse `http://localhost:5000` no seu navegador para abrir a interface do aplicativo.

## Funcionalidades

### Endpoints

- **`/`**: Renderiza a interface principal para entrada de perguntas.
- **`/get_response`**: Recebe uma pergunta via JSON (usada pelo front-end) e retorna a resposta do modelo em HTML.
- **`/limpar`**: Limpa o histórico de sessão e redireciona para a página inicial.

### Configuração da Geração

- **Temperatura (`TEMPERATURA`)**: Define a "criatividade" das respostas do modelo. Valores mais altos (até 1) tornam as respostas mais diversas.
- **Máximo de Tokens de Saída (`MAX_OUTPUT_TOKENS`)**: Limita o número de tokens na resposta gerada.
- **`TOP_P` e `TOP_K`**: Ajustam a amostra dos tokens mais prováveis. TOP_P controla o somatório de probabilidades, e TOP_K restringe o número de tokens considerados na amostra.

### Segurança e Sanitização

Para segurança, a resposta do modelo em Markdown é convertida para HTML e sanitizada com a biblioteca `bleach`, restringindo tags permitidas para proteger contra ataques XSS.

## Arquitetura

- **Flask**: Gerencia as rotas e a lógica de sessão do usuário.
- **Google Generative AI SDK**: Interage com o modelo Gemini 1.5 Flash, usando sessões de chat para manter o contexto da conversa.
- **dotenv**: Gerencia variáveis de ambiente com segurança.
- **Markdown e Bleach**: Processa e sanitiza a resposta da IA antes de exibi-la na interface web.

## Erros e Logging

As respostas e erros são registrados no arquivo `app.log`. Para resolver problemas comuns:
- Verifique o log para mensagens detalhadas de erro.
- Confirme se o `GOOGLE_GEMINI_API_KEY` é válido e está corretamente definido no `.env`.

## Licença

Este projeto é licenciado sob a licença MIT.

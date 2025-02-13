# SEO Mentor Chatbot

## Descrição

Este projeto consiste em um chatbot web desenvolvido utilizando Python com o framework Flask e a API Gemini do Google. O chatbot é projetado para atuar como um **Mentor de SEO altamente especializado**, capaz de auxiliar usuários no aprendizado de **SEO Técnico, OnPage e OffPage**.

O objetivo principal deste chatbot é fornecer mentoria e orientação em SEO, cobrindo todos os aspectos essenciais para um profissional de SEO completo, desde o nível júnior até o C-Level. O chatbot utiliza o modelo de linguagem Gemini para explicar conceitos complexos de SEO de forma acessível, oferecer feedback personalizado e inspirar os alunos a alcançar seu pleno potencial na área de SEO.

**Funcionalidades Essenciais:**

- **Interface de Chat Web:** Interface de usuário interativa para conversas em tempo real com o mentor de SEO.
- **Integração com Google Gemini API:** Utiliza o modelo de linguagem Gemini para fornecer explicações detalhadas, exemplos práticos e feedback em SEO.
- **Mentoria em SEO Técnico:** Explica táticas de SEO Técnico, como otimização de velocidade, arquitetura de site, dados estruturados e indexação.
- **Mentoria em SEO OnPage:** Demonstra estratégias de SEO OnPage, incluindo pesquisa de palavras-chave, otimização de meta tags e criação de conteúdo.
- **Mentoria em SEO OffPage:** Apresenta abordagens de SEO OffPage, como link building e gestão de reputação online.
- **Feedback Personalizado:** Oferece feedback baseado em métricas de SEO e ferramentas como Google Search Console, SEMrush, etc.
- **Estilo de Comunicação Envolvente:** Utiliza analogias, exemplos práticos e perguntas instigantes para facilitar o aprendizado.
- **Indicação de Recursos Complementares:** Sugere guias oficiais, ferramentas, vídeos e comunidades para aprendizado contínuo em SEO.

## Instruções de Instalação

Siga estes passos para instalar e executar o chatbot SEO Mentor:

1. **Clone o repositório:**

    ```bash
    git clone [URL do repositório]
    cd flask-gemini-app
    ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python -m venv venv
    ```

3. **Ative o ambiente virtual:**
    - **No Windows:**

        ```bash
        venv\\Scripts\\activate
        ```

    - **No Linux/macOS:**

        ```bash
        source venv/bin/activate
        ```

4. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configure as variáveis de ambiente:**
    - Crie um arquivo `.env` na raiz do projeto.
    - Adicione as seguintes variáveis, substituindo `SUA_CHAVE_API_GEMINI` e `SUA_CHAVE_SECRETA_FLASK` pelas suas chaves reais:

        ```env
        GOOGLE_GEMINI_API_KEY=SUA_CHAVE_API_GEMINI
        FLASK_SECRET_KEY=SUA_CHAVE_SECRETA_FLASK
        ```

        - **`GOOGLE_GEMINI_API_KEY`:**  Obtenha sua chave API no [Google AI Studio](https://makersuite.google.com/).
        - **`FLASK_SECRET_KEY`:**  Gere uma chave secreta forte para o Flask. Pode usar `secrets.token_hex(16)` em Python para gerar uma.

    - **Opcional:** Configure a temperatura do modelo Gemini (padrão é 0.5):

        ```env
        TEMPERATURA=0.7
        ```

## Guia de Uso

1. **Execute a aplicação Flask:**

    ```bash
    python app.py
    ```

2. **Acesse o Chatbot no Navegador:**
    Abra seu navegador web e acesse o endereço `http://127.0.0.1:10000/` ou a porta que for exibida no terminal ao executar a aplicação.

3. **Interaja com o Chatbot Mentor de SEO:**
    Na interface web, faça perguntas sobre SEO, peça explicações sobre conceitos, solicite feedback sobre suas estratégias ou peça recomendações de recursos de aprendizado. O chatbot SEO Mentor irá guiá-lo em sua jornada de aprendizado em SEO.

4. **Limpar Histórico:**
    Clique no botão "Limpar" para apagar o histórico de conversas da sessão atual.

## Diretrizes de Contribuição

Contribuições são bem-vindas! Se você deseja contribuir para este projeto, siga estas diretrizes:

1. **Fork o repositório.**
2. **Crie um branch para sua feature ou correção de bug:** `git checkout -b feature/nova-feature` ou `git checkout -b fix/correcao-bug`.
3. **Faça suas modificações e commits:** `git commit -m "Adiciona nova feature"`.
4. **Envie suas mudanças para o seu fork:** `git push origin feature/nova-feature`.
5. **Abra um Pull Request** para o repositório principal.

## Licença

Este projeto é distribuído sob a licença [MIT License](./LICENSE).

## Créditos

Desenvolvido por: [Ewerton Leonardo](https://www.linkedin.com/in/ewertonleonardoap/)

---
Este `README.md` foi gerado por Roo, um assistente de engenharia de software.

# Mentor de SEO Chatbot

## Descrição Detalhada

Este projeto consiste em um chatbot interativo projetado para atuar como um mentor de SEO (Otimização para Mecanismos de Busca). O chatbot utiliza o modelo de linguagem Gemini 1.5 Flash do Google Generative AI para fornecer respostas e orientações sobre diversos tópicos de SEO, desde SEO técnico e On-Page até estratégias Off-Page.

**Objetivo:**

O principal objetivo deste chatbot é facilitar o aprendizado de SEO de forma interativa e personalizada. Ele simula uma conversa com um mentor experiente, permitindo que usuários façam perguntas e recebam explicações, dicas e exemplos práticos sobre SEO.

**Problema Solucionado:**

O aprendizado de SEO pode ser complexo e desafiador, especialmente para iniciantes. Recursos online são abundantes, mas muitas vezes falta uma abordagem interativa e personalizada. Este chatbot visa solucionar essa dificuldade, oferecendo um ambiente de aprendizado dinâmico onde os usuários podem obter respostas para suas dúvidas de SEO de maneira rápida e acessível.

**Funcionalidades Essenciais:**

*   **Chat Interativo:** Interface de chat amigável para conversas em tempo real com o mentor de SEO.
*   **Persona de Mentor de SEO:** O chatbot é configurado com um prompt de sistema para atuar como um especialista em SEO, fornecendo respostas relevantes e úteis.
*   **Respostas em Markdown:** As respostas do chatbot são formatadas em Markdown, permitindo a inclusão de títulos, listas, links e blocos de código para melhor clareza e organização.
*   **Histórico de Conversas:** O histórico de conversas é persistido usando sessões Flask, permitindo que os usuários revisitem interações anteriores durante a mesma sessão.
*   **Interface Web Responsiva:** A interface web é projetada para ser responsiva e funcionar bem em diferentes dispositivos (desktops, tablets e smartphones).
*   **Validação e Sanitização:** Validação de perguntas no backend para garantir que perguntas vazias não sejam processadas. Sanitização de HTML nas respostas para segurança.
*   **Tratamento de Erros:** Tratamento robusto de erros, incluindo erros específicos da API Gemini, para fornecer mensagens de erro amigáveis e logs detalhados para depuração.
*   **Configuração Flexível:** Temperatura do modelo Gemini configurável via variável de ambiente para ajustar a criatividade e aleatoriedade das respostas.

**Público-Alvo:**

*   Estudantes de SEO e marketing digital.
*   Profissionais de marketing digital iniciantes.
*   Empreendedores e proprietários de pequenos negócios que desejam aprender SEO para melhorar a visibilidade online de seus negócios.
*   Qualquer pessoa interessada em aprender os fundamentos e estratégias de SEO de forma prática e interativa.

## Tecnologias Empregadas

*   **Backend:**
    *   [Python](https://www.python.org/) - Linguagem de programação principal.
    *   [Flask](https://flask.palletsprojects.com/) - Framework web para construir a aplicação backend e API.
    *   [Google Generative AI Python SDK](https://pypi.org/project/google-generativeai/) - Biblioteca para interagir com os modelos Gemini do Google.
    *   [python-dotenv](https://pypi.org/project/python-dotenv/) - Para carregar variáveis de ambiente a partir de arquivos `.env`.
    *   [markdown](https://pypi.org/project/Markdown/) - Para converter texto Markdown em HTML.
    *   [bleach](https://pypi.org/project/bleach/) - Para sanitizar HTML e remover tags indesejadas por segurança.

*   **Frontend:**
    *   HTML5 - Estrutura da página web.
    *   CSS3 - Estilização da interface do usuário (`static/css/style.css`).
    *   [JavaScript](https://www.javascript.com/) - Para interatividade no frontend (`static/js/chat.js` e [jQuery](https://jquery.com/)).
    *   [jQuery](https://jquery.com/) - Biblioteca JavaScript para manipulação do DOM e requisições AJAX.
    *   [Font Awesome](https://fontawesome.com/) - Biblioteca de ícones para a interface.

## Instruções de Instalação

**Pré-requisitos:**

*   [Python](https://www.python.org/downloads/) (versão 3.x recomendada) instalado.
*   [pip](https://pip.pypa.io/en/stable/installation/) (gerenciador de pacotes do Python) instalado.

**Passos:**

1.  **Clone o repositório:**

    ```bash
    git clone [URL do repositório]
    cd [nome do repositório]
    ```

2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    # source venv/bin/activate  # No Linux/macOS
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

    *   Crie um arquivo `.env` na raiz do projeto.
    *   Adicione as seguintes variáveis ao arquivo `.env`:

        ```
        GOOGLE_GEMINI_API_KEY=SUA_CHAVE_DE_API_GEMINI
        FLASK_SECRET_KEY=uma_chave_secreta_segura  # Opcional (gerado automaticamente se não fornecida)
        TEMPERATURA=0.5                             # Opcional (valor padrão 0.5)
        PORT=10000                                  # Opcional (valor padrão 10000)
        ```

        Substitua `SUA_CHAVE_DE_API_GEMINI` pela sua chave de API do Gemini. Você pode obter uma chave de API no [Google AI Studio](https://makersuite.google.com/).

        `FLASK_SECRET_KEY` é usado para segurança das sessões do Flask. Se não for fornecido, uma chave secreta aleatória será gerada a cada inicialização.

        `TEMPERATURA` controla a aleatoriedade das respostas do modelo Gemini. Valores mais baixos (próximos de 0) tornam as respostas mais determinísticas e focadas, enquanto valores mais altos (próximos de 1) tornam as respostas mais criativas e aleatórias. O valor padrão é 0.5.

        `PORT` define a porta em que o aplicativo Flask será executado. O valor padrão é 10000.

5.  **Execute o aplicativo:**

    ```bash
    python app.py
    ```

6.  **Acesse o aplicativo no seu navegador:**

    Abra o navegador e acesse o endereço `http://localhost:10000` ou `http://127.0.0..1:10000`.

## Guia de Uso

Ao acessar o aplicativo no navegador, você verá a interface do Mentor de SEO Chatbot. A interface é composta por:

*   **Título:** "Mentor de SEO - By Ewerton" (ou título similar).
*   **Botão "Limpar":** Limpa o histórico de conversas da sessão atual.
*   **Histórico de Chat:** Exibe as mensagens trocadas entre o usuário e o sistema. Mensagens do usuário são exibidas em balões azuis ("Usuário"), e mensagens do sistema (chatbot) em balões verdes ("Sistema").
*   **Barra de Entrada de Mensagem:** Um campo de texto (`textarea`) onde você pode digitar suas perguntas ou mensagens para o chatbot.
*   **Botão "Enviar":** Envia a mensagem digitada para o chatbot. Você também pode pressionar a tecla "Enter" (sem Shift) para enviar a mensagem.

**Exemplos de Perguntas:**

Você pode fazer perguntas sobre diversos tópicos de SEO, como:

*   **SEO Técnico:**
    *   "O que é canonical tag e como usar?"
    *   "Como otimizar a velocidade de carregamento do meu site?"
    *   "O que é mobile-first indexing?"
*   **SEO On-Page:**
    *   "Como escolher as palavras-chave certas para o meu nicho?"
    *   "Como otimizar títulos e meta descrições?"
    *   "Quais são as melhores práticas para criar conteúdo otimizado para SEO?"
*   **SEO Off-Page:**
    *   "O que é link building e como conseguir backlinks de qualidade?"
    *   "Como usar as redes sociais para SEO?"
    *   "O que é guest blogging?"
*   **Estratégias de SEO:**
    *   "Como criar uma estratégia de SEO para um novo site?"
    *   "Como analisar o desempenho de SEO do meu site?"
    *   "Quais são as tendências de SEO para 2024?"

Sinta-se à vontade para explorar e fazer perguntas sobre qualquer tópico relacionado a SEO. O chatbot está pronto para te ajudar a aprender e aprofundar seus conhecimentos!

## Diretrizes de Contribuição

Contribuições são bem-vindas! Se você tiver ideias para melhorar o chatbot, adicionar funcionalidades, corrigir bugs ou aprimorar a documentação, sinta-se à vontade para contribuir.

**Como Contribuir:**

1.  Faça um fork do repositório.
2.  Crie uma branch com sua feature ou correção de bug (`git checkout -b minha-feature`).
3.  Faça as alterações e commit (`git commit -m 'Adiciona nova feature...'`).
4.  Envie para sua branch (`git push origin minha-feature`).
5.  Abra um pull request.

Por favor, siga as boas práticas de programação e o guia de estilo PEP 8 para Python ao contribuir com código Python.

## Licença

**Todos os direitos reservados.**

Este projeto é de código fechado e todos os direitos são reservados ao autor. Nenhuma parte deste projeto pode ser reproduzida, distribuída ou modificada sem permissão expressa do autor, a menos que especificado de outra forma em uma licença comercial.

## Créditos e Agradecimentos

*   Desenvolvido por [Seu Nome/Nome do Desenvolvedor] ([link para seu perfil/site, opcional]).
*   Utiliza a API Gemini do Google Generative AI.
*   Agradecimentos às bibliotecas de código aberto [Flask](https://flask.palletsprojects.com/), [python-dotenv](https://pypi.org/project/python-dotenv/), [Markdown](https://pypi.org/project/Markdown/), [bleach](https://pypi.org/project/bleach/), [jQuery](https://jquery.com/), [Font Awesome](https://fontawesome.com/) e outras bibliotecas mencionadas na seção "Tecnologias Empregadas".

---

*Última atualização: 13 de fevereiro de 2025*

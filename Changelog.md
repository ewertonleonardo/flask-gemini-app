# Changelog

Todos as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
e este projeto segue as [Versões Semânticas](https://semver.org/spec/v2.0.0.html).

## [Não Lançado]

### Adicionado

### Modificado

### Deprecado

### Removido

### Corrigido

### Segurança

---

## [0.1.2] - 2025-02-13

### Modificado

- Refatorado `app.py` para incluir tratamento de erros aprimorado (erros específicos da API Gemini, ValueErrors, etc.).
- Refatorado código JavaScript inline de `index.html` para arquivo externo `static/js/chat.js`.
- Melhorada a legibilidade do prompt na função `gerar_resposta()` em `app.py` com o uso de f-strings.
- Adicionada validação da pergunta no backend em `/get_response` em `app.py`.
- Correção informações do `README.md`

### Adicionado

- Criado arquivo `static/js/chat.js` para conter o código JavaScript do frontend.
- Configuração da temperatura do modelo Gemini via variável de ambiente em `app.py`.

## [0.1.1] - 2025-02-12

### Modificado

- Propósito do projeto alterado de SDR Chatbot para SEO Mentor Chatbot.
- Funcionalidade atualizada para focar em mentoria de SEO (Técnico, OnPage, OffPage) em vez de qualificação de leads.
- `README.md` atualizado para refletir o novo propósito e funcionalidades do projeto.

### Adicionado

- Criado arquivo `LICENSE` com a Licença MIT.

## [0.1.0] - 2025-02-12

### Adicionado

- Configuração inicial do projeto como SDR Chatbot.
- Implementada interface web do chatbot usando Flask e HTML/CSS/JavaScript.
- Integrada a API Google Gemini para respostas do chatbot.
- Funcionalidade básica para qualificação de leads para a agência de marketing digital Goformance.

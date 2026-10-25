# 📖 05 — Glossário Técnico (RPA, n8n, Finanças e IA Generativa)

> **Navegação:** [⬅️ Anterior: 04 — Miniestudo RPA, n8n e Python](./04-miniestudo-rpa-n8n-python.md) | [📚 Índice da Documentação](./README.md) | [Próximo: 06 — Arquitetura da Solução ➡️](./06-arquitetura-da-solucao.md)

---

## Tabela de Termos Essenciais (22 Conceitos)

| # | Termo Técnico | Definição Clara e Objetiva | Aplicação Prática neste Projeto |
| :---: | :--- | :--- | :--- |
| 01 | **RPA (Robotic Process Automation)** | Automação de processos repetitivos baseados em regras que simulam a leitura e envio de dados entre sistemas. | Script Python [`src/extrair_clientes.py`](../src/extrair_clientes.py) que coleta clientes do HTML e envia ao n8n. |
| 02 | **Web Scraping** | Extração programática de informações a partir da estrutura DOM de páginas HTML. | Leitura das linhas `#clientes tbody tr` de [`docs/index.html`](./index.html). |
| 03 | **BeautifulSoup (`bs4`)** | Biblioteca Python amplamente utilizada para navegar e extrair dados de árvores HTML e XML. | Utilizada no notebook e no script Python para extrair `nome`, `email`, `saldo` e `perfil`. |
| 04 | **Webhook** | Endpoint HTTP que aguarda notificações ou cargas de dados (`POST`) para iniciar um workflow em tempo real. | Nó inicial do n8n configurado em `POST /Clientes`. |
| 05 | **Respond to Webhook** | Nó do n8n que devolve uma resposta HTTP personalizada ao cliente que chamou o Webhook. | Último nó dos workflows 01 e 02, retornando `HTTP 200 OK` com os clientes processados. |
| 06 | **HTTP Request Node** | Nó nativo do n8n para consumir APIs externas ou baixar arquivos da web. | Baixa a planilha [`docs/data.csv`](./data.csv) hospedada no GitHub Pages da DIO. |
| 07 | **CSV (Comma-Separated Values)** | Formato tabular de texto simples em que colunas são separadas por vírgulas. | Formato da base de opções de investimento (`perfil,produto,minimo,rentabilidade`). |
| 08 | **Merge Node (`combineByPosition`)** | Nó do n8n que une itens vindos de dois ramos paralelos com base na posição do item. | Une o item 0 do `Webhook` (`clientes`) com o item 0 do `Code in JavaScript` (`investimentos`). |
| 09 | **Code Node (`n8n-nodes-base.code`)** | Nó que permite executar JavaScript ou Python para transformações avançadas de dados no n8n. | Utilizado em `Code in JavaScript`, `Code in JavaScript1`, `Code in JavaScript2` e `Code in JavaScript3`. |
| 10 | **Item Splitting (Fan-out)** | Técnica de transformar 1 item contendo um array de $N$ registros em $N$ itens individuais no fluxo do n8n. | Executado em `Code in JavaScript2` (`resultados.map(...)`) para processar 1 e-mail por cliente. |
| 11 | **Expressões Dinâmicas (`{{ $json.* }}`)** | Sintaxe do n8n para interpolar valores do item atual dentro de parâmetros de nós. | Usada em `Message a model`, `If` e `Send a message` (`{{ $json.email_to }}`). |
| 12 | **Referência Cruzada (`$("Nome").all()`)** | Método moderno do n8n para acessar itens produzidos por nós anteriores da execução. | Usado em `Code in JavaScript3` (`$("Code in JavaScript2").all()`) para recuperar os metadados do cliente. |
| 13 | **Suitability (Perfil de Investidor)** | Classificação de tolerância a risco do cliente no mercado financeiro (`Conservador`, `Moderado`, `Arrojado`). | Critério primário de filtragem dos produtos em `Code in JavaScript1`. |
| 14 | **Aporte Mínimo (`minimo`)** | Valor mínimo em reais exigido para aplicar em determinado produto financeiro. | Critério secundário de elegibilidade (`inv.minimo <= saldo_num`). |
| 15 | **Normalização Monetária (`parseBRL`)** | Conversão de textos formatados em moeda (`"R$ 12.500,00"`) para ponto flutuante (`12500`). | Função JavaScript presente em `Code in JavaScript1` e `Code in JavaScript2`. |
| 16 | **Copywriting Rules (`copy_rules`)** | Diretrizes estruturadas de idioma, tom de voz, tamanho e restrições passadas ao LLM. | Objeto anexado em `Code in JavaScript2` proibindo promessas de ganho e garantias. |
| 17 | **LLM (Large Language Model)** | Modelo de inteligência artificial generativa capaz de compreender contexto e redigir textos estruturados. | Modelo `gpt-4o` invocado pelo nó `Message a model`. |
| 18 | **Guardrail Pós-IA** | Camada de código que valida a estrutura JSON retornada pelo LLM antes de enviá-la a sistemas externos. | Implementado em `Code in JavaScript3` com `try/catch` e `JSON.parse()`. |
| 19 | **Fallback Determinístico** | Mecanismo de contingência que gera uma saída válida por regras fixas caso a IA externa falhe. | Modo `fallback_template_seguro` em `Code in JavaScript3`. |
| 20 | **Regex (Expressão Regular)** | Padrão formal de busca e validação de strings. | Padrão `^[^\s@]+@[^\s@]+\.[^\s@]+$` configurado no nó `If` para validar e-mails. |
| 21 | **Gmail OAuth2 (`n8n-nodes-base.gmail`)** | Integração oficial do n8n para envio de e-mails autenticados via conta Google. | Nó `Send a message` acionado na saída `True` do nó `If`. |
| 22 | **Sanitização de Credenciais** | Remoção de chaves de API, IDs de contas e e-mails pessoais antes de exportar JSON para o Git. | Verificada automaticamente por [`tests/validar-workflows.py`](../tests/validar-workflows.py). |

# 📌 01 — Contexto, Problema de Negócio e Objetivos do Desafio

> **Navegação:** [🏠 README Principal](../README.md) | [📚 Índice da Documentação](./README.md) | [Próximo: 02 — Curadoria de Fontes ➡️](./02-curadoria-de-fontes.md)

---

## 1. Apresentação do Desafio Oficial da DIO

Este projeto responde integralmente ao desafio prático da **Digital Innovation One (DIO)**:

> **"Criando um Assistente de Investimentos com RPA e IA Generativa (Processo de RPA com N8N e Python)"**
> Repositório base de referência da DIO: [`digitalinnovationone/dio-lab-assistente-investimentos-rpa-n8n`](https://github.com/digitalinnovationone/dio-lab-assistente-investimentos-rpa-n8n)

Durante as aulas de orientação do desafio, muitos códigos JavaScript intermediários dos nós do **n8n** foram exibidos rapidamente em vídeo sem um repositório gabarito contendo o código-fonte completo daqueles nós. Como consequência natural, ao reproduzir o workflow de 11 nós, alguns blocos permaneceram com o código padrão do n8n (`item.json.myNewField = 1`) ou com sintaxe de código JavaScript inserida dentro de um campo de expressão de prompt.

Este repositório foi construído para entregar **duas conquistas simultâneas**:
1. **A implementação completa do desafio da DIO** (RPA em Python + Workflow MVP + Workflow Completo com IA Generativa e Gmail).
2. **A auditoria técnica e correção integral do workflow original do aluno**, reconstruindo toda a lógica que faltava nos vídeos de orientação e documentando cada correção passo a passo.

---

## 2. O Problema de Negócio no Setor Financeiro

Assessorias de investimentos, corretoras e bancos digitais lidam diariamente com milhares de clientes que possuem saldos disponíveis em conta e perfis de risco distintos (**Conservador**, **Moderado** e **Arrojado**), mas que permanecem com recursos parados por falta de uma recomendação personalizada e tempestiva.

Em cenários reais de instituições financeiras, é comum encontrar duas barreiras técnicas:
1. **Sistemas Legados sem API (Necessidade de RPA):** Os dados cadastrais de clientes (nome, e-mail, saldo em conta e perfil de suitability) muitas vezes estão disponíveis apenas em relatórios web internos ou painéis HTML (`docs/index.html`), exigindo um robô de **RPA (Robotic Process Automation)** em Python para coletar a tabela estruturada.
2. **Cruzamento de Elegibilidade e Conformidade Regulatória (Compliance):** Não basta recomendar qualquer produto da carteira (`docs/data.csv`). O produto precisa respeitar simultaneamente o **perfil de risco do investidor** e o **aporte mínimo exigido** em relação ao saldo disponível, além de gerar uma comunicação clara em português que **jamais prometa ganhos garantidos**.

---

## 3. Objetivo Geral e Objetivos Específicos

### Objetivo Geral
Construir e validar um pipeline fim a fim de **Assistente de Investimentos Automatizado** que extrai dados de clientes de uma página web via **Python (RPA)**, envia os registros via HTTP `POST` para um **Webhook no n8n**, cruza o perfil e o saldo de cada cliente com uma base CSV de produtos financeiros, redige e-mails personalizados com **IA Generativa (OpenAI GPT-4o)** sob regras de compliance e realiza o disparo validado via **Gmail**.

### Objetivos Específicos
- **Completar o script de RPA em Python (`src/extrair_clientes.py` e `src/extrair_clientes.ipynb`):** Ler a tabela HTML `#clientes` com `BeautifulSoup` (e fallback nativo `HTMLParser`) e implementar o envio HTTP `POST` para o Webhook `/Clientes`.
- **Diagnosticar e corrigir os 6 erros do workflow original do aluno:**
  1. Substituir o código placeholder em `Code in JavaScript1` pelo motor de cruzamento `Clientes x Investimentos`.
  2. Corrigir o erro de sintaxe no prompt do nó `Message a model` (`OpenAI`).
  3. Substituir o placeholder em `Code in JavaScript3` pelo parser JSON da resposta da IA com *Guardrail* e *Fallback* determinístico.
  4. Configurar a validação de e-mail por expressão regular (`Regex`) no nó `If`.
  5. Configurar os parâmetros dinâmicos (`sendTo`, `subject`, `message`) no nó `Send a message` (`Gmail`) e conectar a saída `False` do `If` ao `Respond to Webhook`.
  6. Sanitizar credenciais e e-mails pessoais antes do versionamento no GitHub.
- **Entregar tanto a versão MVP quanto a versão Completa:** Disponibilizar o **Workflow 01 (MVP Estático)** e o **Workflow 02 (Completo com IA + Gmail)** em [`workflows/`](../workflows/) e em [`n8n/workflow.json`](../n8n/workflow.json).
- **Garantir Qualidade Verificável:** Validar 100% dos arquivos JSON, conexões, ausência de segredos e regras de recomendação por meio do script [`tests/validar-workflows.py`](../tests/validar-workflows.py).

---

## 4. Comparativo: Requisitos da DIO vs. Entregas deste Repositório

| Etapa Oficial do Roteiro DIO | Status | Onde Encontrar neste Repositório |
| :--- | :---: | :--- |
| **Etapa 1:** Página de Clientes (`docs/index.html`) e CSV (`docs/data.csv`) | ✅ Concluído | [`docs/index.html`](./index.html) e [`docs/data.csv`](./data.csv) |
| **Etapa 2:** Script RPA em Python integrado ao Webhook (`TODO` resolvido) | ✅ Concluído | [`src/extrair_clientes.py`](../src/extrair_clientes.py) e [`src/extrair_clientes.ipynb`](../src/extrair_clientes.ipynb) |
| **Etapa 3 e 4 (MVP):** Workflow n8n com cruzamento CSV e mensagens estáticas | ✅ Concluído | [`workflows/01-assistente-investimentos-mvp/workflow.json`](../workflows/01-assistente-investimentos-mvp/workflow.json) |
| **Etapa 5 (Desafio Extra IA):** Workflow n8n com OpenAI GPT-4o e Gmail corrigido | ✅ Concluído | [`n8n/workflow.json`](../n8n/workflow.json) e [`workflows/02-assistente-investimentos-ia-gmail/workflow.json`](../workflows/02-assistente-investimentos-ia-gmail/workflow.json) |
| **Diferencial Extra 1:** Auditoria forense dos 6 erros do workflow original | ✅ Concluído | [`docs/03-diagnostico-e-correcao-erros.md`](./03-diagnostico-e-correcao-erros.md) |
| **Diferencial Extra 2:** 15 lâminas visuais PNG + 3 diagramas Mermaid + Validador Python | ✅ Concluído | [`assets/`](../assets/) e [`tests/validar-workflows.py`](../tests/validar-workflows.py) |

# 🚀 Workflow 02 — Assistente de Investimentos Completo Corrigido (IA GPT-4o + Gmail)

> **Navegação:** [🏠 README Principal](../../README.md) | [⚙️ Índice de Workflows](../README.md) | [🛠️ Diagnóstico Forense dos 6 Erros](../../docs/03-diagnostico-e-correcao-erros.md)

---

## 📌 Objetivo deste Workflow

Esta é a versão **100% corrigida e validada** do workflow de **11 nós** construído pelo aluno para a **Etapa 5 (Desafio Completo com IA Generativa)** da DIO. O arquivo JSON exportável está disponível tanto em [`workflows/02-assistente-investimentos-ia-gmail/workflow.json`](./workflow.json) quanto no caminho padrão exigido pela DIO em [`n8n/workflow.json`](../../n8n/workflow.json).

---

## 🖼️ Galeria Passo a Passo das Correções (7 Lâminas Didáticas)

### 1. Auditoria e Correção dos 6 Erros do Workflow Original
![Auditoria dos 6 Erros](../../assets/img/02-assistente-ia-gmail/01-visao-geral-e-erros-corrigidos.png)

### 2. Nós 1 a 4: Webhook, HTTP Request, Code in JavaScript e Merge
![Ingestão e Merge](../../assets/img/02-assistente-ia-gmail/02-ingestao-webhook-csv-merge.png)

### 3. Nós 5 e 6: Correção do `Code in JavaScript1` (Cruzamento) & `Code in JavaScript2` (Split)
![Correção Code1 e Code2](../../assets/img/02-assistente-ia-gmail/03-correcao-code1-e-code2.png)

### 4. Nó 7: Correção do Prompt Dinâmico no `Message a model` (`OpenAI GPT-4o`)
![Correção OpenAI](../../assets/img/02-assistente-ia-gmail/04-correcao-openai-message-model.png)

### 5. Nó 8: Correção do `Code in JavaScript3` (Parser JSON + Guardrail + Fallback)
![Correção Code3](../../assets/img/02-assistente-ia-gmail/05-correcao-code3-parser-guardrail.png)

### 6. Nós 9, 10 e 11: Correção do Nó `If` (Regex), `Send a message` (Gmail) e `Respond to Webhook`
![Correção If e Gmail](../../assets/img/02-assistente-ia-gmail/06-correcao-if-gmail-webhook.png)

### 7. Diagrama Completo do Workflow 02 Corrigido (11 Nós)
![Fluxo Completo Corrigido](../../assets/img/02-assistente-ia-gmail/07-fluxo-completo-corrigido.png)

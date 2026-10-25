# 🌟 Prompt Final do Desafio DIO — Assistente de Investimentos (RPA + n8n + IA)

> **Navegação:** [🏠 README Principal](../README.md) | [🤖 Biblioteca de Prompts](./README.md) | [🛠️ Diagnóstico de Erros](../docs/03-diagnostico-e-correcao-erros.md)

---

## 1. Prompt em Produção no Nó `Message a model` (`OpenAI GPT-4o`)

Este é o prompt exato e corrigido configurado no nó **`Message a model`** ([`n8n/workflow.json`](../n8n/workflow.json) e [`workflows/02-assistente-investimentos-ia-gmail/workflow.json`](../workflows/02-assistente-investimentos-ia-gmail/workflow.json)):

```text
=Escreva um e-mail curto em pt-BR para o cliente abaixo, sem prometer ganhos e sem garantias.

Cliente:
Nome: {{ $json.nome }}
Perfil: {{ $json.perfil }}
Saldo: {{ $json.saldo_texto }}

Recomendação:
Produto: {{ $json.recomendacao }}
Motivo: {{ $json.motivo }}

Regras de tom e estilo:
- Idioma: {{ $json.copy_rules.idioma }}
- Tom: {{ $json.copy_rules.tom }}
- Tamanho: {{ $json.copy_rules.tamanho }}

Retorne APENAS JSON válido (sem blocos markdown) com a estrutura:
{
  "subject": "...",
  "text_body": "...",
  "html_body": "..."
}
```

---

## 2. Prompt Completo para Arquitetura e Reconstrução do Pipeline RPA + n8n

Caso deseje solicitar a uma IA generativa (ChatGPT, Claude ou Gemini) a geração ou evolução completa deste pipeline, copie o prompt estruturado abaixo:

```markdown
Atue como um Engenheiro de Software Sênior especialista em Automação de Processos (RPA com Python) e Orquestração de Workflows no n8n (v1.x / v2.x).

### 1. Contexto e Objetivo
Preciso construir e validar o pipeline completo do desafio "Criando um Assistente de Investimentos com RPA e IA Generativa" da DIO:
1. Um script Python de RPA (`src/extrair_clientes.py`) que faz web scraping da tabela `#clientes tbody tr` em `https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/` extraindo `nome`, `email`, `saldo` e `perfil`, e envia via HTTP POST (`{"clientes": [...]}`) para o Webhook `/Clientes` do n8n.
2. Um workflow no n8n com 11 nós que:
   - Recebe a lista de clientes no nó `Webhook` (`POST /Clientes`, `responseMode: "responseNode"`).
   - Busca simultaneamente a base `data.csv` via `HTTP Request` (`responseFormat: "text"`) e converte para JSON no nó `Code in JavaScript`.
   - Une os clientes e os produtos no nó `Merge` (`combineByPosition`).
   - No nó `Code in JavaScript1`, converte o saldo em BRL (`"R$ 12.500,00"` -> `12500`), filtra os produtos do mesmo `perfil` com `minimo <= saldo_num`, seleciona o de maior aporte mínimo elegível e gera a lista `resultados`.
   - No nó `Code in JavaScript2`, divide `resultados` em 1 item por cliente com regras de copywriting (`copy_rules`).
   - No nó `Message a model` (`OpenAI GPT-4o`), gera um JSON contendo `subject`, `text_body` e `html_body` usando expressões `{{ $json.* }}` sem prometer ganhos.
   - No nó `Code in JavaScript3`, faz o parse seguro (`JSON.parse`) da resposta da IA, recupera os campos do cliente via `$("Code in JavaScript2").all()` e aplica um fallback determinístico caso a API falhe.
   - No nó `If`, valida `{{ $json.email_to }}` via Regex `^[^\s@]+@[^\s@]+\.[^\s@]+$`.
   - Na saída `True`, envia o e-mail no nó `Send a message` (`Gmail`) e segue para `Respond to Webhook`. Na saída `False`, vai direto para `Respond to Webhook`.
```

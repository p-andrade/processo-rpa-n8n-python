# ⚙️ Workflows n8n do Desafio (`workflows/` e `n8n/`)

> **Navegação:** [🏠 README Principal](../README.md) | [📚 Documentação Técnica](../docs/README.md) | [🛠️ Diagnóstico de Erros](../docs/03-diagnostico-e-correcao-erros.md) | [🧪 Testes e Validação](../tests/README.md)

---

## 📌 Visão Geral dos Workflows Disponíveis

Este diretório organiza todas as versões do workflow para o desafio **Processo de RPA com N8N e Python**:

| # | Diretório | Propósito Principal | Nós | Credencial Externa |
| :---: | :--- | :--- | :---: | :--- |
| **00** | [`00-rascunho-original-aluno/`](./00-rascunho-original-aluno/README.md) | Preserva o rascunho original enviado pelo aluno com os 6 erros documentados para comparação *Antes vs. Depois*. | 11 nós | Sanitizado |
| **01** | **[`01-assistente-investimentos-mvp/`](./01-assistente-investimentos-mvp/README.md)** | **Versão MVP (Etapas 3 e 4 da DIO):** cruza clientes com `data.csv` e gera mensagens estáticas por perfil, sem depender de OpenAI ou Gmail. | 6 nós | **Nenhuma** (100% nativo) |
| **02** | **[`02-assistente-investimentos-ia-gmail/`](./02-assistente-investimentos-ia-gmail/README.md)** | **Versão Completa Corrigida (Etapa 5 da DIO):** workflow de 11 nós do aluno com todos os 6 erros corrigidos (GPT-4o + Guardrail/Fallback + If Regex + Gmail dinâmico). Também disponível em [`n8n/workflow.json`](../n8n/workflow.json). | 11 nós | **Opcional** (`OpenAI` e `Gmail`; possui fallback automático) |

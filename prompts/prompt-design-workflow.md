# 📐 Template de Prompt — Design de Workflow RPA + n8n

> **Navegação:** [🏠 README Principal](../README.md) | [🤖 Biblioteca de Prompts](./README.md)

Use este template sempre que precisar projetar um workflow no **n8n** que receba dados de um robô **Python (RPA)** e os enriqueça com uma base externa (CSV/API):

```markdown
Projete um workflow exportável para o n8n (v1.x/v2.x) seguindo estas regras estritas:
1. Gatilho: `n8n-nodes-base.webhook` (POST, responseMode="responseNode").
2. Enriquecimento: `n8n-nodes-base.httpRequest` (responseFormat="text") + `n8n-nodes-base.code` para converter CSV em array JSON.
3. União: `n8n-nodes-base.merge` com `mode="combine"` e `combineBy="combineByPosition"`.
4. Cruzamento determinístico em JavaScript antes de chamar qualquer LLM.
5. Proibido deixar nós Code com o placeholder `item.json.myNewField = 1` ou acoplar blocos `credentials` reais.
```

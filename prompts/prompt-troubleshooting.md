# 🔧 Template de Prompt — Troubleshooting e Auditoria de Workflows n8n

> **Navegação:** [🏠 README Principal](../README.md) | [🤖 Biblioteca de Prompts](./README.md)

Use este template para diagnosticar workflows JSON do n8n que param de retornar itens ou apresentam falhas de expressão:

```markdown
Analise o JSON de workflow n8n abaixo e verifique os seguintes pontos críticos de falha:
1. Algum nó `n8n-nodes-base.code` permaneceu com o código padrão `item.json.myNewField = 1`?
2. Os nomes das propriedades geradas por um nó `Code` coincidem exatamente com as propriedades lidas pelo nó seguinte (ex.: `$json.resultados`)?
3. Algum nó de IA (`@n8n/n8n-nodes-langchain.openAi`) contém código JavaScript imperativo (`const x = ...; return ...`) onde deveria haver apenas expressões `{{ $json.* }}`?
4. Após o nó de IA, existe um nó `Code` fazendo `JSON.parse()` e recuperando os metadados originais do cliente via `$("NomeDoNoAnterior").all()`?
5. O nó `If` possui `leftValue` e `rightValue` preenchidos e ambas as portas (`True` e `False`) devidamente conectadas para não travar o `Respond to Webhook`?
```

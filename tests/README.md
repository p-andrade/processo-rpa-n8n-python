# 🧪 Suíte de Validação e Testes Automatizados (`tests/`)

> **Navegação:** [🏠 README Principal](../README.md) | [📚 Documentação Técnica](../docs/README.md) | [⚙️ Workflows n8n](../workflows/README.md)

---

## 📌 Como Executar o Validador

Na raiz do repositório, execute:

```powershell
python tests/validar-workflows.py
```

O script verifica:
1. Integridade sintática e referencial dos workflows (`workflows/01-assistente-investimentos-mvp/workflow.json`, `workflows/02-assistente-investimentos-ia-gmail/workflow.json` e `n8n/workflow.json`).
2. Presença de todas as **6 correções técnicas** no workflow principal (ausência de `myNewField = 1`, ausência de `const nome = ;`, preenchimento do nó `If`, saída `False` conectada e expressões dinâmicas no `Gmail`).
3. Auditoria de segurança (zero chaves de API e zero blocos `credentials` acoplados).
4. Execução real do extrator RPA sobre [`docs/index.html`](../docs/index.html) (`10 clientes`) e simulação de recomendações com [`docs/data.csv`](../docs/data.csv) (`9 produtos`).

Consulte o detalhamento dos casos de teste em [`casos-de-teste.md`](./casos-de-teste.md).

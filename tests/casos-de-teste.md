# 📋 Especificação dos Casos de Teste (`CT-01` a `CT-10`)

> **Navegação:** [🏠 README Principal](../README.md) | [🧪 Índice de Testes](./README.md) | [📚 Cap. 07 — Validação e Testes](../docs/07-validacao-e-testes.md)

---

## Casos Verificados Automaticamente por `tests/validar-workflows.py`

| ID | Descrição do Caso de Teste | Entrada | Saída Esperada | Status |
| :---: | :--- | :--- | :--- | :---: |
| **CT-01** | Extração Web Scraping RPA da tabela `#clientes` | `docs/index.html` | Lista com 10 dicionários contendo `nome`, `email`, `saldo` e `perfil` | ✅ Passou |
| **CT-02** | Conversão e normalização numérica do CSV | `docs/data.csv` | 9 objetos de investimento com `minimo` convertido para número inteiro | ✅ Passou |
| **CT-03** | Validação estrutural do Workflow 01 (MVP) | `workflows/01-assistente-investimentos-mvp/workflow.json` | 6 nós válidos, conexões íntegras e Webhook `POST /Clientes` | ✅ Passou |
| **CT-04** | Validação estrutural e das 6 correções do Workflow 02 | `n8n/workflow.json` e `workflows/02-assistente-investimentos-ia-gmail/workflow.json` | 11 nós válidos, zero boilerplate `myNewField`, prompt válido, Regex no `If`, Gmail dinâmico | ✅ Passou |
| **CT-05** | Regra de elegibilidade — Perfil Conservador | `Ana Silva` (`R$ 12.500,00`) e `Daniel Oliveira` (`R$ 850,00`) | `CDB Liquidez Diária` (mín. 1000) para Ana; `Tesouro Selic` (mín. 500) para Daniel | ✅ Passou |
| **CT-06** | Regra de elegibilidade — Perfil Moderado | `Bruno Lima` (`R$ 3.200,00`) e `Felipe Santos` (`R$ 7.800,00`) | `CDB Prefixado` (mín. 1000) para Bruno; `Fundo Multimercado` (mín. 5000) para Felipe | ✅ Passou |
| **CT-07** | Regra de elegibilidade — Perfil Arrojado | `Carla Souza` (`R$ 28.900,00`) | `Fundo de Ações` (mín. 10000) | ✅ Passou |
| **CT-08** | Bloqueio de e-mail inválido no nó `If` | `entrada-email-invalido.json` (`email-sem-arroba-invalido.com`) | Reprovado na Regex (`False` $\rightarrow$ desvia do Gmail direto para `Respond to Webhook`) | ✅ Passou |
| **CT-09** | Auditoria de Segurança e Sanitização | Todos os arquivos `.json` | Nenhum token privado ou bloco `credentials` acoplado | ✅ Passou |

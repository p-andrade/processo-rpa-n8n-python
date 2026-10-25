# 🧪 07 — Estratégia de Validação, Casos de Teste e Qualidade

> **Navegação:** [⬅️ Anterior: 06 — Arquitetura da Solução](./06-arquitetura-da-solucao.md) | [📚 Índice da Documentação](./README.md) | [Próximo: 08 — Guia de Apresentação ➡️](./08-guia-de-apresentacao.md)

---

## 1. Metodologia de Verificação em Duas Camadas

Para garantir que nenhum erro estrutural, de sintaxe ou de regra de negócio permanecesse no projeto, implementamos o validador automatizado [`tests/validar-workflows.py`](../tests/validar-workflows.py), que realiza verificações determinísticas em todos os artefatos do repositório:

1. **Validação Estrutural e Referencial do Grafo n8n:** Verifica chaves obrigatórias (`name`, `nodes`, `connections`), unicidade de IDs e nomes, existência de todos os nós referenciados nas conexões e configuração `POST /Clientes` com `responseMode: "responseNode"`.
2. **Verificação Antirregressão dos 6 Erros Corrigidos:** Garante que nenhum nó nos workflows finais contenha o boilerplate `item.json.myNewField = 1`, que não existam atribuições vazias (`const nome = ;`), que o nó `If` possua condição Regex preenchida e porta `False` conectada, e que o nó `Send a message` utilize expressões dinâmicas.
3. **Auditoria de Segurança (Zero Segredos):** Verifica a ausência de chaves `sk-...`, tokens Bearer e blocos `credentials` acoplados nos workflows finais.
4. **Teste Funcional Real de RPA e Cruzamento:** Executa o extrator `extrair_clientes_do_html` sobre [`docs/index.html`](./index.html) (validando os 10 clientes), lê [`docs/data.csv`](./data.csv) (validando os 9 produtos) e testa a lógica de recomendação para cada perfil e faixa de saldo.

---

## 2. Matriz de Casos de Teste (`CT-01` a `CT-10`)

| ID | Caso de Teste | Alvo | Tipo | Resultado Obtido |
| :---: | :--- | :--- | :---: | :---: |
| **CT-01** | Extração RPA da tabela HTML (`10 clientes`) | `src/extrair_clientes.py` + `docs/index.html` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-02** | Leitura e normalização de `minimo` nos `9 produtos` do CSV | `docs/data.csv` + `Code in JavaScript` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-03** | Integridade estrutural e de conexões do Workflow 01 (MVP - 6 nós) | `workflows/01-assistente-investimentos-mvp/workflow.json` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-04** | Integridade estrutural e das 6 correções no Workflow 02 (11 nós) | `workflows/02-assistente-investimentos-ia-gmail/workflow.json` e `n8n/workflow.json` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-05** | Recomendação Perfil Conservador (`Ana Silva`, `R$ 12.500,00` $\rightarrow$ `CDB Liquidez Diária`, e `Daniel Oliveira`, `R$ 850,00` $\rightarrow$ `Tesouro Selic`) | `Code in JavaScript1` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-06** | Recomendação Perfil Moderado (`Bruno Lima`, `R$ 3.200,00` $\rightarrow$ `CDB Prefixado`, e `Felipe Santos`, `R$ 7.800,00` $\rightarrow$ `Fundo Multimercado`) | `Code in JavaScript1` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-07** | Recomendação Perfil Arrojado (`Carla Souza`, `R$ 28.900,00` $\rightarrow$ `Fundo de Ações`) | `Code in JavaScript1` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-08** | Rejeição de e-mail inválido pela Regex do nó `If` (`email-sem-arroba-invalido.com` $\rightarrow$ `False`) | `If` + `entrada-email-invalido.json` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-09** | Auditoria de segurança (zero chaves de API e zero blocos `credentials` acoplados) | Todos os `.json` de `workflows/` e `n8n/` | Automatizado (Python) | ✅ **APROVADO** |
| **CT-10** | Disparo ao vivo via OpenAI (`gpt-4o`) e Gmail OAuth2 em instância ativa do n8n | Servidor n8n Runtime | Dependente de Credencial do Usuário | ℹ️ **Documentado com Fallback** |

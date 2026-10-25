# 🔍 02 — Curadoria de Fontes Oficiais e Referências Técnicas

> **Navegação:** [⬅️ Anterior: 01 — Contexto e Objetivos](./01-contexto-e-objetivos.md) | [📚 Índice da Documentação](./README.md) | [Próximo: 03 — Diagnóstico e Correção de Erros ➡️](./03-diagnostico-e-correcao-erros.md)

---

## 1. Critérios de Seleção de Fontes

Para garantir que todas as correções aplicadas ao workflow do **n8n** e ao script de **RPA em Python** seguissem padrões oficiais e verificáveis, utilizamos exclusivamente fontes primárias da **Digital Innovation One (DIO)**, da **documentação oficial do n8n (`v1.x` / `v2.x`)** e da **documentação oficial do ecossistema Python**.

---

## 2. Catálogo Auditável de Fontes Primárias

| ID | Fonte / Instituição | URL Oficial | Data de Verificação | Aplicação Prática neste Projeto |
| :---: | :--- | :--- | :---: | :--- |
| **F-01** | **DIO — Repositório Base do Lab** | [github.com/digitalinnovationone/dio-lab-assistente-investimentos-rpa-n8n](https://github.com/digitalinnovationone/dio-lab-assistente-investimentos-rpa-n8n) | 24/10/2026 | Obtenção da estrutura oficial, roteiro de 5 etapas, `docs/index.html`, `docs/data.csv` e `extrair_clientes.ipynb`. |
| **F-02** | **DIO — GitHub Pages (Clientes & CSV)** | [digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/](https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/) | 24/10/2026 | Endpoint público consumido pelo robô RPA em Python (`index.html`) e pelo nó `HTTP Request` do n8n (`data.csv`). |
| **F-03** | **n8n Docs — Webhook & Respond to Webhook** | [docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/) | 24/10/2026 | Configuração de `httpMethod: "POST"`, `path: "Clientes"` e `responseMode: "responseNode"`. |
| **F-04** | **n8n Docs — Code Node (JavaScript)** | [docs.n8n.io/code/code-node/](https://docs.n8n.io/code/code-node/) | 24/10/2026 | Uso correto de `$input.all()`, `$json`, `$("NodeName").all()` e estrutura de retorno `[{ json: { ... } }]`. |
| **F-05** | **n8n Docs — Merge Node (v3.2)** | [docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.merge/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.merge/) | 24/10/2026 | União posicional (`mode: "combine"`, `combineBy: "combineByPosition"`) entre o payload do Webhook e o CSV processado. |
| **F-06** | **n8n Docs — OpenAI Node (`@n8n/n8n-nodes-langchain.openAi`)** | [docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.openai/](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.openai/) | 24/10/2026 | Correção do parâmetro `responses.values[0].content` com expressões `{{ $json.* }}` em vez de código imperativo JS. |
| **F-07** | **n8n Docs — IF Node (v2.3) & Gmail Node (v2.2)** | [docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.if/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.if/) | 24/10/2026 | Configuração da condição Regex de e-mail no nó `If` e expressões dinâmicas no nó `Send a message` (`Gmail`). |
| **F-08** | **BeautifulSoup 4 & Python Standard Library** | [crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | 24/10/2026 | Seletores CSS `#clientes tbody tr` para web scraping da tabela de clientes. |

---

## 3. Análise dos Dados Oficiais Verificados na Fonte (`F-01` e `F-02`)

### 3.1. Base de Opções de Investimento (`docs/data.csv`)
A consulta direta ao endpoint `https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/data.csv` retorna 9 produtos divididos igualmente entre os 3 perfis:

| Perfil | Produto | Aporte Mínimo (`minimo`) | Rentabilidade |
| :--- | :--- | :---: | :---: |
| **Conservador** | Poupança | `R$ 100` | `6.2%` |
| **Conservador** | Tesouro Selic | `R$ 500` | `13.0%` |
| **Conservador** | CDB Liquidez Diária | `R$ 1.000` | `12.5%` |
| **Moderado** | CDB Prefixado | `R$ 1.000` | `14.0%` |
| **Moderado** | Tesouro IPCA+ | `R$ 1.000` | `IPCA+6.0%` |
| **Moderado** | Fundo Multimercado | `R$ 5.000` | `16.0%` |
| **Arrojado** | Criptomoedas | `R$ 100` | `Variável` |
| **Arrojado** | Ações ETF | `R$ 500` | `Variável` |
| **Arrojado** | Fundo de Ações | `R$ 10.000` | `Variável` |

### 3.2. Base de Clientes (`docs/index.html`)
A página HTML oficial contém 10 clientes na tabela `#clientes`:
1. **Ana Silva** (`ana@email.com`) — Saldo: `R$ 12.500,00` — Perfil: `Conservador`
2. **Bruno Lima** (`bruno@email.com`) — Saldo: `R$ 3.200,00` — Perfil: `Moderado`
3. **Carla Souza** (`carla@email.com`) — Saldo: `R$ 28.900,00` — Perfil: `Arrojado`
4. **Daniel Oliveira** (`daniel@email.com`) — Saldo: `R$ 850,00` — Perfil: `Conservador`
5. **Elena Rodrigues** (`elena@email.com`) — Saldo: `R$ 45.000,00` — Perfil: `Arrojado`
6. **Felipe Santos** (`felipe@email.com`) — Saldo: `R$ 7.800,00` — Perfil: `Moderado`
7. **Gabriela Costa** (`gabriela@email.com`) — Saldo: `R$ 1.500,00` — Perfil: `Conservador`
8. **Henrique Alves** (`henrique@email.com`) — Saldo: `R$ 22.300,00` — Perfil: `Moderado`
9. **Isabela Martins** (`isabela@email.com`) — Saldo: `R$ 500,00` — Perfil: `Conservador`
10. **João Pereira** (`joao@email.com`) — Saldo: `R$ 15.000,00` — Perfil: `Arrojado`

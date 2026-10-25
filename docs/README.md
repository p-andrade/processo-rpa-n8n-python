# 📚 Documentação Técnica — Processo de RPA com n8n, Python e IA Generativa

Bem-vindo ao diretório central de documentação técnica do projeto **Desafio DIO — Criando um Assistente de Investimentos com RPA e IA Generativa (Processo de RPA com N8N e Python)**. Este acervo foi projetado sob princípios de engenharia de software e design instrucional para documentar toda a jornada: desde a extração automatizada de dados via **Python (RPA)** até a auditoria, correção de erros e validação do workflow completo no **n8n** integrado ao **GPT-4o (OpenAI)** e **Gmail**.

---

## 🗺️ Trilha de Leitura Recomendada

A documentação está organizada em uma sequência lógica de **8 capítulos principais** + os arquivos base do laboratório da DIO (`index.html` e `data.csv`):

| Ordem | Documento | Propósito Principal | Público Recomendado |
| :---: | :--- | :--- | :--- |
| **01** | [01-contexto-e-objetivos.md](./01-contexto-e-objetivos.md) | Contextualiza o desafio da DIO, o problema do mercado financeiro, o papel do RPA em Python e a evolução do MVP para o fluxo completo com IA e Gmail. | Todos os perfis |
| **02** | [02-curadoria-de-fontes.md](./02-curadoria-de-fontes.md) | Catálogo auditável de fontes oficiais (`docs.n8n.io`, repositório oficial da DIO, documentação BeautifulSoup/Python) com datas de acesso e finalidades. | Pesquisadores e Arquitetos |
| **03** | [03-diagnostico-e-correcao-erros.md](./03-diagnostico-e-correcao-erros.md) | **Relatório Forense Completo (*Antes vs. Depois*):** detalha os 6 erros encontrados no workflow original do aluno, a causa raiz de cada um e o código exato das correções aplicadas. | Desenvolvedores e Avaliadores |
| **04** | [04-miniestudo-rpa-n8n-python.md](./04-miniestudo-rpa-n8n-python.md) | Miniestudo técnico *"Do Web Scraping ao Agente Financeiro: integrando RPA em Python, cruzamento de dados CSV e LLMs no n8n"*. | Estudantes e Analistas |
| **05** | [05-glossario.md](./05-glossario.md) | Dicionário técnico em tabela com 22 termos essenciais de RPA, Web Scraping, n8n, Finanças e IA Generativa contextualizados no projeto. | Iniciantes e Estudantes |
| **06** | [06-arquitetura-da-solucao.md](./06-arquitetura-da-solucao.md) | Documenta a arquitetura ponta a ponta, contratos JSON entre o Python e o n8n, lógica de elegibilidade por saldo/perfil e diagramas Mermaid. | Desenvolvedores e Arquitetos |
| **07** | [07-validacao-e-testes.md](./07-validacao-e-testes.md) | Registra a estratégia de qualidade, validação estática e lógica automatizada (`tests/validar-workflows.py`), matriz de casos de teste (`CT-01` a `CT-10`) e limitações. | QA e Engenheiros de Software |
| **08** | [08-guia-de-apresentacao.md](./08-guia-de-apresentacao.md) | Roteiro estruturado (*pitch técnico*) para apresentar e defender as correções e a arquitetura deste projeto em avaliações da DIO e entrevistas. | Candidatos e Profissionais |

---

## 📊 Arquivos de Dados do Laboratório DIO neste Diretório

Além dos capítulos técnicos, esta pasta mantém os dois arquivos originais do laboratório da DIO para execução local offline e paridade com o GitHub Pages:
- **[`docs/index.html`](./index.html):** Página HTML contendo a tabela `#clientes` com os 10 clientes fictícios, seus e-mails, saldos em reais (`R$`) e perfis de investidor (`Conservador`, `Moderado`, `Arrojado`).
- **[`docs/data.csv`](./data.csv):** Base CSV contendo as 9 opções de produtos de investimento (`Poupança`, `CDB Liquidez Diária`, `Tesouro Selic`, `CDB Prefixado`, `Fundo Multimercado`, `Tesouro IPCA+`, `Ações ETF`, `Fundo de Ações`, `Criptomoedas`), seus aportes mínimos e rentabilidades.

---

## 🔗 Conexão com os Demais Diretórios do Repositório

- **Quer ver o código Python de RPA?** Acesse [`src/README.md`](../src/README.md) ([`src/extrair_clientes.py`](../src/extrair_clientes.py) e [`src/extrair_clientes.ipynb`](../src/extrair_clientes.ipynb)).
- **Quer inspecionar ou importar os workflows JSON corrigidos no n8n?** Acesse [`workflows/README.md`](../workflows/README.md) ou diretamente [`n8n/workflow.json`](../n8n/workflow.json).
- **Quer consultar os prompts e regras de copywriting financeiro?** Acesse [`prompts/README.md`](../prompts/README.md).
- **Quer visualizar os diagramas e as 15 lâminas PNG?** Acesse [`assets/README.md`](../assets/README.md).
- **Quer executar o validador automatizado em Python?** Acesse [`tests/README.md`](../tests/README.md).

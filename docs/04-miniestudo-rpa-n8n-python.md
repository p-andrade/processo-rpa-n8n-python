# 📖 04 — Miniestudo Final: Do Web Scraping ao Agente Financeiro com RPA, n8n e IA

> **Navegação:** [⬅️ Anterior: 03 — Diagnóstico e Correção de Erros](./03-diagnostico-e-correcao-erros.md) | [📚 Índice da Documentação](./README.md) | [Próximo: 05 — Glossário Técnico ➡️](./05-glossario.md)

---

## 1. O Papel do RPA em Python na Automação Moderna

**Robotic Process Automation (RPA)** é a técnica de automatizar tarefas operacionais repetitivas que originalmente exigiriam interação humana em interfaces gráficas ou páginas web. Quando um sistema legado publica informações apenas em tabelas HTML — sem disponibilizar uma API REST estruturada — um robô em **Python** utilizando `BeautifulSoup` (ou `html.parser`) atua como uma ponte de integração:

1. Faz a requisição HTTP `GET` à página (`docs/index.html`).
2. Localiza a tabela `#clientes` e percorre as linhas `tbody tr`.
3. Converte as células `<td>` em objetos JSON padronizados (`nome`, `email`, `saldo`, `perfil`).
4. Dispara o lote via `POST` para o orquestrador **n8n** (`/Clientes`).

---

## 2. Por que Combinar Regras Determinísticas (JavaScript) com IA Generativa (LLM)?

Um erro comum em projetos iniciantes de IA no mercado financeiro é delegar **cálculos matemáticos e filtros de elegibilidade** para o modelo de linguagem (LLM). Modelos generativos são excelentes redatores, mas podem alucinar comparações numéricas (como decidir se `R$ 850,00` é maior ou menor que o aporte mínimo de `R$ 1.000,00`).

Por isso, a arquitetura deste projeto aplica o padrão **Híbrido Determinístico + Generativo**:
- **Camada Determinística (`Code in JavaScript` e `Code in JavaScript1`):** Converte `R$ 12.500,00` para `12500`, filtra estritamente os produtos do `data.csv` cujo `perfil` coincide com o do cliente e cujo `minimo <= saldo_num`, e elege matematicamente o produto ótimo.
- **Camada Generativa (`Message a model` — GPT-4o):** Recebe a recomendação já calculada e aplica regras de *copywriting* (`copy_rules`) para redigir um e-mail humano, cordial, personalizado e **sem promessas de rentabilidade garantida**.
- **Camada de Guardrail (`Code in JavaScript3`):** Audita o JSON retornado pela IA e mantém um template determinístico de contingência caso a API externa oscile.

---

## 3. Tabela Completa de Simulação do Cruzamento (10 Clientes x `data.csv`)

Abaixo está o resultado exato produzido pelo motor corrigido em `Code in JavaScript1` para os 10 clientes oficiais da DIO:

| # | Cliente | Perfil | Saldo (Texto) | Saldo (`Number`) | Produtos Elegíveis no Perfil (`minimo <= saldo`) | Produto Recomendado (Maior Aporte Elegível) | Rentabilidade |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- | :---: |
| 01 | **Ana Silva** | Conservador | `R$ 12.500,00` | `12500` | Poupança (100), Tesouro Selic (500), CDB Liquidez Diária (1000) | **CDB Liquidez Diária** | `12.5%` |
| 02 | **Bruno Lima** | Moderado | `R$ 3.200,00` | `3200` | CDB Prefixado (1000), Tesouro IPCA+ (1000) | **CDB Prefixado** | `14.0%` |
| 03 | **Carla Souza** | Arrojado | `R$ 28.900,00` | `28900` | Criptomoedas (100), Ações ETF (500), Fundo de Ações (10000) | **Fundo de Ações** | `Variável` |
| 04 | **Daniel Oliveira** | Conservador | `R$ 850,00` | `850` | Poupança (100), Tesouro Selic (500) | **Tesouro Selic** | `13.0%` |
| 05 | **Elena Rodrigues** | Arrojado | `R$ 45.000,00` | `45000` | Criptomoedas (100), Ações ETF (500), Fundo de Ações (10000) | **Fundo de Ações** | `Variável` |
| 06 | **Felipe Santos** | Moderado | `R$ 7.800,00` | `7800` | CDB Prefixado (1000), Tesouro IPCA+ (1000), Fundo Multimercado (5000) | **Fundo Multimercado** | `16.0%` |
| 07 | **Gabriela Costa** | Conservador | `R$ 1.500,00` | `1500` | Poupança (100), Tesouro Selic (500), CDB Liquidez Diária (1000) | **CDB Liquidez Diária** | `12.5%` |
| 08 | **Henrique Alves** | Moderado | `R$ 22.300,00` | `22300` | CDB Prefixado (1000), Tesouro IPCA+ (1000), Fundo Multimercado (5000) | **Fundo Multimercado** | `16.0%` |
| 09 | **Isabela Martins** | Conservador | `R$ 500,00` | `500` | Poupança (100), Tesouro Selic (500) | **Tesouro Selic** | `13.0%` |
| 10 | **João Pereira** | Arrojado | `R$ 15.000,00` | `15000` | Criptomoedas (100), Ações ETF (500), Fundo de Ações (10000) | **Fundo de Ações** | `Variável` |

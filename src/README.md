# 🤖 Scripts de RPA em Python (`src/`)

> **Navegação:** [🏠 README Principal](../README.md) | [📚 Documentação Técnica](../docs/README.md) | [⚙️ Workflows n8n](../workflows/README.md) | [🧪 Testes e Validação](../tests/README.md)

---

## 📌 Visão Geral

Este diretório contém a camada de **Robotic Process Automation (RPA)** em Python responsável por:
1. Acessar a página web de clientes ([`docs/index.html`](../docs/index.html) local ou hospedada no GitHub Pages da DIO).
2. Extrair os dados da tabela HTML `#clientes` (`nome`, `email`, `saldo` e `perfil`) usando `BeautifulSoup`.
3. Resolver o `TODO (N8N)` deixado no laboratório original, enviando o payload JSON `{"clientes": [...]}` via requisição HTTP `POST` para o nó `Webhook` (`/Clientes`) do n8n.

---

## 📂 Arquivos Disponíveis

| Arquivo | Descrição |
| :--- | :--- |
| **[`extrair_clientes.py`](./extrair_clientes.py)** | Script CLI completo em Python com suporte a modo local (`--local`), modo de simulação sem servidor (`--dry-run`) e disparo `POST` para o Webhook do n8n (`--webhook-url`). |
| **[`extrair_clientes.ipynb`](./extrair_clientes.ipynb)** | Notebook Jupyter/Colab compatível com o roteiro da DIO (também espelhado em [`rpa/extrair_clientes.ipynb`](../rpa/extrair_clientes.ipynb)). |

---

## 🚀 Como Executar

### 1. Modo de Simulação e Inspeção Local (`--dry-run` e `--local`)
Extrai os 10 clientes diretamente de [`docs/index.html`](../docs/index.html) e imprime o JSON formatado no terminal sem exigir que o servidor do n8n esteja aberto:
```powershell
python src/extrair_clientes.py --local --dry-run
```

### 2. Disparo Real contra o Webhook do n8n
Com o workflow importado e escutando no n8n (`http://localhost:5678/webhook-test/Clientes`):
```powershell
python src/extrair_clientes.py --webhook-url "http://localhost:5678/webhook-test/Clientes"
```

# 🎤 08 — Guia de Apresentação e Defesa Técnica (Pitch do Projeto)

> **Navegação:** [⬅️ Anterior: 07 — Validação e Testes](./07-validacao-e-testes.md) | [📚 Índice da Documentação](./README.md) | [🏠 README Principal](../README.md)

---

## 1. Estrutura de Pitch Técnico (3 a 5 Minutos)

Use este roteiro para apresentar seu repositório na entrega da DIO, no LinkedIn ou em entrevistas técnicas de Automação, Dados e IA:

### ⏱️ Minuto 1: O Problema e a Arquitetura Híbrida (RPA + n8n + IA)
> *"Neste projeto da DIO, construí um Assistente de Investimentos Automatizado que resolve um cenário clássico do mercado financeiro: coletar dados de clientes de um sistema web legado sem API usando **RPA em Python (`BeautifulSoup`)**, cruzar o perfil de risco e o saldo de cada cliente com uma base CSV de produtos financeiros no **n8n**, e redigir e-mails personalizados com **GPT-4o** sob regras estritas de compliance (sem prometer ganhos garantidos)."*

### ⏱️ Minuto 2: Como Resolvi as Lacunas do Desafio e Corrigi os 6 Erros do Workflow
> *"Durante as aulas, vários códigos JavaScript intermediários não tinham documentação escrita. Eu mapeei o fluxo ponta a ponta, preservei meu rascunho inicial para fins de auditoria e implementei 6 correções críticas:*
> 1. *Construí em `Code in JavaScript1` o motor que converte saldos em Reais (`parseBRL`) e seleciona o produto de maior aporte mínimo compatível com o saldo e perfil do cliente.*
> 2. *Corrigi o prompt do nó `Message a model` (`OpenAI`) para usar expressões nativas `{{ $json.* }}`.*
> 3. *Implementei em `Code in JavaScript3` o parser JSON da resposta da IA com `try/catch` e **fallback determinístico automático**, garantindo que o workflow funcione mesmo sem chave paga da OpenAI.*
> 4. *Configurei a validação Regex de e-mail no nó `If`, parametrizando dinamicamente o envio no `Gmail` e conectando a saída `False` ao `Respond to Webhook`."*

### ⏱️ Minuto 3: Qualidade de Software e Validação Automatizada
> *"Para garantir qualidade de produção, criei um validador automatizado em Python (`tests/validar-workflows.py`) que audita a estrutura de todos os nós e conexões, impede o vazamento de credenciais no GitHub e testa a extração real dos 10 clientes do HTML e o cruzamento com os 9 produtos do CSV."*

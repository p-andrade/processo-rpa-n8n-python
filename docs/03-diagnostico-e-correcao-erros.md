# 🛠️ 03 — Diagnóstico Forense e Correção dos Erros do Workflow Original

> **Navegação:** [⬅️ Anterior: 02 — Curadoria de Fontes](./02-curadoria-de-fontes.md) | [📚 Índice da Documentação](./README.md) | [Próximo: 04 — Miniestudo RPA, n8n e Python ➡️](./04-miniestudo-rpa-n8n-python.md)

---

## 1. Contexto da Auditoria

Nos vídeos de orientação do desafio da DIO, o instrutor apresenta um workflow avançado de **11 nós** que vai além do MVP estático: ele busca o `data.csv`, une com os clientes vindos do `Webhook`, cruza os perfis e saldos, divide em 1 item por cliente com regras de copywriting (`copy_rules`), chama o modelo `gpt-4o` (`Message a model`), faz o parse do JSON retornado pela IA, valida o e-mail em um nó `If`, dispara o e-mail via `Gmail` (`Send a message`) e responde ao `Webhook`.

Contudo, como o instrutor já tinha os scripts JavaScript prontos em sua máquina e não disponibilizou o arquivo `.json` exportado nem a documentação da lógica interna de cada nó `Code`, o workflow construído pelo aluno a partir dos vídeos ficou com **lacunas de código e parâmetros incompletos**.

Abaixo apresentamos o **diagnóstico completo dos 6 erros identificados** no rascunho original ([`workflows/00-rascunho-original-aluno/workflow-original-com-erros.json`](../workflows/00-rascunho-original-aluno/workflow-original-com-erros.json)) e as **correções exatas** implementadas na versão final ([`n8n/workflow.json`](../n8n/workflow.json) e [`workflows/02-assistente-investimentos-ia-gmail/workflow.json`](../workflows/02-assistente-investimentos-ia-gmail/workflow.json)).

![Auditoria e Correção dos 6 Erros](../assets/img/02-assistente-ia-gmail/01-visao-geral-e-erros-corrigidos.png)

---

## 2. Resumo Executivo das 6 Correções

| # | Nó Afetado | Problema no Rascunho Original | Impacto na Execução | Solução Implementada |
| :---: | :--- | :--- | :--- | :--- |
| **01** | `Code in JavaScript1` | Continha apenas o boilerplate padrão `item.json.myNewField = 1`. | Não gerava o array `$json.resultados`. Com isso, o nó seguinte (`Code in JavaScript2`) recebia `[]` e encerrava o fluxo com **0 itens**. | Implementado o motor completo que lê `clientes` e `investimentos` do `Merge`, converte saldo BRL para número, filtra por perfil e aporte mínimo e retorna `{ resultados }`. |
| **02** | `Message a model` (`OpenAI`) | Continha código JavaScript imperativo quebrado (`const nome = ;`, `const perfil = ;`, `return [{json: ...}]`) dentro do campo de prompt. | Erro de sintaxe ou envio literal de código JS como se fosse texto para o modelo GPT-4o. | Substituído por template de expressão nativo do n8n usando `{{ $json.nome }}`, `{{ $json.perfil }}`, `{{ $json.saldo_texto }}`, `{{ $json.recomendacao }}` e `{{ $json.motivo }}`. |
| **03** | `Code in JavaScript3` | Continha apenas o boilerplate padrão `item.json.myNewField = 1`. | A resposta textual JSON do GPT-4o não era convertida em objeto (`subject`, `text_body`, `html_body`) e o campo `email_to` era perdido após o nó da OpenAI. | Implementado parser JSON resiliente (`JSON.parse` com limpeza de blocos markdown), recuperação de dados via `$("Code in JavaScript2").all()` e **fallback automático** caso sem API key. |
| **04** | `If` | Condição `regex` estava com `leftValue: ""` e `rightValue: ""`, e a saída `False` (`main[1]`) estava desconectada. | Todo item falhava na validação Regex vazia e morria silenciosamente na porta `False`, travando o `Respond to Webhook`. | Configurado `leftValue: "={{ $json.email_to }}"`, `rightValue: "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"` e conectada a porta `False` diretamente ao `Respond to Webhook`. |
| **05** | `Send a message` (`Gmail`) | Campos estáticos fixos: `sendTo: "pedrotmajr@gmail.com"`, `subject: "Test"`, `message: "Hello World"`. | Ignorava o e-mail do cliente e o texto gerado pela IA, enviando sempre `"Hello World"`. | Configuradas expressões dinâmicas: `sendTo: "={{ $json.email_to }}"`, `subject: "={{ $json.subject }}"` e `message: "={{ $json.html_body || $json.text_body }}"`. |
| **06** | Segurança e HTTP CSV | Blocos `credentials` com IDs locais acoplados e `HTTP Request` sem `responseFormat: "text"`. | Risco de exposição de metadados no GitHub e falha ao ler `data.csv` como string. | Removidos blocos `credentials` acoplados, adicionado `continueOnFail: true` nos nós externos e forçado `responseFormat: "text"` no `HTTP Request`. |

---

## 3. Análise Detalhada Nó a Nó (*Antes vs. Depois*)

### 🔴 Erro 01: Lógica Ausente no Nó `Code in JavaScript1` (Pós-Merge)

#### O que acontecia no original:
Logo após o nó `Merge` (que une o payload do `Webhook` com o array `investimentos` vindo do `Code in JavaScript`), o nó `Code in JavaScript1` estava com o código padrão de quando se cria um nó novo no n8n:
```javascript
// ANTES (Com Erro - Boilerplate padrão do n8n)
for (const item of $input.all()) {
  item.json.myNewField = 1;
}
return $input.all();
```
Porém, o nó seguinte (`Code in JavaScript2`, que o aluno já havia preenchido corretamente!) começa com a linha:
```javascript
const resultados = $json.resultados || [];
```
Como `Code in JavaScript1` não criava a propriedade `resultados`, a variável `resultados` ficava sempre vazia (`[]`) e o `Code in JavaScript2` retornava `0 itens`, parando todo o workflow ali mesmo.

#### ✅ Como foi corrigido:
Reconstruímos em `Code in JavaScript1` toda a lógica de negócio que faz a ponte exata entre o `Merge` e o `Code in JavaScript2`:
```javascript
// DEPOIS (Corrigido em Code in JavaScript1)
function parseBRL(valor) {
  if (typeof valor === "number") return valor;
  if (!valor) return 0;
  const s = String(valor)
    .replace("R$", "")
    .replace(/\./g, "")
    .replace(",", ".")
    .replace(/[^\d.]/g, "")
    .trim();
  const n = Number(s);
  return Number.isFinite(n) ? n : 0;
}

const clientes = $json.body?.clientes ?? $json.clientes ?? [];
const investimentos = $json.investimentos ?? [];

const TEMPLATES = {
  Conservador: (nome, prod, rent) => `Olá, ${nome}! Para o seu perfil Conservador, priorizamos segurança e liquidez em renda fixa. Recomendamos o produto ${prod} (rentabilidade de referência: ${rent}).`,
  Moderado: (nome, prod, rent) => `Olá, ${nome}! Para o seu perfil Moderado, buscamos equilíbrio entre proteção e rentabilidade. Recomendamos o produto ${prod} (rentabilidade de referência: ${rent}).`,
  Arrojado: (nome, prod, rent) => `Olá, ${nome}! Para o seu perfil Arrojado, focamos em diversificação e maior potencial de retorno no longo prazo. Recomendamos o produto ${prod} (rentabilidade: ${rent}).`
};

const resultados = clientes.map(c => {
  const nome = String(c.nome || "").trim();
  const email = String(c.email || "").trim().toLowerCase();
  const perfil = String(c.perfil || "Conservador").trim();
  const saldo_texto = String(c.saldo || "R$ 0,00").trim();
  const saldo_num = parseBRL(saldo_texto);

  const opcoesPerfil = investimentos.filter(
    inv => String(inv.perfil || "").toLowerCase() === perfil.toLowerCase()
  );
  const elegiveis = opcoesPerfil.filter(inv => Number(inv.minimo) <= saldo_num);
  elegiveis.sort((a, b) => Number(b.minimo) - Number(a.minimo));

  const escolhido = elegiveis[0] ?? opcoesPerfil[0] ?? {
    produto: "Tesouro Selic",
    minimo: 100,
    rentabilidade: "13.0%"
  };

  const templateFn = TEMPLATES[perfil] ?? TEMPLATES.Conservador;
  const mensagem_escolhida = templateFn(nome, escolhido.produto, escolhido.rentabilidade);

  return {
    nome,
    email,
    perfil,
    saldo_texto,
    saldo_num,
    recomendacao: escolhido.produto,
    rentabilidade: escolhido.rentabilidade,
    aporte_minimo: escolhido.minimo,
    motivo: `Produto alinhado ao perfil ${perfil} com aporte mínimo de R$ ${escolhido.minimo} compatível com o saldo de ${saldo_texto} (rentabilidade: ${escolhido.rentabilidade}).`,
    mensagem_escolhida
  };
});

return [{ json: { resultados } }];
```

---

### 🔴 Erro 02: Sintaxe Incorreta no Nó `Message a model` (`OpenAI`)

#### O que acontecia no original:
No nó `Message a model` (`@n8n/n8n-nodes-langchain.openAi`), o campo `content` continha um script JavaScript de nó `Code` (e com atribuições vazias `const nome = ;` e `const perfil = ;`):
```javascript
// ANTES (Com Erro - Código JS imperativo dentro do campo de Prompt)
=// 1. Captura os dados do item que está passando pelo nó
const nome = ;
const perfil = ;
const saldo_texto = $json.saldo_texto;
...
return [{ json: { prompt: prompt } }];
```
No n8n, o campo **Prompt / Content** do nó da OpenAI não executa `return [{ json: ... }]`; ele espera um **texto com expressões interpoladas entre chaves duplas `{{ ... }}`**.

#### ✅ Como foi corrigido:
Substituímos pelo template de expressão limpo e válido no n8n:
```text
=Escreva um e-mail curto em pt-BR para o cliente abaixo, sem prometer ganhos e sem garantias.

Cliente:
Nome: {{ $json.nome }}
Perfil: {{ $json.perfil }}
Saldo: {{ $json.saldo_texto }}

Recomendação:
Produto: {{ $json.recomendacao }}
Motivo: {{ $json.motivo }}

Regras de tom e estilo:
- Idioma: {{ $json.copy_rules.idioma }}
- Tom: {{ $json.copy_rules.tom }}
- Tamanho: {{ $json.copy_rules.tamanho }}

Retorne APENAS JSON válido (sem blocos markdown) com a estrutura:
{
  "subject": "...",
  "text_body": "...",
  "html_body": "..."
}
```

---

### 🔴 Erro 03: Ausência de Parser JSON e Perda de Contexto em `Code in JavaScript3`

#### O que acontecia no original:
O nó `Code in JavaScript3` (posicionado entre o `Message a model` e o `If`) também estava com o código boilerplate `item.json.myNewField = 1`.
Quando o nó `Message a model` responde, ele retorna a string gerada pelo GPT-4o, mas:
1. Essa string precisa passar por `JSON.parse()` para extrair `subject`, `text_body` e `html_body` (removendo eventuais blocos ````json` que o modelo adicione).
2. Os campos originais do cliente (`email_to`, `nome`, `perfil`, `recomendacao`) que estavam em `Code in JavaScript2` precisam ser preservados junto com a resposta da IA para que os nós `If` e `Send a message` saibam para qual endereço de e-mail enviar!

#### ✅ Como foi corrigido:
Implementamos em `Code in JavaScript3` a recomposição completa do item com `$("Code in JavaScript2").all()`, parsing seguro `try/catch` e **fallback determinístico** caso a API da OpenAI não esteja configurada:
```javascript
// DEPOIS (Corrigido em Code in JavaScript3)
const clientesOriginais = $("Code in JavaScript2").all();
const respostasIA = $input.all();

const saida = respostasIA.map((item, idx) => {
  const base = clientesOriginais[idx]?.json ?? item.json ?? {};
  const rawObj = item.json ?? {};

  const rawText =
    rawObj?.message?.content ??
    rawObj?.output ??
    rawObj?.text ??
    rawObj?.choices?.[0]?.message?.content ??
    (typeof rawObj?.content === "string" ? rawObj.content : "");

  let parsed = null;
  let modo_geracao = "ia_generativa_openai";

  if (rawText && typeof rawText === "string") {
    try {
      const limpo = rawText.replace(/```json/gi, "").replace(/```/g, "").trim();
      parsed = JSON.parse(limpo);
    } catch (e) {
      parsed = null;
    }
  }

  const fallbackSubject = `Recomendação de Investimento (${base.perfil}): ${base.recomendacao}`;
  const fallbackText =
    base.mensagem_base ||
    `Olá, ${base.nome}! Com base no seu perfil ${base.perfil} e saldo de ${base.saldo_texto}, sugerimos conhecer o produto ${base.recomendacao}. ${base.motivo}`;
  const fallbackHtml = `<p>Olá, <strong>${base.nome}</strong>!</p><p>${fallbackText}</p>`;

  if (!parsed || !parsed.subject || (!parsed.text_body && !parsed.html_body)) {
    modo_geracao = "fallback_template_seguro";
    parsed = {
      subject: fallbackSubject,
      text_body: fallbackText,
      html_body: fallbackHtml
    };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const email_valido = emailRegex.test(String(base.email_to || "").trim());

  return {
    json: {
      email_to: String(base.email_to || "").trim(),
      email_valido,
      nome: base.nome,
      perfil: base.perfil,
      saldo_texto: base.saldo_texto,
      saldo_num: base.saldo_num,
      recomendacao: base.recomendacao,
      motivo: base.motivo,
      subject: String(parsed.subject).trim(),
      text_body: String(parsed.text_body || fallbackText).trim(),
      html_body: String(parsed.html_body || fallbackHtml).trim(),
      modo_geracao
    }
  };
});

return saida;
```

---

### 🔴 Erros 04 e 05: Condição Vazia no Nó `If` e Campos Fixos no Nó `Send a message` (`Gmail`)

#### O que acontecia no original:
- No nó **`If`**, os campos `leftValue` e `rightValue` estavam em branco (`""`), e a porta `False` não levava a lugar nenhum.
- No nó **`Send a message` (`Gmail`)**, os parâmetros eram valores de teste estáticos (`sendTo: "pedrotmajr@gmail.com"`, `subject: "Test"`, `message: "Hello World"`).

#### ✅ Como foi corrigido:
1. **No nó `If`:**
   - `leftValue`: `"={{ $json.email_to }}"`
   - `operation`: `"regex"`
   - `rightValue`: `"^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"`
   - **Porta `True` (`main[0]`):** Conectada ao nó `Send a message` (`Gmail`).
   - **Porta `False` (`main[1]`):** Conectada diretamente ao nó `Respond to Webhook`, garantindo que mesmo clientes com e-mail inválido não travem a resposta HTTP do workflow.
2. **No nó `Send a message` (`Gmail`):**
   - `sendTo`: `"={{ $json.email_to }}"`
   - `subject`: `"={{ $json.subject }}"`
   - `message`: `"={{ $json.html_body || $json.text_body }}"`

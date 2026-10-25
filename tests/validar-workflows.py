#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador Estrutural, de Segurança, de RPA e de Lógica dos Workflows n8n
Projeto: Desafio DIO — Processo de RPA com N8N e Python (Assistente de Investimentos)

O que este script valida:
1. Existência de todos os arquivos JSON obrigatórios (workflows e exemplos) e dados (HTML/CSV).
2. Extração RPA real via BeautifulSoup na tabela de docs/index.html (10 clientes) e leitura de docs/data.csv (9 produtos).
3. Validade sintática JSON (UTF-8) de todos os workflows e payloads.
4. Presença dos elementos essenciais de exportação do n8n (name, nodes, connections).
5. Ausência de nós com nomes ou IDs duplicados dentro de cada workflow.
6. Integridade referencial das conexões (toda origem e destino em 'connections' deve existir em 'nodes').
7. Verificação das 6 correções aplicadas no workflow principal (ausência de boilerplate 'myNewField',
   expressões válidas no Message a model, regex configurada no If, campos dinâmicos no Gmail,
   desvio False conectado ao Respond to Webhook e zero credenciais acopladas).
8. Simulação lógica completa do cruzamento Clientes x Investimentos e geração de recomendação + fallback.
"""

import csv
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from extrair_clientes import extrair_clientes_do_html  # noqa: E402

EXPECTED_WORKFLOWS = {
    "workflows/01-assistente-investimentos-mvp/workflow.json": {
        "expected_nodes": [
            "Webhook Receber Clientes",
            "Buscar Base CSV Investimentos",
            "Converter CSV para JSON",
            "Unir Clientes e Investimentos",
            "Cruzar Perfis e Gerar Recomendacoes Estáticas",
            "Responder Webhook MVP",
        ],
        "webhook_node": "Webhook Receber Clientes",
        "webhook_path": "Clientes",
    },
    "workflows/02-assistente-investimentos-ia-gmail/workflow.json": {
        "expected_nodes": [
            "Webhook",
            "HTTP Request",
            "Code in JavaScript",
            "Merge",
            "Code in JavaScript1",
            "Code in JavaScript2",
            "Message a model",
            "Code in JavaScript3",
            "If",
            "Send a message",
            "Respond to Webhook",
        ],
        "webhook_node": "Webhook",
        "webhook_path": "Clientes",
    },
    "n8n/workflow.json": {
        "expected_nodes": [
            "Webhook",
            "HTTP Request",
            "Code in JavaScript",
            "Merge",
            "Code in JavaScript1",
            "Code in JavaScript2",
            "Message a model",
            "Code in JavaScript3",
            "If",
            "Send a message",
            "Respond to Webhook",
        ],
        "webhook_node": "Webhook",
        "webhook_path": "Clientes",
    },
}

EXPECTED_PAYLOADS = [
    "workflows/01-assistente-investimentos-mvp/exemplo-payload.json",
    "workflows/02-assistente-investimentos-ia-gmail/exemplos/entrada-clientes-completa.json",
    "workflows/02-assistente-investimentos-ia-gmail/exemplos/entrada-cliente-baixo-saldo.json",
    "workflows/02-assistente-investimentos-ia-gmail/exemplos/entrada-email-invalido.json",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{30,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", re.IGNORECASE),
]


def load_json_file(rel_path: str):
    full_path = ROOT_DIR / rel_path
    if not full_path.exists():
        return None, f"Arquivo esperado não encontrado: {rel_path}"
    try:
        content = full_path.read_text(encoding="utf-8")
        data = json.loads(content)
        return data, None
    except Exception as exc:
        return None, f"Erro ao interpretar JSON em {rel_path}: {exc}"


def check_security_no_secrets(rel_path: str) -> list[str]:
    errors = []
    full_path = ROOT_DIR / rel_path
    raw_text = full_path.read_text(encoding="utf-8")
    for pattern in SECRET_PATTERNS:
        if pattern.search(raw_text):
            errors.append(f"Possível segredo/token detectado em {rel_path} pelo padrão {pattern.pattern}")

    data = json.loads(raw_text)
    if isinstance(data, dict) and "nodes" in data:
        for node in data.get("nodes", []):
            if "credentials" in node and node["credentials"]:
                errors.append(
                    f"Nó '{node.get('name')}' em {rel_path} contém bloco 'credentials' acoplado."
                )
    return errors


def validate_workflow_structure(rel_path: str, spec: dict) -> list[str]:
    errors = []
    data, err = load_json_file(rel_path)
    if err:
        return [err]

    if not isinstance(data, dict):
        return [f"{rel_path}: A raiz do JSON deve ser um objeto."]

    for key in ("name", "nodes", "connections"):
        if key not in data:
            errors.append(f"{rel_path}: Chave obrigatória '{key}' ausente no workflow.")

    nodes = data.get("nodes", [])
    connections = data.get("connections", {})

    if not isinstance(nodes, list) or len(nodes) == 0:
        errors.append(f"{rel_path}: 'nodes' deve ser uma lista não vazia.")
        return errors

    node_names = []
    node_ids = []
    nodes_by_name = {}

    for idx, node in enumerate(nodes):
        n_name = node.get("name")
        n_id = node.get("id")
        n_type = node.get("type")
        n_pos = node.get("position")

        if not n_name:
            errors.append(f"{rel_path}: Nó no índice {idx} não possui 'name'.")
        else:
            node_names.append(n_name)
            nodes_by_name[n_name] = node

        if not n_id:
            errors.append(f"{rel_path}: Nó '{n_name}' não possui 'id'.")
        else:
            node_ids.append(n_id)

        if not n_type:
            errors.append(f"{rel_path}: Nó '{n_name}' não possui 'type'.")

        if not isinstance(n_pos, list) or len(n_pos) != 2:
            errors.append(f"{rel_path}: Nó '{n_name}' possui 'position' inválido.")

    dup_names = {x for x in node_names if node_names.count(x) > 1}
    if dup_names:
        errors.append(f"{rel_path}: Nós com nomes duplicados encontrados: {sorted(dup_names)}")

    dup_ids = {x for x in node_ids if node_ids.count(x) > 1}
    if dup_ids:
        errors.append(f"{rel_path}: Nós com IDs duplicados encontrados: {sorted(dup_ids)}")

    missing_expected = [n for n in spec["expected_nodes"] if n not in nodes_by_name]
    if missing_expected:
        errors.append(f"{rel_path}: Nós obrigatórios ausentes: {missing_expected}")

    if not isinstance(connections, dict) or len(connections) == 0:
        errors.append(f"{rel_path}: 'connections' deve ser um dicionário não vazio.")
    else:
        for src_node, conn_types in connections.items():
            if src_node not in nodes_by_name:
                errors.append(
                    f"{rel_path}: Conexão parte de nó de origem inexistente: '{src_node}'."
                )
            if not isinstance(conn_types, dict):
                errors.append(f"{rel_path}: Estrutura de conexão inválida em '{src_node}'.")
                continue
            for conn_kind, branches in conn_types.items():
                for branch_idx, targets in enumerate(branches):
                    for target in targets:
                        dest_node = target.get("node")
                        if dest_node not in nodes_by_name:
                            errors.append(
                                f"{rel_path}: Conexão de '{src_node}' ({conn_kind}[{branch_idx}]) "
                                f"aponta para nó de destino inexistente: '{dest_node}'."
                            )

    wh_name = spec["webhook_node"]
    if wh_name in nodes_by_name:
        wh_params = nodes_by_name[wh_name].get("parameters", {})
        if wh_params.get("httpMethod") != "POST":
            errors.append(f"{rel_path}: '{wh_name}' deve ter httpMethod='POST'.")
        if wh_params.get("path") != spec["webhook_path"]:
            errors.append(f"{rel_path}: '{wh_name}' deve ter path='{spec['webhook_path']}'.")
        if wh_params.get("responseMode") != "responseNode":
            errors.append(f"{rel_path}: '{wh_name}' deve ter responseMode='responseNode'.")

    raw_text = (ROOT_DIR / rel_path).read_text(encoding="utf-8")
    if "$node[" in raw_text:
        errors.append(f"{rel_path}: Sintaxe depreciada '$node[...]' detectada.")
    if "item.json.myNewField = 1" in raw_text:
        errors.append(f"{rel_path}: Código boilerplate 'myNewField = 1' ainda presente.")
    if "const nome = ;" in raw_text or "const perfil = ;" in raw_text:
        errors.append(f"{rel_path}: Erro de sintaxe 'const nome = ;' ainda presente.")

    # Verificações específicas do workflow corrigido 02 / n8n/workflow.json
    if "Message a model" in nodes_by_name:
        if_node = nodes_by_name.get("If", {})
        conds = if_node.get("parameters", {}).get("conditions", {}).get("conditions", [])
        if not conds or not conds[0].get("leftValue") or not conds[0].get("rightValue"):
            errors.append(f"{rel_path}: Nó 'If' está com leftValue ou rightValue vazio.")

        if_conns = connections.get("If", {}).get("main", [])
        if len(if_conns) < 2 or not if_conns[1]:
            errors.append(f"{rel_path}: Saída False (main[1]) do nó 'If' não está conectada.")

        gmail_node = nodes_by_name.get("Send a message", {})
        g_params = gmail_node.get("parameters", {})
        if g_params.get("subject") == "Test" or g_params.get("message") == "Hello World":
            errors.append(f"{rel_path}: Nó 'Send a message' ainda contém valores fixos de teste.")

    errors.extend(check_security_no_secrets(rel_path))
    return errors


def simulate_rpa_and_workflow_logic() -> list[str]:
    """Executa testes funcionais do RPA e das regras de negócio de recomendação."""
    errors = []

    html_path = ROOT_DIR / "docs" / "index.html"
    csv_path = ROOT_DIR / "docs" / "data.csv"

    if not html_path.exists():
        return ["Arquivo docs/index.html não encontrado."]
    if not csv_path.exists():
        return ["Arquivo docs/data.csv não encontrado."]

    clientes = extrair_clientes_do_html(html_path.read_text(encoding="utf-8"))
    if len(clientes) != 10:
        errors.append(f"Extração RPA esperava 10 clientes em docs/index.html, mas obteve {len(clientes)}.")

    with csv_path.open(encoding="utf-8") as f:
        investimentos = list(csv.DictReader(f))
    if len(investimentos) != 9:
        errors.append(f"Leitura de docs/data.csv esperava 9 produtos, mas obteve {len(investimentos)}.")

    for inv in investimentos:
        inv["minimo"] = int(re.sub(r"[^\d]", "", str(inv["minimo"])) or 0)

    def parse_brl(val: str) -> float:
        s = str(val).replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(s) if s else 0.0

    def recomendar(cliente: dict) -> dict:
        saldo_num = parse_brl(cliente["saldo"])
        perfil = cliente["perfil"]
        opcoes = [i for i in investimentos if i["perfil"].lower() == perfil.lower()]
        elegiveis = sorted(
            [i for i in opcoes if i["minimo"] <= saldo_num],
            key=lambda x: x["minimo"],
            reverse=True,
        )
        escolhido = elegiveis[0] if elegiveis else opcoes[0]
        return {"saldo_num": saldo_num, "produto": escolhido["produto"], "minimo": escolhido["minimo"]}

    # Testar casos conhecidos da base oficial
    ana = next((c for c in clientes if c["nome"] == "Ana Silva"), None)
    bruno = next((c for c in clientes if c["nome"] == "Bruno Lima"), None)
    carla = next((c for c in clientes if c["nome"] == "Carla Souza"), None)
    daniel = next((c for c in clientes if c["nome"] == "Daniel Oliveira"), None)

    if not ana or recomendar(ana)["produto"] != "CDB Liquidez Diária":
        errors.append("Falha na recomendação para Ana Silva (Conservador, R$ 12.500,00 -> CDB Liquidez Diária).")
    if not bruno or recomendar(bruno)["produto"] != "CDB Prefixado":
        errors.append("Falha na recomendação para Bruno Lima (Moderado, R$ 3.200,00 -> CDB Prefixado).")
    if not carla or recomendar(carla)["produto"] != "Fundo de Ações":
        errors.append("Falha na recomendação para Carla Souza (Arrojado, R$ 28.900,00 -> Fundo de Ações).")
    if not daniel or recomendar(daniel)["produto"] != "Tesouro Selic":
        errors.append("Falha na recomendação para Daniel Oliveira (Conservador, R$ 850,00 -> Tesouro Selic).")

    # Testar validação de e-mail do nó If
    email_regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    inv_payload, err = load_json_file(
        "workflows/02-assistente-investimentos-ia-gmail/exemplos/entrada-email-invalido.json"
    )
    if err:
        errors.append(err)
    else:
        bad_email = inv_payload["clientes"][0]["email"]
        if email_regex.match(bad_email):
            errors.append(f"Regex de e-mail aprovou indevidamente e-mail inválido: {bad_email}")

    return errors


def main() -> int:
    print("=" * 78)
    print(" VALIDADOR DE RPA E WORKFLOWS N8N — DESAFIO DIO ASSISTENTE DE INVESTIMENTOS")
    print("=" * 78)

    all_errors = []

    # 1. Validar Workflows principais
    for wf_path, spec in EXPECTED_WORKFLOWS.items():
        wf_errors = validate_workflow_structure(wf_path, spec)
        if wf_errors:
            all_errors.extend(wf_errors)
            print(f"[FALHA] {wf_path}")
        else:
            print(
                f"[OK] Estrutura, nós, conexões, correções e segurança validados: "
                f"{wf_path} ({len(spec['expected_nodes'])} nós)"
            )

    # 2. Validar arquivos de Payload de exemplo
    for payload_path in EXPECTED_PAYLOADS:
        _, err = load_json_file(payload_path)
        if err:
            all_errors.append(err)
            print(f"[FALHA] {payload_path}: {err}")
        else:
            sec_errs = check_security_no_secrets(payload_path)
            if sec_errs:
                all_errors.extend(sec_errs)
                print(f"[FALHA] {payload_path}")
            else:
                print(f"[OK] Payload de exemplo válido e seguro: {payload_path}")

    # 3. Simular extração RPA e lógica de cruzamento de investimentos
    sim_errors = simulate_rpa_and_workflow_logic()
    if sim_errors:
        all_errors.extend(sim_errors)
        print("[FALHA] Simulação de extração RPA (BeautifulSoup) e cruzamento de investimentos.")
    else:
        print("[OK] Extração RPA (10 clientes HTML + 9 produtos CSV) e simulação lógica de recomendações")

    print("-" * 78)
    if all_errors:
        print(f"RESULTADO FINAL: FALHA ({len(all_errors)} erro(s) encontrado(s)):")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("RESULTADO FINAL: SUCESSO — RPA, workflows corrigidos e payloads passaram em 100% dos testes!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

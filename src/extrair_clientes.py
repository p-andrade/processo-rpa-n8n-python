#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de RPA (Robotic Process Automation) — Extração de Clientes e Integração com n8n
Projeto: Desafio DIO — Processo de RPA com N8N e Python (Assistente de Investimentos)

Responsabilidades deste script:
1. Acessar a página web de clientes (via GitHub Pages oficial da DIO ou arquivo local docs/index.html).
2. Extrair os dados da tabela HTML (#clientes tbody tr) usando BeautifulSoup (se instalado) ou
   html.parser nativo da biblioteca padrão do Python (zero dependências obrigatórias).
3. Estruturar a lista de clientes (nome, email, saldo, perfil) em formato JSON padronizado.
4. Enviar o payload via HTTP POST para o Webhook do n8n (quando N8N_WEBHOOK_URL estiver configurado)
   ou executar em modo de simulação/inspeção segura (--dry-run).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

ROOT_DIR = Path(__file__).resolve().parent.parent
LOCAL_HTML_PATH = ROOT_DIR / "docs" / "index.html"
URL_PAGINA_OFICIAL = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"
DEFAULT_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/Clientes")


class _TabelaClientesParser(HTMLParser):
    """Parser HTML nativo (stdlib) para extrair #clientes tbody tr td sem depender de pacotes externos."""

    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.current_row = []
        self.current_cell = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.in_tbody = True
        elif self.in_tbody and tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif self.in_tr and tag == "td":
            self.in_td = True
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        elif tag == "tr" and self.in_tr:
            self.in_tr = False
            if len(self.current_row) >= 4:
                self.rows.append(self.current_row[:4])
        elif tag == "td" and self.in_td:
            self.in_td = False
            self.current_row.append("".join(self.current_cell).strip())

    def handle_data(self, data):
        if self.in_td:
            self.current_cell.append(data)


def obter_html_clientes(usar_local: bool = False) -> str:
    """Obtém o HTML da página de clientes da URL oficial ou do arquivo local de contingência."""
    if not usar_local:
        try:
            if requests is not None:
                resp = requests.get(URL_PAGINA_OFICIAL, timeout=10)
                resp.raise_for_status()
                resp.encoding = "utf-8"
                return resp.text
            req = urllib.request.Request(URL_PAGINA_OFICIAL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8")
        except Exception as exc:
            print(f"[AVISO] Falha ao acessar URL remota ({exc}). Utilizando copia local: {LOCAL_HTML_PATH}")

    if LOCAL_HTML_PATH.exists():
        return LOCAL_HTML_PATH.read_text(encoding="utf-8")

    raise FileNotFoundError(f"Arquivo HTML local não encontrado em {LOCAL_HTML_PATH}")


def extrair_clientes_do_html(html: str) -> list[dict]:
    """Faz o parsing da tabela #clientes e retorna a lista de dicionários de clientes."""
    clientes = []

    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        linhas = soup.select("#clientes tbody tr")
        for linha in linhas:
            colunas = linha.find_all("td")
            if len(colunas) < 4:
                continue
            clientes.append(
                {
                    "nome": colunas[0].get_text(strip=True),
                    "email": colunas[1].get_text(strip=True),
                    "saldo": colunas[2].get_text(strip=True),
                    "perfil": colunas[3].get_text(strip=True),
                }
            )
        return clientes

    parser = _TabelaClientesParser()
    parser.feed(html)
    for col in parser.rows:
        clientes.append(
            {
                "nome": col[0],
                "email": col[1],
                "saldo": col[2],
                "perfil": col[3],
            }
        )
    return clientes


def enviar_para_webhook(clientes: list[dict], webhook_url: str, timeout: int = 30) -> dict:
    """Envia a lista de clientes via HTTP POST para o Webhook do n8n."""
    payload = {"clientes": clientes}
    if requests is not None:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=timeout,
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"status_code": response.status_code, "raw_body": response.text}

    body_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=body_bytes,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw_text = resp.read().decode("utf-8")
        try:
            return json.loads(raw_text)
        except ValueError:
            return {"status_code": resp.status, "raw_body": raw_text}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Robô RPA em Python para extração de clientes e envio ao Webhook do n8n."
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Lê diretamente o arquivo local docs/index.html sem requisitar o GitHub Pages.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas extrai e exibe o payload JSON no terminal, sem disparar requisição POST ao n8n.",
    )
    parser.add_argument(
        "--webhook-url",
        default=DEFAULT_WEBHOOK_URL,
        help=f"URL do Webhook do n8n (padrão: {DEFAULT_WEBHOOK_URL}).",
    )
    args = parser.parse_args()

    print("=" * 78)
    print(" ROBO RPA PYTHON — EXTRACAO DE CLIENTES PARA ASSISTENTE DE INVESTIMENTOS")
    print("=" * 78)

    html = obter_html_clientes(usar_local=args.local)
    clientes = extrair_clientes_do_html(html)

    print(f"[OK] Total de clientes extraidos da tabela HTML: {len(clientes)}\n")
    for idx, c in enumerate(clientes, start=1):
        print(f"  {idx:02d}. {c['nome']:<18} | {c['email']:<20} | {c['saldo']:<13} | Perfil: {c['perfil']}")

    payload = {"clientes": clientes}

    if args.dry_run:
        print("\n[MODO DRY-RUN] Payload JSON pronto para envio ao Webhook POST /Clientes:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"\n[INFO] Enviando {len(clientes)} clientes via POST para: {args.webhook_url} ...")
    try:
        resposta = enviar_para_webhook(clientes, args.webhook_url)
        print("[SUCESSO] Resposta recebida do workflow n8n:")
        print(json.dumps(resposta, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"[AVISO] Nao foi possivel conectar ao servidor n8n em '{args.webhook_url}': {exc}")
        print("[DICA] Certifique-se de que o n8n esta em execucao e com o Webhook escutando, ou use --dry-run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

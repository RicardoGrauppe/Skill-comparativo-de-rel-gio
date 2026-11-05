#!/usr/bin/env python3
"""Salva em <rodada>/assets/ as fotos oficiais que ainda vêm da internet e aponta o dados.json para elas.

Uso:  python3 baixar_fotos.py "<pasta da rodada>"

Faz um download comum, sem se passar por navegador. Se a marca recusar, para e avisa:
não se contorna bloqueio de site.
"""
import json
import os
import sys
import urllib.request

ASSINATURAS = {b"\x89PNG": "png", b"\xff\xd8\xff": "jpg", b"RIFF": "webp"}


def baixar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "carrossel-comparativo"})
    with urllib.request.urlopen(pedido, timeout=60) as resposta:
        return resposta.read()


def extensao(dados):
    for assinatura, ext in ASSINATURAS.items():
        if dados.startswith(assinatura):
            return ext
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rodada = os.path.abspath(sys.argv[1])
    caminho = os.path.join(rodada, "dados.json")
    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)

    mudou = False
    for lado in ("a", "b"):
        foto = d[lado]["foto"]
        if not foto["src"].startswith("http"):
            continue
        try:
            dados = baixar(foto["src"])
        except Exception as erro:
            sys.exit(f"Parado: a foto de {d[lado]['marca']} não baixou ({erro}). Peça o arquivo ao Ricardo Grauppe.")
        ext = extensao(dados)
        if not ext:
            sys.exit(f"Parado: a resposta de {d[lado]['marca']} não é uma imagem. Peça o arquivo ao Ricardo Grauppe.")
        os.makedirs(os.path.join(rodada, "assets"), exist_ok=True)
        local = f"assets/{lado}.{ext}"
        with open(os.path.join(rodada, local), "wb") as f:
            f.write(dados)
        foto["src_oficial"] = foto["src"]
        foto["src"] = local
        mudou = True
        print(f"Salva: {local}")

    if mudou:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

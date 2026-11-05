#!/usr/bin/env python3
"""Monta o carrossel oficial, em português e em inglês, a partir do dados.json de uma rodada.

Uso:  python3 montar.py "<pasta da rodada>"
Lê:   <rodada>/dados.json
Gera: <rodada>/carrossel.html  (português = #1 a #5, inglês = #6 a #10)

O layout é o mesmo nos dois idiomas. Aqui só se troca o texto, se calcula a geometria
dos relógios, sempre na escala real, e se recusa o que quebra as regras do pipeline.
"""
import html
import json
import os
import re
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(AQUI, "01 - Carrossel", "modelo.html")
IDIOMAS = [("pt", "Português"), ("en", "English")]
FALTOU = object()


def falha(msg):
    sys.exit(f"Reprovado: {msg}")


def validar(d):
    for lado in ("a", "b"):
        if d[lado]["preco_num"] <= 0 or d[lado]["mm"] <= 0:
            falha(f"preço ou diâmetro inválido em {lado}.")
    if d["a"]["preco_num"] >= d["b"]["preco_num"]:
        falha("o relógio a precisa ser o mais barato.")
    for idioma, _ in IDIOMAS:
        t = d["textos"][idioma]
        p2 = t["pagina2"]
        if len(p2["em_comum"]) > 4:
            falha(f"{idioma}: Em comum tem mais de 4 itens.")
        if len(p2["diferencas"]) > 7:
            falha(f"{idioma}: Principais diferenças tem mais de 7 linhas.")
        if len(t["pagina3"]["itens"]) != 3:
            falha(f"{idioma}: o fato estranho precisa de exatamente 3 itens.")
        if re.search(r"\b(vph|hz|calibre|caliber|cal\.)\b", json.dumps(p2["em_comum"], ensure_ascii=False), re.I):
            falha(f"{idioma}: jargão nas pills de Em comum.")
    texto = json.dumps(d["textos"], ensure_ascii=False)
    for proibido in ("—", "espião", "espionagem"):
        if proibido in texto:
            falha(f'texto proibido nos dados: "{proibido}".')


def foto_existe(rodada, src):
    if not src.startswith("http") and not os.path.exists(os.path.join(rodada, src)):
        falha(f"foto não encontrada: {src}")


def corte(foto):
    """Corte opcional da foto, para tirar sombra embutida que suja o fundo."""
    return f";clip-path:polygon({foto['clip']})" if foto.get("clip") else ""


def imagem(foto, mm, px_mm, centro_x, centro_y):
    """Largura e posição para o aro ter o tamanho real e o centro cair no ponto pedido."""
    w = mm * px_mm / foto["d"]
    return f"left:{centro_x - foto['cx'] * w:.1f}px;top:{centro_y - foto['cy'] * w:.1f}px;width:{w:.1f}px{corte(foto)}"


def recorte(foto, centro_x, centro_y, d):
    w = d / foto["d"]
    return f"width:{w:.1f}px;height:{w:.1f}px;left:{centro_x - foto['cx'] * w:.1f}px;top:{centro_y - foto['cy'] * w:.1f}px{corte(foto)}"


def deitado(foto, mm, px_mm, centro_x, centro_y, giro):
    """Relógio na horizontal, em escala real: gira em torno do centro do mostrador."""
    w = mm * px_mm / foto["d"]
    ox, oy = foto["cx"] * w, foto["cy"] * w
    return (
        f"left:{centro_x - ox:.1f}px;top:{centro_y - oy:.1f}px;width:{w:.1f}px;"
        f"transform-origin:{ox:.1f}px {oy:.1f}px;transform:rotate({giro}deg){corte(foto)}"
    )


def campos(d, t):
    a, b = d["a"], d["b"]
    p1, p2, p3, p4, p5 = (t[f"pagina{n}"] for n in range(1, 6))
    c = {}
    for k, r in (("a", a), ("b", b)):
        c[f"{k}.marca"], c[f"{k}.marca_caixa"] = r["marca"], r["marca"].upper()
        c[f"{k}.modelo"], c[f"{k}.ref"] = r["modelo"], r["ref"]
        c[f"{k}.preco"] = t["preco"][k]
        c[f"{k}.mm_txt"] = f"{r['mm']:g} mm"
        c[f"{k}.foto"] = r["foto"]["src"]

    # Capa: 10 px por mm e título em duas linhas na largura dos relógios
    c["capa.a"] = imagem(a["foto"], a["mm"], 10, 255, 613)
    c["capa.b"] = imagem(b["foto"], b["mm"], 10, 780, 613)
    c["capa.titulo"], c["capa.linha2"], c["capa.deslize"] = p4["titulo"], p4["linha2"], p4["capa"]
    c["capa.tam1"], c["capa.tam2"] = p4["tamanhos"]

    # Revelação: relógios deitados a 12,5 px por mm
    c["rev.titulo"], c["rev.linha2"] = p1["titulo"], p1["linha2"]
    c["rev.a"] = deitado(a["foto"], a["mm"], 12.5, 300, 470, -90)
    c["rev.b"] = deitado(b["foto"], b["mm"], 12.5, 780, 1040, 90)

    # Resumo: 5,5 px por mm
    c["res.a"] = imagem(a["foto"], a["mm"], 5.5, 330, 368)
    c["res.b"] = imagem(b["foto"], b["mm"], 5.5, 750, 368)
    for k in ("titulo", "subtitulo", "fechamento", "rotulo_comum", "rotulo_diferencas"):
        c[f"res.{k}"] = p2[k]

    # Fato estranho: os dois aros do mesmo tamanho, para olhar o material
    for k in ("titulo", "subtitulo", "secao", "fechamento", "surpresa_a", "surpresa_b", "legenda_a", "legenda_b"):
        c[f"fato.{k}"] = p3[k]
    c["fato.a"] = recorte(a["foto"], 270, 200, 440)
    c["fato.b"] = recorte(b["foto"], 810, 200, 440)

    # Chamada: relógios inteiros, a 9,29 px por mm
    c["cta.titulo"], c["cta.linha2"], c["cta.botao"] = p5["titulo"], p5["linha2"], p5["botao"]
    # Marca longa não pode quebrar linha: as duas descem juntas para caber em uma só
    maior = max(len(a["marca"]), len(b["marca"]))
    tam = min(48, int(480 / (0.8 * maior)))
    c["cta.tam"], c["cta.letra"] = tam, round(tam * 0.8)
    c["cta.a"] = imagem(a["foto"], a["mm"], 9.29, 280, 590)
    c["cta.b"] = imagem(b["foto"], b["mm"], 9.29, 800, 590)

    esc = {k: html.escape(str(v), quote=True) for k, v in c.items()}
    for k, r in (("a", a), ("b", b)):
        esc[f"{k}.barras"] = "".join(
            f'<i class="bar" style="left:{x["l"]}%;top:{x["t"]}%;width:{x["w"]}%;height:{x["h"]}%"></i>' for x in r["censura"]
        )
    e = html.escape
    esc["CHIPS"] = "".join(f'<div class="chip">{e(x)}</div>' for x in p2["em_comum"])
    linhas = ""
    for x in p2["diferencas"]:
        ca = ' class="win"' if x.get("vence") == "a" else ""
        cb = ' class="win"' if x.get("vence") == "b" else ""
        linhas += f'<tr><th>{e(x["nome"])}</th><td{ca}>{e(x["a"])}</td><td{cb}>{e(x["b"])}</td></tr>'
    esc["LINHAS"] = linhas
    esc["ALTURA"] = str({7: 48, 6: 55, 5: 64, 4: 77}.get(len(p2["diferencas"]), 48))
    esc["EXTRAS"] = "".join(f'<div class="extra"><b>{e(x["titulo"])}</b><span>{e(x["texto"])}</span></div>' for x in p3["itens"])
    return esc


SCRIPT = """<script>
  var deck = document.getElementById('deck');
  function layout() {
    var n = location.hash.replace('#', '');
    var solo = /^([1-9]|10)$/.test(n);
    document.body.classList.toggle('solo', solo);
    document.querySelectorAll('.slide').forEach(function (s) {
      s.classList.toggle('active', s.dataset.slide === n);
    });
    deck.style.zoom = solo ? 1 : Math.min(innerWidth / (5 * 1080 + 4 * 32 + 64), 1);
  }
  addEventListener('resize', layout);
  addEventListener('hashchange', layout);
  layout();
</script>"""


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rodada = os.path.abspath(sys.argv[1])
    with open(os.path.join(rodada, "dados.json"), encoding="utf-8") as f:
        d = json.load(f)
    validar(d)
    for src in (d["a"]["foto"]["src"], d["b"]["foto"]["src"]):
        foto_existe(rodada, src)

    with open(MODELO, encoding="utf-8") as f:
        modelo = f.read()
    corpo = ""
    for i, (idioma, nome) in enumerate(IDIOMAS):
        c = campos(d, d["textos"][idioma])
        c["idioma"] = idioma
        for j in range(5):
            c[f"n{j + 1}"] = str(i * 5 + j + 1)

        def troca(m):
            valor = c.get(m.group(1), FALTOU)
            if valor is FALTOU:
                falha(f"campo sem valor no modelo: {m.group(1)}")
            return valor

        paginas = re.findall(r"<section .*?</section>", re.sub(r"\{\{([\w.]+)\}\}", troca, modelo), re.S)
        # Nomes só para a visualização: não aparecem em página sozinha nem no export
        corpo += f'<div class="row-name">{nome}</div>\n'
        for j, pagina in enumerate(paginas):
            corpo += f'<div class="cell"><div class="page-name">{idioma}{j + 1}</div>\n{pagina}\n</div>\n'

    os.makedirs(os.path.join(rodada, "fonts"), exist_ok=True)
    shutil.copy(os.path.join(AQUI, "fonts", "Montserrat.ttf"), os.path.join(rodada, "fonts", "Montserrat.ttf"))
    with open(os.path.join(AQUI, "estilo.css"), encoding="utf-8") as f:
        css = f.read()
    saida = (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(d['slug'])}</title>\n<style>\n{css}</style>\n</head>\n<body>\n"
        f'<div id="deck">\n{corpo}</div>\n{SCRIPT}\n</body>\n</html>\n'
    )
    destino = os.path.join(rodada, "carrossel.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(saida)
    remotas = sorted(set(re.findall(r'src="(http[^"]+)"', saida)))
    print(f"Pronto: {destino}")
    if remotas:
        print(f"Atenção: {len(remotas)} foto(s) ainda vêm da internet. Salve em assets/ antes de exportar.")


if __name__ == "__main__":
    main()

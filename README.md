# Comparativo de relógio

Pipeline que cria um carrossel de Instagram de 5 páginas comparando dois relógios parecidos com preços muito distantes, em português e inglês.

## Como usar

Abra esta pasta no Claude Code e peça: "roda o Carrossel Comparativo". Para escolher o par, é só dizer quais relógios quer. Sem indicação, o agente escolhe.

## O que precisa

- macOS, com Google Chrome instalado
- Python 3 com Pillow (`pip3 install pillow`)

Para ver o HTML no navegador, rode `python3 -m http.server 8864` nesta pasta e abra `http://localhost:8864/output/<rodada>/carrossel.html`.

## Rodadas prontas

Os JPEGs de 2160x2700 estão em `output/<rodada>/export/pt` e `export/en`:

- `2026-11-04-prx-vs-royal-oak`: Tissot PRX e Audemars Piguet Royal Oak
- `2026-11-04-speedtimer-vs-daytona`: Seiko Speedtimer e Rolex Daytona

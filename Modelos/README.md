---
type: reference
status: active
area: nexus
pipeline: carrossel-comparativo
created: 2026-11-04
updated: 2026-11-04
tags: [relogios, carrossel, modelos]
---

# Modelo do Carrossel Comparativo

Um layout de 5 páginas, `01 - Carrossel/`, montado em dois idiomas a partir do mesmo `dados.json`. Nasceu da rodada `2026-11-04-hydroconquest-vs-seamaster`.

| Idioma | Páginas | Nomes na visualização |
|---|---|---|
| Português | `#1` a `#5` | `pt1` a `pt5` |
| Inglês | `#6` a `#10` | `en1` a `en5` |

Os nomes aparecem só na visão geral, não em página sozinha nem no export.

## Foto, cortes e posições

Cada relógio entra com uma única foto oficial, de frente, inteira e sem fundo. As 5 páginas reaproveitam essa foto, e o `montar.py` aplica sempre os mesmos cortes, escalas e posições. Por rodada, só se informa o centro do mostrador (`cx`, `cy`), o diâmetro do aro (`d`) e as barras da capa (`censura`).

## Arquivos

- `estilo.css`: visual do carrossel.
- `01 - Carrossel/modelo.html`: as 5 páginas, com campos `{{...}}`.
- `montar.py`: calcula a escala real dos relógios, confere as regras e gera `carrossel.html` na pasta da rodada.
- `baixar_fotos.py`: salva as fotos oficiais em `assets/` com um download comum e aponta o `dados.json` para elas. Para se a marca recusar.
- `exportar.sh`: baixa as fotos, monta de novo e gera os JPEGs em `export/pt` e `export/en`, em 2160x2700, 300 DPI e sRGB.

## Escala dos relógios

O `montar.py` usa o diâmetro em mm e a medida da foto para dar a cada relógio o tamanho real, em pixels por mm fixos:

| Página | Pixels por mm |
|---|---|
| 1. Capa | 10 |
| 2. Revelação | 12,5 |
| 3. Resumo | 5,5 |
| 5. Chamada | 9,29 |

Na página 4, os dois aros têm o mesmo tamanho, de propósito, porque o assunto é o material. Essa página não compara tamanho.

## Armadilhas

- Foto sem fundo muda muito de enquadramento entre marcas. `cx`, `cy` e `d` precisam ser medidos em cada foto.
- A sombra embutida em algumas fotos aparece no fundo claro e vira uma mancha nos fundos escuros. Quando ela aparecer, usar `foto.clip`: os pontos de um `polygon` em porcentagem da imagem, sem encostar no relógio.
- A foto precisa ser quadrada, porque a capa e o fato estranho usam altura igual à largura. Foto retrato fica achatada. Na Audemars Piguet, o parâmetro `extend` da própria URL oficial completa a tela sem mexer no relógio.
- Relógio com aro muito maior que 45 mm pode encostar nas laterais da capa. Se acontecer, avisar antes de mudar a escala.
- Título da capa muda de tamanho conforme o texto: `pagina4.tamanhos` guarda os dois tamanhos de cada idioma.

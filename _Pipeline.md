---
type: reference
status: active
area: nexus
pipeline: carrossel-comparativo
created: 2026-11-04
updated: 2026-11-04
tags: [relogios, carrossel, pipeline, ia]
---

# Pipeline: Carrossel Comparativo

> **Input:** nada, ou um par de relógios sugerido pelo Ricardo Grauppe.
> **Output:** o carrossel oficial de 5 páginas em dois modelos, português e inglês, em HTML e em JPEG 2160x2700 pronto para o Instagram, com os dados conferidos.
> **Roda sozinho, do par ao JPEG:** não para para aprovação dele. O controle é do Revisor.
> **Um pipeline, dois modelos:** par, ficha e layout são os mesmos. Muda só o idioma do texto, inclusive o formato dos números. Nunca rodar a pesquisa duas vezes para o mesmo par.

## A pegada, em toda edição

Topo de funil, para leigo. O carrossel deixa a pulga atrás da orelha: "ué, parece que o mais barato é melhor do que o mais caro". Os pares são relógios que parecem inspirados um no outro, na pegada "quem copiou quem".

A pergunta fica no ar e o que o mais caro entrega de verdade continua aparecendo. A dúvida vem de fatos conferidos, nunca de esconder informação. Ninguém afirma que uma marca copiou a outra sem fonte.

## Os agentes

| # | Agente | Entrega | Salva em |
|---|---|---|---|
| 1 | [[01 - Cacador de Pares]] | O melhor par, escolhido por fóruns e opinião comum, com ângulo | `par.md` |
| 2 | [[02 - Pesquisador de Fichas]] | Ficha com fonte em cada dado | `ficha.md` |
| 3 | [[03 - Copywriter]] | Copy das 5 páginas e legenda, nos dois idiomas | `dados.json` e `legenda.md` |
| 4 | [[04 - Diagramador]] | Fotos, medidas e o carrossel montado | `dados.json` e `carrossel.html` |
| 5 | [[05 - Revisor]] | Reprova ou aprova fatos, copy e visual | `revisao.md` |
| 6 | [[06 - Exportador]] | Um JPEG de alta resolução por página, pronto para o Instagram | `export/` |

Tudo em fila: cada etapa depende da anterior, então não há ganho em paralelizar. O Revisor volta a peça para o agente responsável até não sobrar nenhum item reprovado, com limite de 5 voltas em cada checagem. Depois disso, entrega a melhor versão e lista o que ficou aberto.

## Sem paradas

Decisão do Ricardo Grauppe em 2026-11-04: a rodada vai do par ao JPEG sem esperar por ele.

1. **Par e ângulo:** o agente 1 escolhe e segue.
2. **Copy:** segue para o HTML depois de aprovada na checagem de fatos do Revisor.
3. **Export:** com o HTML aprovado pelo Revisor, o agente 6 gera os JPEGs. `sh Modelos/exportar.sh "output/<rodada>"`.
4. **Fim da rodada:** entregar a pasta `export/` e o link do HTML, com a copy, o par escolhido, o motivo da escolha e o que ficou aproximado ou aberto. Publicar continua com ele.

Se ele trouxer correção depois da entrega, ela volta pelo agente responsável e pelo Revisor.

## As 5 páginas

| Página | Função | Estilo |
|---|---|---|
| 1. Capa | Sem os nomes, qual você escolheria? Relógios A e B, sem marca | Fundo claro, título em duas linhas na largura dos relógios, seta depois do texto de deslizar |
| 2. Revelação | Nomes, tamanho e preço, com a pergunta sobre a diferença | Metade clara e metade marinho, com os relógios deitados |
| 3. Resumo | "Em comum" e principais diferenças | Fundo claro com luz, blocos e tabela sobreposta à faixa marinho |
| 4. Fato estranho | O fato que não faz sentido e o que o mais caro tem a mais | Estúdio escuro |
| 5. Chamada | Depois de tudo isso, a opinião continua a mesma? | Marinho, relógios inteiros, marcas em destaque e botão com balão |

Sequência de referência, da legenda Casio e Tudor: mesma linguagem visual, detalhes que separam, o que têm em comum e a pergunta final.

## Regras que ele já definiu

**Copy**
- "Em comum" tem no máximo 4 itens, os mais importantes e óbvios para o leigo.
- "Principais diferenças" tem no máximo 7 linhas, escolhidas por essa pegada e sem jargão (calibre e vph ficam de fora).
- Sem "Destaque técnico" e sem linhas de fonte ou data nas páginas. Valor aproximado leva `~`.
- 300 m é resistência à água, nunca profundidade: "resistem a 300 m", jamais "descem 300 m".
- Sem rótulos genéricos de página como "Comparativo" ou "Ficha técnica". O título diz alguma coisa.
- O inglês mantém o mesmo sentido e a mesma função em cada página, com número no formato americano (`$2,400`, `13.8 mm`).

**Visual**
- Texto centralizado, fonte Montserrat, relógios sempre na escala real.
- Relógio aparece inteiro. Nunca usar só o mostrador recortado em círculo.
- Título da capa em duas linhas, na largura dos relógios, direto no fundo claro. A capa não leva bloco de cor nem barra azul.
- Preço sem destaque: valor menor e peso médio, sem ocupar o foco da página.
- Na chamada, a marca é o maior texto abaixo dos relógios, e o botão leva o ícone de balão.
- Ícones da biblioteca Solar. Profundidade vem de luz, camadas, textura e sobreposição, com sombra bem sutil.
- Sem borda como separação e sem sobrancelha em caixa alta.

Regras gerais do texto: [[tom-de-voz]].

## Fotos

**Padrão fixo:** cada relógio usa uma única foto oficial, de frente, inteira e sem fundo. Essa foto serve para as 5 páginas nos dois idiomas, só mudando corte, escala e posição. Posições e cortes são sempre os do modelo, em toda rodada, e não se escolhem fotos de detalhe, de fundo da caixa ou de ambiente.

As fotos oficiais das páginas das marcas estão autorizadas pelo Ricardo Grauppe. Alguns sites recusam download por script, e não se contorna essa proteção. O caminho é:

1. Usar a URL oficial da foto de frente no `dados.json` enquanto a peça está em revisão, carregando pelo navegador. Preferir a maior versão que a marca oferece, porque o export é em 2160x2700.
2. No export, o `exportar.sh` tenta um download comum e passa o `dados.json` para os arquivos locais em `assets/`.
3. Se a marca recusar, a rodada entrega o HTML aprovado e pede o arquivo a ele.

## Como montar

```bash
python3 Modelos/montar.py "output/<YYYY-MM-DD>-<slug>"
```

O script monta os dois idiomas e recusa peça fora das regras (mais de 4 itens em comum, mais de 7 diferenças, travessão, relógio `a` que não seja o mais barato). Preview: `python3 -m http.server 8864` nesta pasta, em `/output/<rodada>/carrossel.html`. Página sozinha em tamanho real: `#1` a `#5` em português e `#6` a `#10` em inglês.

## Onde salvar

```
output/<YYYY-MM-DD>-<slug>/
├── par.md            ← par escolhido e ângulo
├── ficha.md          ← dados com fonte
├── dados.json        ← a peça em dados: fotos, medidas e textos nos dois idiomas
├── legenda.md        ← legenda do post, nos dois idiomas
├── revisao.md        ← itens reprovados e aprovados
├── carrossel.html    ← gerado, não editar à mão
├── assets/           ← fotos locais, salvas no export
├── fonts/            ← copiada pelo script
└── export/pt e en/   ← JPEGs 2160x2700, 300 DPI, sRGB
```

Correção que vale sempre entra em `Modelos/` ou nesta página. Correção só desta rodada entra no `dados.json`.

## Rodadas

- `2026-11-04-hydroconquest-vs-seamaster`: Longines HydroConquest 39 mm e Omega Seamaster Diver 300M. Peça que originou o modelo. Fotos ainda pela URL oficial, sem export. A espessura da Longines é aproximada (~12 mm) por falta de número oficial da referência.
- `2026-11-04-prx-vs-royal-oak`: Tissot PRX 40 mm e Audemars Piguet Royal Oak 41 mm. Par escolhido pelo Ricardo Grauppe, antes da regra sem paradas. Exportada em JPEG, com fotos locais.
- `2026-11-04-speedtimer-vs-daytona`: Seiko Speedtimer SSC961 e Rolex Cosmograph Daytona 126500LN. Primeira rodada com par escolhido pelo agente, sem aprovação até o JPEG. A opinião comum vem de revista e de dono, porque o Reddit recusou o acesso.

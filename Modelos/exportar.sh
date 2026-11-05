#!/bin/sh
# Gera as 10 páginas prontas para o Instagram: JPEG 2160x2700 (4:5), sRGB, 300 DPI.
# Uso: sh exportar.sh "<pasta da rodada>"
set -e
AQUI=$(cd "$(dirname "$0")" && pwd)
RODADA=$(cd "$1" && pwd)
python3 "$AQUI/baixar_fotos.py" "$RODADA"
python3 "$AQUI/montar.py" "$RODADA"
if grep -q 'src="http' "$RODADA/carrossel.html"; then
  echo "Parado: ainda há fotos vindas da internet."
  exit 1
fi
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
URL=$(python3 -c "import sys,urllib.parse;print('file://'+urllib.parse.quote(sys.argv[1]))" "$RODADA/carrossel.html")
TMP=$(mktemp -d)
n=1
for idioma in pt en; do
  mkdir -p "$RODADA/export/$idioma"
  for pagina in 1 2 3 4 5; do
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
      --force-color-profile=srgb --window-size=1080,1350 --virtual-time-budget=5000 \
      --user-data-dir="$TMP/perfil" --screenshot="$TMP/p.png" "$URL#$n" >/dev/null 2>&1
    SAIDA="$RODADA/export/$idioma/pagina-$pagina.jpg"
    python3 - "$TMP/p.png" "$SAIDA" <<'PY'
import sys
from PIL import Image
imagem = Image.open(sys.argv[1]).convert("RGB")
if imagem.size != (2160, 2700):
    sys.exit(f"Parado: {sys.argv[2]} saiu em {imagem.size} em vez de 2160x2700.")
with open("/System/Library/ColorSync/Profiles/sRGB Profile.icc", "rb") as perfil:
    imagem.save(sys.argv[2], "JPEG", quality=95, subsampling=0, optimize=True, dpi=(300, 300), icc_profile=perfil.read())
PY
    n=$((n + 1))
  done
done
rm -rf "$TMP"
echo "Exportado em $RODADA/export/"

#!/usr/bin/env bash
# Reproduce el video completo del proyecto de punta a punta.
# Requisitos: g++ (C++17), python3 con matplotlib, ffmpeg.
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "== 1. Compilando el Segment Tree (C++) =="
g++ -std=c++17 -O2 -o src/segtree src/main.cpp
(cd src && ./segtree)

echo "== 2. Generando escenas animadas =="
mkdir -p animation/norm
mkdir -p video
python3 animation/animate.py src/steps_main.json \
  "Segment Tree - Build, Query(1,4) y Update(3,10)" animation/out_main.mp4 5 3
python3 animation/animate.py src/steps_edge_single.json \
  "Caso borde: arreglo de un solo elemento" animation/out_edge_single.mp4 5 5
python3 animation/animate.py src/steps_edge_full_range.json \
  "Caso borde: query sobre el rango completo" animation/out_edge_full.mp4 5 3

echo "== 3. Generando slides de titulo y complejidad =="
python3 animation/slides.py animation/title.mp4 5 \
  "Anima tu Estructura de Datos" "Segment Tree" \
  "CS2023 - Algoritmos y Estructuras de Datos" "Integrantes: André Valle Enriquez"
python3 animation/slides.py animation/complexity.mp4 10 \
  "Analisis de complejidad" \
  "Build: O(N) - visita cada nodo una vez al construir" \
  "Update (point update): O(log N) - un camino raiz-hoja" \
  "Query (range sum): O(log N) - a lo sumo O(log N) nodos por nivel" \
  "Espacio: O(N) - arreglo de tamano 4N"

echo "== 4. Normalizando resolucion (1280x720) =="
normalize() {
  in=$1; color=$2; out=animation/norm/$(basename "$in")
  ffmpeg -y -i "$in" -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=$color,fps=15" \
    -c:v libx264 -pix_fmt yuv420p "$out" -loglevel error
}
normalize animation/title.mp4 "#2d3436"
normalize animation/out_main.mp4 "white"
normalize animation/out_edge_single.mp4 "white"
normalize animation/out_edge_full.mp4 "white"
normalize animation/complexity.mp4 "#2d3436"

echo "== 5. Concatenando video final =="
cat > animation/norm/concat_list.txt << EOF
file 'title.mp4'
file 'out_main.mp4'
file 'out_edge_single.mp4'
file 'out_edge_full.mp4'
file 'complexity.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i animation/norm/concat_list.txt \
  -c:v libx264 -pix_fmt yuv420p video/segment_tree_video.mp4 -loglevel error

echo "Listo: video/segment_tree_video.mp4"

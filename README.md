# Anima tu Estructura de Datos — Segment Tree

Proyecto Final 1 del curso **Algoritmos y Estructuras de Datos**.

Video educativo que explica y demuestra visualmente el funcionamiento de un
**Segment Tree** (range sum query + point update), con una animación generada
a partir de una implementación real del algoritmo en C++.

**Integrante:** André Valle Enriquez

## Contenido del video generado

1. Título y créditos.
2. `build` del árbol sobre el arreglo `[2, 4, 5, 7, 8, 9]`, luego `query(1, 4)`
   y `update(3, 10)` seguido de otra `query(1, 4)`.
3. Caso borde: arreglo de un solo elemento.
4. Caso borde: `query` sobre el rango completo.
5. Análisis de complejidad temporal.

## ¿Qué es un Segment Tree?

Un Segment Tree es un árbol binario (guardado en un arreglo) que permite
responder consultas sobre rangos de un arreglo (suma, mínimo, máximo, etc.)
y actualizar elementos, ambas operaciones en `O(log N)`. El TDA que
implementa aquí soporta:

- `build(arr)`: construye el árbol en `O(N)`.
- `update(i, val)`: fija `arr[i] = val` y recalcula los ancestros en `O(log N)`.
- `query(l, r)`: retorna la suma de `arr[l..r]` en `O(log N)`.

## Estructura del repositorio

```
src/
  segment_tree.h   # Implementación del Segment Tree + logger de pasos (JSON)
  main.cpp         # Escenarios de demostración (normal + 2 casos borde)
animation/
  animate.py       # Lee los steps_*.json y anima el árbol con matplotlib
  slides.py        # Genera las slides de título y complejidad
build_video.sh      # Reproduce todo el pipeline de punta a punta
```

## Cómo funciona la animación

1. `src/main.cpp` ejecuta el Segment Tree sobre datos reales y, mientras
   corre, cada operación interna (visitar un nodo, fijar su valor, cubrir
   total/parcialmente un rango, etc.) se registra en un archivo
   `steps_*.json` mediante la clase `StepLogger`.
2. `animation/animate.py` lee ese JSON, reconstruye la topología del árbol
   (a partir de los eventos de `build`) y genera un video (matplotlib +
   ffmpeg) resaltando en cada frame exactamente el nodo/estado que el
   algoritmo real está procesando en ese instante.
3. `animation/slides.py` genera las slides de texto (título, complejidad).

## Requisitos

- `g++` con soporte C++17
- Python 3 con `matplotlib`
- `ffmpeg` (con soporte para `libx264`)

## Cómo reproducir el video

### Opción 1: en Google Colab (recomendado, sin instalar nada localmente)

Colab ya trae Linux, `g++` y Python preinstalados, así que solo falta
`ffmpeg` y `matplotlib`. En un notebook nuevo en
[colab.research.google.com](https://colab.research.google.com), ejecutar en
celdas separadas:

```python
!git clone https://github.com/AE00NN/SegmentTree-AED.git
%cd SegmentTree-AED
```

```python
!apt-get install -y ffmpeg -q > /dev/null
!pip install matplotlib -q
```

```python
!chmod +x build_video.sh
!bash build_video.sh
```

```python
from google.colab import files
files.download('video/segment_tree_video.mp4')
```

El último paso descarga el video generado directamente a la computadora.

### Opción 2: localmente (Linux o macOS)

```bash
./build_video.sh
```

Esto compila el C++, ejecuta los 3 escenarios, genera las animaciones y las
slides, normaliza resoluciones y concatena todo en
`video/segment_tree_video.mp4`.

## Complejidad

| Operación | Tiempo | Notas |
|---|---|---|
| `build` | O(N) | Visita cada uno de los ~2N-1 nodos una vez |
| `update` | O(log N) | Recorre un único camino raíz→hoja |
| `query` | O(log N) | Como mucho O(log N) nodos "totalmente cubiertos" por nivel |
| Espacio | O(N) | Arreglo de tamaño `4N` |

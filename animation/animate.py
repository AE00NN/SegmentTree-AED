"""
Anima un Segment Tree a partir de los pasos reales registrados por el
programa en C++ (steps_*.json). No se simulan valores: todo nodo, rango
y valor mostrado proviene de la ejecución real del algoritmo.

Uso:
    python animate.py steps_main.json "Build + Query(1,4) + Update(3,10)" out_main.mp4
"""

import json
import sys
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation

# --- Colores por estado (misma paleta en todo el video) ---
COLOR_IDLE = "#dfe6e9"
COLOR_VISIT = "#fdcb6e"      # nodo siendo visitado ahora
COLOR_SET = "#55efc4"        # nodo cuyo valor se acaba de fijar/recalcular
COLOR_OUT_OF_RANGE = "#b2bec3"
COLOR_LEAF_MATCH = "#74b9ff"   # rango totalmente cubierto en una query
COLOR_PARTIAL = "#a29bfe"      # rango parcialmente cubierto en una query
COLOR_EDGE = "#2d3436"
COLOR_TEXT = "#2d3436"


def load_events(path):
    with open(path) as f:
        return json.load(f)


def build_structure(events):
    """A partir de los eventos build_*, reconstruye la topología del árbol:
    node_id -> {start, end, value, depth, children}
    """
    nodes = {}
    for e in events:
        if e["op"] in ("build_visit", "build_set"):
            node = e["node"]
            nodes.setdefault(node, {"start": e["start"], "end": e["end"]})
            if e["op"] == "build_set":
                nodes[node]["value"] = e["value"]

    for node in nodes:
        nodes[node]["children"] = [c for c in (2 * node, 2 * node + 1) if c in nodes]
        nodes[node]["depth"] = int(math.floor(math.log2(node)))
    return nodes


def compute_positions(nodes, root=1):
    """Asigna coordenadas x a cada nodo: las hojas se ordenan por su 'start'
    y los nodos internos se centran sobre sus hijos."""
    leaves = sorted([n for n, d in nodes.items() if not d["children"]],
                     key=lambda n: nodes[n]["start"])
    x_of = {n: i for i, n in enumerate(leaves)}

    # Propagar x hacia arriba (post-orden simple vía memoización recursiva)
    memo = dict(x_of)

    def x_pos(n):
        if n in memo:
            return memo[n]
        children = nodes[n]["children"]
        xs = [x_pos(c) for c in children]
        memo[n] = sum(xs) / len(xs)
        return memo[n]

    for n in nodes:
        x_pos(n)

    max_depth = max(d["depth"] for d in nodes.values())
    positions = {}
    for n, d in nodes.items():
        positions[n] = (memo[n], max_depth - d["depth"])  # y: root arriba
    return positions


def label_for(node_id, data, value_override=None):
    # Solo mostramos el valor una vez que fue efectivamente calculado en esta
    # animación (value_override), nunca el valor final "adelantado".
    v = value_override if value_override is not None else "?"
    return f"{v}\n[{data['start']},{data['end']}]"


def render_scene(events, title, out_path, fps=2, hold_frames=3, dpi=140):
    nodes = build_structure(events)
    positions = compute_positions(nodes)

    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    x_span = max(xs) - min(xs) if xs else 1
    fig_w = max(8, x_span * 1.3 + 2)
    fig_h = max(5, (max(ys) + 1) * 1.6 + 1.5)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

    # Estado que evoluciona a lo largo de la animación.
    # 'computed' es permanente (una vez que build_set fija el valor, no se
    # pierde); 'highlight' es transitorio (el color de la operación actual).
    current_value = {n: None for n in nodes}  # se llena en build_set
    computed = {n: False for n in nodes}
    highlight = {n: None for n in nodes}
    caption = {"text": title}

    # Aplanar eventos a "frames": cada evento real se sostiene 'hold_frames'
    frames = []
    for e in events:
        frames.extend([e] * hold_frames)

    def draw(ax):
        ax.clear()
        ax.set_xlim(min(xs) - 1, max(xs) + 1)
        ax.set_ylim(-0.8, max(ys) + 1.2)
        ax.axis("off")
        ax.set_title(caption["text"], fontsize=13, color=COLOR_TEXT, wrap=True)

        # Aristas
        for n, data in nodes.items():
            x1, y1 = positions[n]
            for c in data["children"]:
                x2, y2 = positions[c]
                ax.plot([x1, x2], [y1, y2], color=COLOR_EDGE, linewidth=1.2, zorder=1)

        # Nodos
        for n, data in nodes.items():
            x, y = positions[n]
            if highlight[n] is not None:
                color = highlight[n]
            elif computed[n]:
                color = COLOR_SET
            else:
                color = COLOR_IDLE
            circle = mpatches.Circle((x, y), 0.38, facecolor=color,
                                      edgecolor=COLOR_EDGE, linewidth=1.2, zorder=2)
            ax.add_patch(circle)
            label = label_for(n, data, current_value[n])
            ax.text(x, y, label, ha="center", va="center", fontsize=8,
                    color=COLOR_TEXT, zorder=3)

    def update(frame_idx):
        e = frames[frame_idx]
        op = e["op"]

        if op == "header":
            caption["text"] = f"{title}\n{e['name']}({', '.join(f'{k}={v}' for k, v in e['params'].items())})"
            draw(ax)
            return

        node = e.get("node")
        if node is None:
            draw(ax)
            return

        # El resaltado es siempre transitorio: solo el nodo de este evento
        # se marca; el resto vuelve a su estado permanente (computed o no).
        for n in highlight:
            highlight[n] = None

        if op == "build_visit":
            highlight[node] = COLOR_VISIT
        elif op == "build_set":
            computed[node] = True
            current_value[node] = e["value"]
            highlight[node] = COLOR_SET
        elif op == "update_visit":
            highlight[node] = COLOR_VISIT
        elif op == "update_set":
            current_value[node] = e["value"]
            highlight[node] = COLOR_SET
        elif op == "query_leaf":
            highlight[node] = COLOR_LEAF_MATCH
        elif op == "query_partial":
            highlight[node] = COLOR_PARTIAL
        elif op == "query_out_of_range":
            highlight[node] = COLOR_OUT_OF_RANGE

        draw(ax)

    anim = FuncAnimation(fig, update, frames=len(frames), interval=1000 / fps)
    anim.save(out_path, writer="ffmpeg", fps=fps, dpi=dpi)
    plt.close(fig)
    print(f"Guardado: {out_path} ({len(frames)} frames, {len(events)} eventos)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python animate.py <steps.json> <titulo> <salida.mp4> [fps] [hold_frames]")
        sys.exit(1)
    events = load_events(sys.argv[1])
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    hold_frames = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    render_scene(events, sys.argv[2], sys.argv[3], fps=fps, hold_frames=hold_frames)

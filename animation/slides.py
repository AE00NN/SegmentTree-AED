"""
Genera slides de texto simples (fondo + texto centrado, con viñetas
opcionales) para las partes no-animadas del video: título, análisis de
complejidad y créditos.
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

BG = "#2d3436"
FG = "#ffffff"
ACCENT = "#55efc4"


def make_slide(lines, out_path, duration_sec=5, fps=2, big_first_line=False):
    frames = int(duration_sec * fps)
    fig, ax = plt.subplots(figsize=(11.2, 6.3), dpi=140)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    def draw(_):
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(BG)

        n = len(lines)
        start_y = 0.5 + (n - 1) * 0.07
        for i, line in enumerate(lines):
            y = start_y - i * 0.14
            if i == 0 and big_first_line:
                ax.text(0.5, y, line, ha="center", va="center",
                        fontsize=22, color=ACCENT, fontweight="bold", wrap=True)
            else:
                ax.text(0.5, y, line, ha="center", va="center",
                        fontsize=14, color=FG, wrap=True)

    anim = FuncAnimation(fig, draw, frames=frames, interval=1000 / fps)
    anim.save(out_path, writer="ffmpeg", fps=fps, dpi=140,
              savefig_kwargs={"facecolor": BG})
    plt.close(fig)
    print(f"Guardado: {out_path} ({duration_sec}s)")


if __name__ == "__main__":
    # Modo simple por CLI: python slides.py out.mp4 duracion "linea1" "linea2" ...
    out = sys.argv[1]
    dur = float(sys.argv[2])
    lines = sys.argv[3:]
    make_slide(lines, out, duration_sec=dur, big_first_line=True)

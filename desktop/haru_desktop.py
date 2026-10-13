#!/usr/bin/env python3
"""Haru Urara desktop companion for Windows."""

from __future__ import annotations

import math
import random
import sys
import time
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageTk

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "assets" / "sprites" / "haru-urara-spritesheet.png"
CELL_WIDTH, CELL_HEIGHT = 192, 208
TRANSPARENT = "#010203"
ROWS = {
    "idle": (0, 6, 180), "running-right": (1, 8, 85),
    "running-left": (2, 8, 85), "waving": (3, 4, 130),
    "jumping": (4, 5, 115), "failed": (5, 8, 170),
    "waiting": (6, 6, 190), "running": (7, 6, 110),
    "review": (8, 6, 180), "look-a": (9, 8, 120),
    "look-b": (10, 8, 120),
}


def direction_index(dx: float, dy: float) -> int:
    """Closest clockwise 22.5-degree direction, where zero points up."""
    if dx == 0 and dy == 0:
        return 0
    degrees = (math.degrees(math.atan2(dx, -dy)) + 360) % 360
    return int((degrees + 11.25) // 22.5) % 16


@dataclass
class Motion:
    state: str = "idle"
    frame: int = 0
    loops_left: int | None = None
    next_frame_at: float = 0.0


class HaruDesktop:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Haru Urara")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSPARENT)
        if sys.platform == "win32":
            self.root.wm_attributes("-transparentcolor", TRANSPARENT)
        self.canvas = tk.Canvas(self.root, width=CELL_WIDTH, height=CELL_HEIGHT,
                                bg=TRANSPARENT, highlightthickness=0, borderwidth=0)
        self.canvas.pack()
        self.sprite = self.canvas.create_image(CELL_WIDTH // 2, CELL_HEIGHT // 2)
        self.frames = self._load_frames()
        self.photos: dict[tuple[str, int], ImageTk.PhotoImage] = {}
        self.motion = Motion(next_frame_at=time.monotonic())
        self.paused = False
        self.auto_walk = True
        self.walk_target: int | None = None
        self.next_walk_at = time.monotonic() + random.uniform(5, 9)
        self.drag_origin: tuple[int, int, int, int] | None = None
        self.drag_moved = False
        x = self.root.winfo_screenwidth() - CELL_WIDTH - 40
        y = self.root.winfo_screenheight() - CELL_HEIGHT - 90
        self.root.geometry(f"+{max(0, x)}+{max(0, y)}")
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._end_drag)
        self.canvas.bind("<Double-Button-1>", lambda _event: self.play("jumping", 1))
        self.canvas.bind("<Button-3>", self._show_menu)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())
        self.menu = self._build_menu()
        self.root.after(16, self._tick)

    def _load_frames(self) -> dict[str, list[Image.Image]]:
        if not ATLAS.exists():
            raise FileNotFoundError(f"No se encontró el atlas: {ATLAS}")
        result = {}
        with Image.open(ATLAS) as source:
            atlas = source.convert("RGBA")
            for state, (row, count, _duration) in ROWS.items():
                result[state] = [atlas.crop((col * CELL_WIDTH, row * CELL_HEIGHT,
                                             (col + 1) * CELL_WIDTH, (row + 1) * CELL_HEIGHT))
                                 for col in range(count)]
        return result

    def _build_menu(self) -> tk.Menu:
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="Saludar", command=lambda: self.play("waving", 2))
        menu.add_command(label="Saltar", command=lambda: self.play("jumping", 1))
        menu.add_command(label="Revisar", command=lambda: self.play("review", 1))
        menu.add_separator()
        menu.add_command(label="Pausar", command=self._toggle_pause)
        menu.add_command(label="Desactivar caminata", command=self._toggle_walk)
        menu.add_separator()
        menu.add_command(label="Cerrar Haru", command=self.root.destroy)
        return menu

    def play(self, state: str, loops: int | None = None) -> None:
        self.motion = Motion(state, 0, loops, time.monotonic())

    def _photo(self, state: str, frame: int) -> ImageTk.PhotoImage:
        key = (state, frame)
        if key not in self.photos:
            self.photos[key] = ImageTk.PhotoImage(self.frames[state][frame])
        return self.photos[key]

    def _tick(self) -> None:
        now = time.monotonic()
        if not self.paused:
            self._update_walk(now)
            if now >= self.motion.next_frame_at:
                self._advance_animation(now)
            self._render()
        self.root.after(16, self._tick)

    def _advance_animation(self, now: float) -> None:
        state = self.motion.state
        self.motion.frame += 1
        if self.motion.frame >= len(self.frames[state]):
            self.motion.frame = 0
            if self.motion.loops_left is not None:
                self.motion.loops_left -= 1
                if self.motion.loops_left <= 0:
                    self.motion = Motion(next_frame_at=now)
                    return
        self.motion.next_frame_at = now + ROWS[state][2] / 1000

    def _render(self) -> None:
        if self.motion.state == "idle" and not self.drag_origin:
            px, py = self.root.winfo_pointerxy()
            dx = px - (self.root.winfo_x() + CELL_WIDTH / 2)
            dy = py - (self.root.winfo_y() + CELL_HEIGHT / 2)
            index = direction_index(dx, dy)
            state, frame = ("look-a", index) if index < 8 else ("look-b", index - 8)
        else:
            state, frame = self.motion.state, self.motion.frame
        self.canvas.itemconfigure(self.sprite, image=self._photo(state, frame))

    def _update_walk(self, now: float) -> None:
        if self.drag_origin or self.motion.state not in {"idle", "running-left", "running-right"}:
            return
        x = self.root.winfo_x()
        if self.walk_target is None and self.auto_walk and now >= self.next_walk_at:
            limit = max(20, self.root.winfo_screenwidth() - CELL_WIDTH - 20)
            self.walk_target = random.randint(20, limit)
        if self.walk_target is None:
            if self.motion.state.startswith("running-"):
                self.play("idle")
            return
        delta = self.walk_target - x
        if abs(delta) <= 3:
            self.walk_target = None
            self.next_walk_at = now + random.uniform(6, 12)
            self.play("idle")
            return
        step = 2 if delta > 0 else -2
        desired = "running-right" if step > 0 else "running-left"
        if self.motion.state != desired:
            self.play(desired)
        self.root.geometry(f"+{x + step}+{self.root.winfo_y()}")

    def _start_drag(self, event: tk.Event) -> None:
        self.drag_origin = (event.x_root, event.y_root, self.root.winfo_x(), self.root.winfo_y())
        self.drag_moved = False
        self.walk_target = None

    def _drag(self, event: tk.Event) -> None:
        if self.drag_origin:
            px, py, wx, wy = self.drag_origin
            self.drag_moved = self.drag_moved or abs(event.x_root - px) + abs(event.y_root - py) > 4
            self.root.geometry(f"+{wx + event.x_root - px}+{wy + event.y_root - py}")

    def _end_drag(self, _event: tk.Event) -> None:
        if self.drag_origin:
            self.drag_origin = None
            if self.drag_moved:
                self.play("waving", 1)

    def _show_menu(self, event: tk.Event) -> None:
        self.menu.tk_popup(event.x_root, event.y_root)

    def _toggle_pause(self) -> None:
        self.paused = not self.paused
        self.menu.entryconfigure(4, label="Reanudar" if self.paused else "Pausar")

    def _toggle_walk(self) -> None:
        self.auto_walk = not self.auto_walk
        self.walk_target = None
        self.menu.entryconfigure(5, label="Desactivar caminata" if self.auto_walk else "Activar caminata")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    HaruDesktop().run()

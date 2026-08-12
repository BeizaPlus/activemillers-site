"""Super simple video trimmer GUI. Pick a video, drag sliders to set start/end,
preview thumbnails and playback, then export the trimmed clip with ffmpeg.

Run: python tools/video_trimmer.py [path-to-video]
Optional argument pre-loads that specific file instead of the default quick source
(also reachable via the /fastcut slash command).
"""
import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

FFMPEG = r"C:\Users\steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
FFPROBE = FFMPEG.replace("ffmpeg.exe", "ffprobe.exe")
FFPLAY = FFMPEG.replace("ffmpeg.exe", "ffplay.exe")

DEFAULT_INPUT_DIR = r"C:\Users\steve\AppData\Local\Comfy-Desktop\ComfyUI-Shared\output\video\LTX_2.3_i2v"
DEFAULT_OUTPUT_DIR = r"C:\Users\steve\Personal Assistant\Beiza\activemillers-site\videos"
# Recently-used raw renders, for one-click loading instead of browsing every time.
# Add new entries here as new sources come up.
QUICK_SOURCES = {
    "Figure 7 source (onepass-4stage)": "septic-knee-onepass-4stage_00001_.mp4",
    "Batch A - The Slow Build (0-14s)": "septic-knee-30s-batchA-0to14s_00001_.mp4",
    "Batch B - The Rapid Clouding (14-30s)": "septic-knee-30s-batchB-14to30s_00001_.mp4",
    "Erythema Batch A (0-15s)": "erythema-30s-batchA-0to15s_00001_.mp4",
}

CLI_PRELOAD_PATH = sys.argv[1] if len(sys.argv) > 1 else None
THUMB_W, THUMB_H = 280, 158


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)


def get_duration(path):
    r = run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def extract_frame(path, t, out_png):
    run([FFMPEG, "-y", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-vf",
         f"scale={THUMB_W}:-1", out_png])


class Trimmer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Trimmer")
        self.geometry("700x760")
        self.minsize(460, 420)
        self.configure(bg="#0a0a09")
        self.video_path = None
        self.duration = 0.0
        self.thumb_start_img = None
        self.thumb_end_img = None
        self._thumb_job = None

        self.fg = "#e8e8e8"
        self.bg = "#0a0a09"
        self.entry_bg = "#1a1a19"
        self.accent = "#e60021"

        # --- scrollable container so every control stays reachable on any screen size ---
        outer = tk.Frame(self, bg=self.bg)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=self.bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        body = tk.Frame(canvas, bg=self.bg)
        body_id = canvas.create_window((0, 0), window=body, anchor="nw")

        def on_body_configure(_e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(e):
            canvas.itemconfig(body_id, width=e.width)

        body.bind("<Configure>", on_body_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        self._build(body)

        if CLI_PRELOAD_PATH and os.path.exists(CLI_PRELOAD_PATH):
            self.video_path = CLI_PRELOAD_PATH
            self.path_label.config(text=f"Loaded: {CLI_PRELOAD_PATH}")
            threading.Thread(target=self._load_duration, daemon=True).start()
        else:
            first_label, first_file = next(iter(QUICK_SOURCES.items()))
            first_path = os.path.join(DEFAULT_INPUT_DIR, first_file)
            if os.path.exists(first_path):
                self.video_path = first_path
                self.path_label.config(text=f"{first_label}: {first_path}")
                threading.Thread(target=self._load_duration, daemon=True).start()

    def _label(self, parent, text, **kw):
        return tk.Label(parent, text=text, fg=self.fg, bg=self.bg, font=("Segoe UI", 10), **kw)

    def _build(self, root):
        fg, bg, entry_bg, accent = self.fg, self.bg, self.entry_bg, self.accent

        top = tk.Frame(root, bg=bg, pady=10)
        top.pack(fill="x", padx=12)
        tk.Button(top, text="Browse video...", command=self.browse, bg=entry_bg, fg=fg,
                  activebackground=accent, relief="flat", padx=10, pady=4).pack(side="left")

        quick_row = tk.Frame(root, bg=bg)
        quick_row.pack(fill="x", padx=12, pady=(0, 6))
        self._label(quick_row, "Quick load:").pack(side="left")
        for label, filename in QUICK_SOURCES.items():
            tk.Button(quick_row, text=label, command=lambda f=filename, l=label: self.load_quick(f, l),
                      bg=entry_bg, fg=fg, activebackground=accent, relief="flat", padx=8, pady=3,
                      font=("Segoe UI", 9)).pack(side="left", padx=4)

        self.path_label = self._label(root, "No file selected", wraplength=640, justify="left")
        self.path_label.pack(anchor="w", padx=12)

        self.duration_label = self._label(root, "Duration: -")
        self.duration_label.pack(anchor="w", padx=12, pady=(4, 10))

        thumbs = tk.Frame(root, bg=bg)
        thumbs.pack(padx=12)

        start_col = tk.Frame(thumbs, bg=bg)
        start_col.grid(row=0, column=0, padx=8)
        self._label(start_col, "Start frame").pack()
        self.start_canvas = tk.Label(start_col, bg="#141414", width=THUMB_W, height=THUMB_H)
        self.start_canvas.pack()

        end_col = tk.Frame(thumbs, bg=bg)
        end_col.grid(row=0, column=1, padx=8)
        self._label(end_col, "End frame").pack()
        self.end_canvas = tk.Label(end_col, bg="#141414", width=THUMB_W, height=THUMB_H)
        self.end_canvas.pack()

        controls = tk.Frame(root, bg=bg, pady=12)
        controls.pack(fill="x", padx=12)

        # Start slider + entry, kept in sync
        row1 = tk.Frame(controls, bg=bg)
        row1.pack(fill="x", pady=4)
        self._label(row1, "Start (s):", ).pack(side="left")
        self.start_var = tk.DoubleVar(value=0)
        self.start_entry_var = tk.StringVar(value="0.00")
        tk.Entry(row1, textvariable=self.start_entry_var, width=8, bg=entry_bg, fg=fg,
                 insertbackground=fg).pack(side="left", padx=6)
        tk.Button(row1, text="Preview frame", command=lambda: self.update_thumb("start"),
                  bg=entry_bg, fg=fg, relief="flat", padx=8).pack(side="left", padx=6)
        self.start_slider = tk.Scale(controls, from_=0, to=1, resolution=0.05, orient="horizontal",
                                      variable=self.start_var, command=self._on_start_slide,
                                      bg=bg, fg=fg, troughcolor=entry_bg, highlightthickness=0,
                                      activebackground=accent, showvalue=False)
        self.start_slider.pack(fill="x", pady=(0, 8))

        # End slider + entry
        row2 = tk.Frame(controls, bg=bg)
        row2.pack(fill="x", pady=4)
        self._label(row2, "End (s):  ").pack(side="left")
        self.end_var = tk.DoubleVar(value=0)
        self.end_entry_var = tk.StringVar(value="0.00")
        tk.Entry(row2, textvariable=self.end_entry_var, width=8, bg=entry_bg, fg=fg,
                 insertbackground=fg).pack(side="left", padx=6)
        tk.Button(row2, text="Preview frame", command=lambda: self.update_thumb("end"),
                  bg=entry_bg, fg=fg, relief="flat", padx=8).pack(side="left", padx=6)
        self.end_slider = tk.Scale(controls, from_=0, to=1, resolution=0.05, orient="horizontal",
                                    variable=self.end_var, command=self._on_end_slide,
                                    bg=bg, fg=fg, troughcolor=entry_bg, highlightthickness=0,
                                    activebackground=accent, showvalue=False)
        self.end_slider.pack(fill="x", pady=(0, 8))

        self.start_entry_var.trace_add("write", lambda *_: self._on_start_entry())
        self.end_entry_var.trace_add("write", lambda *_: self._on_end_entry())

        row3 = tk.Frame(controls, bg=bg)
        row3.pack(fill="x", pady=8)
        tk.Button(row3, text="Play trimmed range (ffplay)", command=self.play_range,
                  bg=entry_bg, fg=fg, relief="flat", padx=10, pady=4).pack(side="left")

        row4 = tk.Frame(controls, bg=bg)
        row4.pack(fill="x", pady=4)
        self._label(row4, "Output filename:").pack(side="left")
        self.output_name_var = tk.StringVar(value="trimmed-clip.mp4")
        tk.Entry(row4, textvariable=self.output_name_var, width=32, bg=entry_bg, fg=fg,
                 insertbackground=fg).pack(side="left", padx=6, fill="x", expand=True)

        row5 = tk.Frame(controls, bg=bg)
        row5.pack(fill="x", pady=4)
        self._label(row5, "Output folder:").pack(side="left")
        self.output_dir_var = tk.StringVar(value=DEFAULT_OUTPUT_DIR)
        tk.Entry(row5, textvariable=self.output_dir_var, width=45, bg=entry_bg, fg=fg,
                 insertbackground=fg).pack(side="left", padx=6, fill="x", expand=True)
        tk.Button(row5, text="...", command=self.browse_output_dir, bg=entry_bg, fg=fg, relief="flat").pack(side="left")
        tk.Button(row5, text="Open folder", command=self.open_output_dir, bg=entry_bg, fg=fg, relief="flat").pack(side="left", padx=(6, 0))

        self.strip_audio_var = tk.BooleanVar(value=True)
        tk.Checkbutton(controls, text="Strip audio (site videos are always muted)", variable=self.strip_audio_var,
                        bg=bg, fg=fg, selectcolor=bg, activebackground=bg, activeforeground=fg).pack(anchor="w", pady=6)

        self.trim_btn = tk.Button(controls, text="Trim & Save", command=self.trim_and_save,
                                   bg=accent, fg="white", relief="flat", padx=14, pady=8, font=("Segoe UI", 10, "bold"))
        self.trim_btn.pack(pady=10)

        self.status_label = self._label(root, "", wraplength=660, justify="left")
        self.status_label.pack(anchor="w", padx=12, pady=(0, 16))

    # --- slider/entry sync ---
    def _on_start_slide(self, val):
        self.start_entry_var.set(f"{float(val):.2f}")
        self._debounced_thumb("start")

    def _on_end_slide(self, val):
        self.end_entry_var.set(f"{float(val):.2f}")
        self._debounced_thumb("end")

    def _on_start_entry(self):
        try:
            v = float(self.start_entry_var.get())
            self.start_var.set(v)
        except ValueError:
            pass

    def _on_end_entry(self):
        try:
            v = float(self.end_entry_var.get())
            self.end_var.set(v)
        except ValueError:
            pass

    def _debounced_thumb(self, which):
        if self._thumb_job:
            self.after_cancel(self._thumb_job)
        self._thumb_job = self.after(250, lambda: self.update_thumb(which))

    # --- loading ---
    def load_quick(self, filename, label):
        path = os.path.join(DEFAULT_INPUT_DIR, filename)
        if not os.path.exists(path):
            messagebox.showwarning("Not found", f"Couldn't find:\n{path}")
            return
        self.video_path = path
        self.path_label.config(text=f"{label}: {path}")
        self.status_label.config(text="Reading duration...")
        threading.Thread(target=self._load_duration, daemon=True).start()

    def browse(self):
        path = filedialog.askopenfilename(
            title="Choose a video",
            initialdir=DEFAULT_INPUT_DIR if os.path.isdir(DEFAULT_INPUT_DIR) else os.path.expanduser("~"),
            filetypes=[("Video files", "*.mp4 *.mov *.webm *.mkv"), ("All files", "*.*")],
        )
        if not path:
            return
        self.video_path = path
        self.path_label.config(text=path)
        self.status_label.config(text="Reading duration...")
        threading.Thread(target=self._load_duration, daemon=True).start()

    def _load_duration(self):
        dur = get_duration(self.video_path)
        self.duration = dur
        self.duration_label.config(text=f"Duration: {dur:.2f}s")
        self.start_slider.config(to=max(dur, 0.1))
        self.end_slider.config(to=max(dur, 0.1))
        self.start_var.set(0)
        self.start_entry_var.set("0.00")
        self.end_var.set(dur)
        self.end_entry_var.set(f"{dur:.2f}")
        base = os.path.splitext(os.path.basename(self.video_path))[0]
        self.output_name_var.set(f"{base}-trim.mp4")
        self.status_label.config(text="Ready.")
        self.update_thumb("start")
        self.update_thumb("end")

    def _safe_time(self, entry_var):
        try:
            t = float(entry_var.get())
        except ValueError:
            t = 0.0
        return max(0.0, min(t, max(self.duration - 0.05, 0)))

    def update_thumb(self, which):
        if not self.video_path:
            return
        t = self._safe_time(self.start_entry_var if which == "start" else self.end_entry_var)
        out_png = os.path.join(os.path.dirname(__file__), f"_trimmer_thumb_{which}.png")
        threading.Thread(target=self._extract_and_show, args=(t, out_png, which), daemon=True).start()

    def _extract_and_show(self, t, out_png, which):
        extract_frame(self.video_path, t, out_png)
        if not os.path.exists(out_png):
            return
        img = Image.open(out_png)
        img.thumbnail((THUMB_W, THUMB_H))
        tkimg = ImageTk.PhotoImage(img)
        if which == "start":
            self.thumb_start_img = tkimg
            self.start_canvas.config(image=tkimg)
        else:
            self.thumb_end_img = tkimg
            self.end_canvas.config(image=tkimg)

    def play_range(self):
        if not self.video_path:
            messagebox.showwarning("No video", "Choose a video first.")
            return
        start = self._safe_time(self.start_entry_var)
        end = self._safe_time(self.end_entry_var)
        length = max(end - start, 0.1)
        threading.Thread(target=lambda: run([FFPLAY, "-autoexit", "-window_title", "Trim preview",
                                              "-ss", str(start), "-t", str(length), self.video_path]), daemon=True).start()

    def browse_output_dir(self):
        d = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if d:
            self.output_dir_var.set(d)

    def open_output_dir(self):
        d = self.output_dir_var.get().strip()
        if not d:
            return
        os.makedirs(d, exist_ok=True)
        subprocess.Popen(["explorer.exe", os.path.normpath(d)])

    def trim_and_save(self):
        if not self.video_path:
            messagebox.showwarning("No video", "Choose a video first.")
            return
        start = self._safe_time(self.start_entry_var)
        end = self._safe_time(self.end_entry_var)
        if end <= start:
            messagebox.showwarning("Bad range", "End must be after start.")
            return
        out_dir = self.output_dir_var.get().strip()
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, self.output_name_var.get().strip() or "trimmed-clip.mp4")
        self.trim_btn.config(state="disabled")
        self.status_label.config(text=f"Trimming {start:.2f}s -> {end:.2f}s ...")
        threading.Thread(target=self._do_trim, args=(start, end, out_path), daemon=True).start()

    def _do_trim(self, start, end, out_path):
        length = end - start
        cmd = [FFMPEG, "-y", "-v", "error", "-i", self.video_path, "-ss", str(start), "-t", str(length),
               "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-movflags", "+faststart"]
        if self.strip_audio_var.get():
            cmd += ["-an"]
        cmd += [out_path]
        r = run(cmd)
        if r.returncode == 0 and os.path.exists(out_path):
            self.status_label.config(text=f"Saved: {out_path}")
        else:
            self.status_label.config(text=f"ffmpeg failed: {r.stderr[-400:]}")
        self.trim_btn.config(state="normal")


if __name__ == "__main__":
    app = Trimmer()
    app.mainloop()

from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, UnidentifiedImageError


ICON_SIZES = (16, 24, 32, 48, 64, 128, 256)


def convert_png_to_ico(input_path: Path, output_path: Path, sizes: list[int]) -> None:
    if not input_path:
        raise ValueError("Select a PNG file first.")
    if input_path.suffix.lower() != ".png":
        raise ValueError("Input file must be a .png file.")
    if not input_path.is_file():
        raise ValueError("Input PNG file does not exist.")
    if not output_path:
        raise ValueError("Choose an output .ico file.")
    if output_path.suffix.lower() != ".ico":
        raise ValueError("Output file must use the .ico extension.")
    if not output_path.parent.exists():
        raise ValueError("Output folder does not exist.")
    if not sizes:
        raise ValueError("Select at least one icon size.")

    ico_sizes = [(size, size) for size in sizes]

    try:
        with Image.open(input_path) as image:
            if image.format != "PNG":
                raise ValueError("Input file is not a valid PNG image.")

            image.convert("RGBA").save(output_path, format="ICO", sizes=ico_sizes)
    except UnidentifiedImageError as exc:
        raise ValueError("Input file is not a readable image.") from exc


class IcoGeneratorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PNG to ICO Generator")
        self.minsize(620, 390)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.image_info = tk.StringVar(value="No PNG selected")
        self.status = tk.StringVar(value="Ready")
        self.size_vars = {size: tk.BooleanVar(value=True) for size in ICON_SIZES}

        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        main = ttk.Frame(self, padding=18)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)

        title = ttk.Label(main, text="PNG to ICO Generator", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, sticky="w")

        input_group = ttk.LabelFrame(main, text="Input PNG", padding=12)
        input_group.grid(row=1, column=0, sticky="ew", pady=(16, 10))
        input_group.columnconfigure(0, weight=1)

        ttk.Entry(input_group, textvariable=self.input_path).grid(row=0, column=0, sticky="ew")
        ttk.Button(input_group, text="Browse...", command=self.choose_input).grid(
            row=0, column=1, padx=(8, 0)
        )
        ttk.Label(input_group, textvariable=self.image_info).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

        output_group = ttk.LabelFrame(main, text="Output ICO", padding=12)
        output_group.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        output_group.columnconfigure(0, weight=1)

        ttk.Entry(output_group, textvariable=self.output_path).grid(row=0, column=0, sticky="ew")
        ttk.Button(output_group, text="Save As...", command=self.choose_output).grid(
            row=0, column=1, padx=(8, 0)
        )

        size_group = ttk.LabelFrame(main, text="Icon Sizes", padding=12)
        size_group.grid(row=3, column=0, sticky="ew", pady=(0, 14))

        for index, size in enumerate(ICON_SIZES):
            checkbox = ttk.Checkbutton(
                size_group,
                text=f"{size}x{size}",
                variable=self.size_vars[size],
            )
            checkbox.grid(row=0, column=index, padx=(0, 12), sticky="w")

        actions = ttk.Frame(main)
        actions.grid(row=4, column=0, sticky="ew")
        actions.columnconfigure(0, weight=1)

        ttk.Label(actions, textvariable=self.status).grid(row=0, column=0, sticky="w")
        ttk.Button(actions, text="Convert", command=self.convert).grid(row=0, column=1)

    def choose_input(self) -> None:
        selected = filedialog.askopenfilename(
            title="Select PNG Image",
            filetypes=(("PNG images", "*.png"), ("All files", "*.*")),
        )
        if not selected:
            return

        input_path = Path(selected)
        self.input_path.set(str(input_path))
        self.output_path.set(str(input_path.with_suffix(".ico")))

        self._update_image_info(input_path)

    def choose_output(self) -> None:
        initial_file = "icon.ico"
        initial_dir = None

        if self.input_path.get():
            input_path = Path(self.input_path.get())
            initial_file = input_path.with_suffix(".ico").name
            initial_dir = str(input_path.parent)

        selected = filedialog.asksaveasfilename(
            title="Save ICO File",
            defaultextension=".ico",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=(("ICO files", "*.ico"), ("All files", "*.*")),
        )
        if selected:
            self.output_path.set(selected)

    def convert(self) -> None:
        selected_sizes = [size for size, selected in self.size_vars.items() if selected.get()]

        try:
            convert_png_to_ico(
                Path(self.input_path.get()),
                Path(self.output_path.get()),
                selected_sizes,
            )
        except ValueError as exc:
            self.status.set(str(exc))
            messagebox.showerror("Conversion Failed", str(exc))
            return
        except OSError as exc:
            self.status.set("Could not write ICO file.")
            messagebox.showerror("Conversion Failed", f"Could not write ICO file:\n{exc}")
            return

        self.status.set(f"Created {self.output_path.get()}")
        messagebox.showinfo("Conversion Complete", "ICO file created successfully.")

    def _update_image_info(self, input_path: Path) -> None:
        try:
            with Image.open(input_path) as image:
                if image.format != "PNG":
                    self.image_info.set("Selected file is not a valid PNG image")
                    return

                transparency = "with transparency" if image.mode in ("RGBA", "LA", "P") else "opaque"
                self.image_info.set(f"{image.width}x{image.height}px, {image.mode}, {transparency}")
        except (OSError, UnidentifiedImageError):
            self.image_info.set("Could not read selected image")


if __name__ == "__main__":
    app = IcoGeneratorApp()
    app.mainloop()

import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from watcher import FolderWatcher
from organizer_core import EXTENSION_MAP, organize_directory

# Force Clean Light Theme Only
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Category Descriptions and File Extensions
CATEGORY_INFO = {
    "Videos": {
        "title": "Videos & Clips",
        "desc": "Video recordings, movies, and animated media.",
        "exts": ".mp4, .mkv, .mov, .avi, .flv, .webm"
    },
    "Images": {
        "title": "Images & Photos",
        "desc": "Raster photos, vector graphics, and camera HEIC files.",
        "exts": ".jpg, .jpeg, .png, .gif, .webp, .heic, .svg"
    },
    "Audio": {
        "title": "Audio & Music",
        "desc": "Sound tracks, voice recordings, and music files.",
        "exts": ".mp3, .wav, .flac, .aac, .m4a, .ogg"
    },
    "Documents": {
        "title": "Documents & Text",
        "desc": "PDFs, spreadsheets, word documents, and databases.",
        "exts": ".pdf, .docx, .xlsx, .txt, .csv, .vcf, .mwb"
    },
    "Archives": {
        "title": "Archives & Compressed",
        "desc": "Zip packages, tarballs, and compressed bundles.",
        "exts": ".zip, .tar.gz, .tar, .gz, .7z, .rar"
    },
    "Executables_and_Apps": {
        "title": "Apps & Software",
        "desc": "Executable packages, AppImages, and software installers.",
        "exts": ".appimage, .exe, .msi, .deb, .rpm, .gguf"
    }
}

def open_native_folder_picker(initial_dir):
    """Detects OS and launches native folder picker (Zenity for Linux, WinExplorer for Windows)."""
    if sys.platform.startswith("linux"):
        try:
            cmd = [
                "zenity", 
                "--file-selection", 
                "--directory", 
                f"--filename={initial_dir}/",
                "--title=Select Target Folder"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except FileNotFoundError:
            return filedialog.askdirectory(initialdir=initial_dir)
    else:
        # Windows / macOS Native File Explorer Dialog
        chosen = filedialog.askdirectory(initialdir=initial_dir)
        return chosen if chosen else None


class AnimatedRectangleTick(ctk.CTkButton):
    """Custom Rectangular Checkbox with spring scale animation."""
    def __init__(self, parent, is_checked=True, command=None, **kwargs):
        self.is_checked = is_checked
        self.custom_command = command
        
        super().__init__(
            parent,
            text="✔" if self.is_checked else "",
            width=24,
            height=24,
            corner_radius=6,
            border_width=2,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.animate_toggle,
            **kwargs
        )
        self.update_appearance()

    def update_appearance(self):
        if self.is_checked:
            self.configure(
                text="✔",
                fg_color="#26A269",        # Vibrant Green
                border_color="#26A269",
                hover_color="#1F8354",
                text_color="#FFFFFF"
            )
        else:
            self.configure(
                text="",
                fg_color="#FFFFFF",        # Empty White Box
                border_color="#B0B0B0",    # Clean Grey Border
                hover_color="#EAEAEA",
                text_color="#FFFFFF"
            )

    def animate_toggle(self):
        """Micro scale animation when toggling the rectangle."""
        self.is_checked = not self.is_checked
        
        # Step 1: Shrink box
        self.configure(width=20, height=20)
        
        # Step 2: Swap state & spring outward
        def step_two():
            self.update_appearance()
            self.configure(width=26, height=26)
            
            # Step 3: Settle at normal size
            def step_three():
                self.configure(width=24, height=24)
                if self.custom_command:
                    self.custom_command(self.is_checked)

            self.after(35, step_three)

        self.after(35, step_two)


class CategoryItemRow(ctk.CTkFrame):
    """Spacious Category Card containing rectangle tick, title, and far-right info circle."""
    def __init__(self, parent, key, info_callback, **kwargs):
        super().__init__(
            parent, 
            corner_radius=8, 
            border_width=1, 
            border_color="#E1E1E0", 
            fg_color="#FAFAFA", 
            height=48, 
            **kwargs
        )
        self.grid_propagate(False)

        self.key = key
        self.is_active = True
        self.info_data = CATEGORY_INFO.get(key, {
            "title": key, "desc": "Categorized files", "exts": "Supported extensions"
        })

        # 1. Animated Rectangular Tick
        self.tick = AnimatedRectangleTick(
            self, 
            is_checked=True, 
            command=self.on_tick_toggle
        )
        self.tick.pack(side="left", padx=(14, 10), pady=10)

        # 2. Category Title
        self.label = ctk.CTkLabel(
            self, 
            text=self.info_data["title"], 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2E2E2E"
        )
        self.label.pack(side="left", padx=4, pady=10)

        # 3. Info Circle Button (ⓘ)
        self.info_btn = ctk.CTkButton(
            self,
            text="ⓘ",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#E8E8E7",
            text_color="#6E6E73",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: info_callback(self.info_data)
        )
        self.info_btn.pack(side="right", padx=(0, 14), pady=10)

    def on_tick_toggle(self, checked):
        self.is_active = checked


class CrossPlatformFileOrganizer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Standard Half-Screen Default Sizing ---
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        app_w = max(700, int(screen_w * 0.50))
        app_h = max(550, int(screen_h * 0.72))
        pos_x = int((screen_w - app_w) / 2)
        pos_y = int((screen_h - app_h) / 2)

        self.title("File Organizer")
        self.geometry(f"{app_w}x{app_h}+{pos_x}+{pos_y}")
        self.minsize(620, 500)
        self.resizable(True, True)
        self.configure(fg_color="#F6F5F4")

        # Path & Watcher State (Path.home() works on both Windows and Linux)
        self.selected_path = str(Path.home() / "Downloads")
        self.watcher = FolderWatcher(self.selected_path)
        self.is_running = False
        self.category_rows = {}

        # --- Top Header Bar ---
        self.header_bar = ctk.CTkFrame(self, corner_radius=0, height=48, fg_color="#FFFFFF", border_width=1, border_color="#E1E1E0")
        self.header_bar.pack(fill="x", side="top")

        os_name = "Windows" if sys.platform == "win32" else "Linux"
        self.subtitle_label = ctk.CTkLabel(
            self.header_bar, 
            text=f"Automated Local Directory Sorting ({os_name})", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2E2E2E"
        )
        self.subtitle_label.pack(side="left", padx=22, pady=12)

        self.status_badge = ctk.CTkLabel(
            self.header_bar,
            text="● IDLE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6E6E73",
            fg_color="#EFEFEF",
            corner_radius=10,
            width=80,
            height=24
        )
        self.status_badge.pack(side="right", padx=22, pady=12)

        # --- Main Form Container ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=24, pady=18)

        # --- 1. Target Directory Section ---
        self.folder_group = ctk.CTkFrame(self.main_container, corner_radius=10, border_width=1, border_color="#E1E1E0", fg_color="#FFFFFF")
        self.folder_group.pack(fill="x", pady=(0, 16))

        self.folder_title = ctk.CTkLabel(
            self.folder_group, 
            text="TARGET DIRECTORY", 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6E6E73"
        )
        self.folder_title.pack(anchor="w", padx=18, pady=(12, 6))

        self.input_row = ctk.CTkFrame(self.folder_group, fg_color="transparent")
        self.input_row.pack(fill="x", padx=16, pady=(0, 14))

        self.path_entry = ctk.CTkEntry(
            self.input_row,
            placeholder_text="Select or paste directory path...",
            height=38,
            fg_color="#FAFAFA",
            border_color="#D1D1D0",
            text_color="#2E2E2E",
            font=ctk.CTkFont(size=12)
        )
        self.path_entry.insert(0, self.selected_path)
        self.path_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            self.input_row,
            text="Browse...",
            command=self.browse_folder,
            width=95,
            height=38,
            fg_color="#3584E4",
            hover_color="#1C67C6",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.browse_btn.pack(side="right")

        # --- 2. Organization Rules Section ---
        self.rules_group = ctk.CTkFrame(self.main_container, corner_radius=10, border_width=1, border_color="#E1E1E0", fg_color="#FFFFFF")
        self.rules_group.pack(fill="both", expand=True, pady=(0, 16))

        self.rules_title = ctk.CTkLabel(
            self.rules_group, 
            text="ORGANIZATION RULES", 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6E6E73"
        )
        self.rules_title.pack(anchor="w", padx=18, pady=(12, 8))

        # Grid Container for Categories
        self.grid_container = ctk.CTkFrame(self.rules_group, fg_color="transparent")
        self.grid_container.pack(fill="x", padx=14, pady=(0, 8))

        self.grid_container.grid_columnconfigure(0, weight=1)
        self.grid_container.grid_columnconfigure(1, weight=1)

        raw_categories = list(EXTENSION_MAP.keys())
        cols = 2

        for index, key in enumerate(raw_categories):
            row = index // cols
            col = index % cols

            item_row = CategoryItemRow(
                self.grid_container, 
                key=key, 
                info_callback=self.show_info_banner
            )
            item_row.grid(row=row, column=col, sticky="ew", padx=6, pady=6)
            self.category_rows[key] = item_row

        # --- Dynamic Info Banner Box ---
        self.info_banner = ctk.CTkFrame(self.rules_group, corner_radius=8, fg_color="#F0F0EF", border_width=1, border_color="#E0E0DF")
        self.info_banner.pack(fill="x", padx=18, pady=(6, 12))

        self.info_text = ctk.CTkLabel(
            self.info_banner,
            text="ⓘ Click any (ⓘ) icon on a rule card to view supported file extensions and details.",
            font=ctk.CTkFont(size=11),
            text_color="#444444",
            anchor="w",
            justify="left"
        )
        self.info_text.pack(fill="x", padx=14, pady=10)

        # --- 3. Bottom Action Buttons ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=24, pady=(0, 18))

        self.btn_run_once = ctk.CTkButton(
            self.footer_frame,
            text="Organize Now",
            command=self.run_manual_sort,
            height=44,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#CCCCCC",
            text_color="#2E2E2E",
            hover_color="#EAEAEA"
        )
        self.btn_run_once.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.btn_toggle = ctk.CTkButton(
            self.footer_frame,
            text="Start Auto-Monitor",
            command=self.toggle_monitoring,
            fg_color="#3584E4",
            hover_color="#1C67C6",
            height=44,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_toggle.pack(side="right", expand=True, fill="x", padx=(8, 0))

    def show_info_banner(self, data):
        banner_msg = f"● {data['title']}: {data['desc']}\n  Formats: {data['exts']}"
        self.info_text.configure(text=banner_msg)

    def browse_folder(self):
        current = self.path_entry.get().strip() or str(Path.home())
        chosen_dir = open_native_folder_picker(current)
        if chosen_dir:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, chosen_dir)
            self.selected_path = chosen_dir

    def get_category_states(self):
        return {key: row.is_active for key, row in self.category_rows.items()}

    def run_manual_sort(self):
        target = self.path_entry.get().strip()
        if target:
            organize_directory(target, self.get_category_states())

    def toggle_monitoring(self):
        target = self.path_entry.get().strip()
        if not target or not Path(target).exists():
            return

        if not self.is_running:
            self.selected_path = target
            self.watcher.path_to_watch = self.selected_path
            self.watcher.start(self.get_category_states())
            self.is_running = True
            
            self.btn_toggle.configure(text="Stop Auto-Monitor", fg_color="#E01B24", hover_color="#C0111A")
            self.status_badge.configure(text="● ACTIVE", text_color="#198754", fg_color="#E8F5E9")
        else:
            self.watcher.stop()
            self.is_running = False
            
            self.btn_toggle.configure(text="Start Auto-Monitor", fg_color="#3584E4", hover_color="#1C67C6")
            self.status_badge.configure(text="● IDLE", text_color="#6E6E73", fg_color="#EFEFEF")

    def on_closing(self):
        if self.is_running:
            self.watcher.stop()
        self.destroy()


if __name__ == "__main__":
    app = CrossPlatformFileOrganizer()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
import os
from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror

from common import HyLangFile


class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title_base = "HyLang"
        self.data = {}


        self.title(self.title_base)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Open a yaml file")
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="Open a yaml", command=self.select_file)
        self.button.pack(pady=10)

        self.export = ctk.CTkButton(self, text="Export as .lang", command=self.export_to_lang)
        self.export.pack(pady=10)

    def export_to_lang(self):
        if self.label.cget("text") == "Open a yaml file":
            showerror("Error", "Import a File first")
            return

        file_path = fd.asksaveasfilename(
            title="Export .lang File",
            defaultextension=".lang",
            filetypes=[("Lang files", "*.lang"), ("All files", "*.*")]
        )

        if file_path is None:
            showinfo(f"No file selected - Import first!")
            return

        try:
            flattend = HyLangFile.convert_yamldict_to_langdict(self.data)
            path = file_path.replace(".yaml", ".lang").replace(".yml", ".lang")
            HyLangFile.save_lang(path, flattend)
            showinfo("Success", f"Exported to {Path(file_path).name}")
        except Exception as e:
           showerror("Error", f"Failed to export .lang: {e}")

    def select_file(self):
        filename = fd.askopenfilename(
            title='Open a file',
            filetypes=(
                ('YAML files', '*.yaml *.yml'),
                ('All files', '*.*')
            )
        )

        if filename == ():
            showerror("Error", "No file selected")
            return

        showinfo(
            title='Selected File',
            message=filename
        )
        yaml_data = HyLangFile(Path(filename)).load_yaml()
        self.data = yaml_data
        self.label.configure(text=yaml_data)

        self.title(f"{self.title_base} - {os.path.basename(filename)}")
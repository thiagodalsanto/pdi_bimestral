import tkinter as tk
from components.image_buttons.open_file import open_file
from components.image_buttons.save_image import save_image

def config_frame(self):
    self.master.title("PDI Bimestral")
    self.master.geometry("1200x550")
    self.master.configure(bg="#363636")

    self.frame_image = tk.Frame(self.master)
    self.frame_image.pack(expand=True, fill="both")

    self.frame_buttons = tk.Frame(self.master, bg="#363636")
    self.frame_buttons.pack(side="right", pady=10, padx=10)

    self.load_image_button = tk.Button(self.frame_buttons, text="Send Image", command=lambda: open_file(self), bg="black", fg="white")
    self.load_image_button.pack(side="top", pady=10, fill="both")

    self.save_image_button = tk.Button(self.frame_buttons, text="Save Image", command=lambda: save_image(self), bg="black", fg="white")
    self.save_image_button.pack(side="top", pady=10, fill="both")

    self.remove_effect_button = tk.Button(self.frame_buttons, text="Delete Conversion", command=self.select_filter_to_remove, bg="black", fg="white")
    self.remove_effect_button.pack(side="top", pady=10, fill="both")
from tkinter import messagebox
from opencv_models.contrast import Contrast

class ContrastEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_contrast(self):
        if self.app_instance.image_path:
            contrast = Contrast(self.app_instance.altered_image, "Contraste")
            imagem_contrast, final_value = contrast.run_contrast()
            if imagem_contrast is not None:
                effect_name = f"Contrast (Alpha: {final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "contrast")
                self.app_instance.contrast_effect_applied = True
                self.app_instance.show_image_effect(imagem_contrast)
                self.app_instance.applied_effects.append(("contrast", contrast))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")
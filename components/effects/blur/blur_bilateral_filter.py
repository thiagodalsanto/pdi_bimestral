from tkinter import messagebox
from features.filter import Filter

class BlurBilateralFilterEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_blur_bilateral(self):
        if self.app_instance.image_path:
            bilateral_filter = Filter(self.app_instance.altered_image, "Filtro Bilateral", "bilateral")
            imagem_bilateral, final_value = bilateral_filter.run_filter()
            if imagem_bilateral is not None:
                effect_name = f"Filtro Bilateral Blur ({final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.app_instance.filter_effect_applied = True
                self.app_instance.show_image_effect(imagem_bilateral)
                self.app_instance.applied_effects.append(("filter", imagem_bilateral))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

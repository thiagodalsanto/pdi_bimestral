from tkinter import messagebox
from features.filter import Filter

class BlurGaussianFilterEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_blur_gaussian(self):
        if self.app_instance.image_path:
            gaussian_filter = Filter(self.app_instance.altered_image, "Filter Gaussian", "gaussian")
            imagem_gaussian, final_value = gaussian_filter.run_filter()
            if imagem_gaussian is not None:
                effect_name = f"Filtro Gaussian Blur (Sigma: {final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.app_instance.filter_effect_applied = True
                self.app_instance.show_image_effect(imagem_gaussian)
                self.app_instance.applied_effects.append(("filter", gaussian_filter))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

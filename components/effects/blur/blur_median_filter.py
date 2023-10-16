from tkinter import messagebox
from features.filter import Filter

class BlurMedianFilterEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_median_blur(self):
        if self.app_instance.image_path:
            median_filter = Filter(self.app_instance.altered_image, "Filter Median", "median")
            imagem_median, final_value = median_filter.run_filter()
            if imagem_median is not None:
                effect_name = f"Filtro Median Blur (Kernel Size: {final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.app_instance.filter_effect_applied = True
                self.app_instance.show_image_effect(imagem_median)
                self.app_instance.applied_effects.append(("filter", median_filter))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

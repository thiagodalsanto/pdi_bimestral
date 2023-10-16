from tkinter import messagebox
from features.threshold import Threshold

class ThresholdRGBEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_threshold_rgb(self):
        if self.app_instance.image_path:
            threshold_rgb = Threshold(self.app_instance.altered_image, "Threshold RGB", "binarize_rgb")
            binarized_image, final_value = threshold_rgb.run_threshold()
            if binarized_image is not None:
                effect_name = f"Threshold (Binarização: {final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "threshold")
                self.app_instance.threshold_effect_applied = True
                self.app_instance.show_image_effect(binarized_image)
                self.app_instance.applied_effects.append(("threshold", threshold_rgb))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")
from tkinter import messagebox
from features.morphology import Morphology


class MorphErosionEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_morph_erosion(self):
        if self.app_instance.image_path:
            morphology = Morphology(self.app_instance.altered_image, "Erosao", "erosion")
            erosion_image, final_value = morphology.run_morphology()
            if erosion_image is not None:
                effect_name = f"Erosão (Kernel Size: {final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "morph")
                self.app_instance.morphology_effect_applied = True
                self.app_instance.show_image_effect(erosion_image)
                self.app_instance.applied_effects.append(("morph", morphology))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert")

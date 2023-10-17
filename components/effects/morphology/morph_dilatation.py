from tkinter import messagebox
from opencv_models.morphology import Morphology

class MorphDilatationEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_morph_dilatation(self):
        if self.app_instance.image_path:
            morphology = Morphology(self.app_instance.altered_image, "Dilatacao", "dilatation")
            dilatation_image, final_value = morphology.run_morphology()
            if dilatation_image is not None:
                effect_name = f"Dilatação (Kernel Size: {final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "morph")
                self.app_instance.morphology_effect_applied = True
                self.app_instance.show_image_effect(dilatation_image)
                self.app_instance.applied_effects.append(("morph", morphology))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert")
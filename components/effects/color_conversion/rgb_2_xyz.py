from tkinter import messagebox
from opencv_models.conversion import Conversion

class RGB2XYZEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def cvt_rgb_2_xyz(self):
        if not self.app_instance.conversion_effect_applied and self.app_instance.image_path:
            effect_name = "RGB --> XYZ"
            conversion = Conversion(self.app_instance.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.app_instance.conversion_effect_applied = True
            self.app_instance.show_image_effect(converted_img)
            self.app_instance.applied_effects.append(("conversion", converted_img))
        elif self.app_instance.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")



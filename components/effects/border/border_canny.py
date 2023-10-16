from tkinter import messagebox
from features.border import Border

class CannyBorderEffect:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def apply_canny_border(self):
        if self.app_instance.image_path:
            canny_border = Border(self.app_instance.altered_image, "Canny Border", "canny")
            image_canny, final_value = canny_border.run_border()
            if image_canny is not None:
                effect_name = f"Canny Border ({final_value})"
                self.app_instance.add_effect_to_list_view_applied_effects(effect_name, "border")
                self.app_instance.border_effect_applied = True
                self.app_instance.show_image_effect(image_canny)
                self.app_instance.applied_effects.append(("border", canny_border))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")
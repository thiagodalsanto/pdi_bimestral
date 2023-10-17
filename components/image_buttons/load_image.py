import cv2

def load_image(self):
    self.original_image = cv2.imread(self.image_path)
    self.altered_image = self.original_image.copy()

    self.clear_applied_effects()
    self.show_original_image(self.original_image.copy())
    self.resulted_image = None
    self.show_image_effect(self.altered_image.copy())
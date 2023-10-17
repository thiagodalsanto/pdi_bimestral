from tkinter import filedialog
from components.image_buttons.load_image import load_image

def open_file(self):
    self.image_path = filedialog.askopenfilename()

    if self.image_path:
        print('Selected Archive', self.image_path)
        load_image(self)
    else:
        print('No archive selected')
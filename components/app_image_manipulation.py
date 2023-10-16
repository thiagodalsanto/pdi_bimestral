import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from components.UI.config_frame import config_frame
from components.UI.list_views_config import list_views_config
from components.effects_functions.clear_applied_effects import clear_applied_effects
from components.effects_functions.add_effect_list_applied import add_effect_to_list_view_applied_effects

from components.effects.blur.blur_bilateral_filter import BlurBilateralFilterEffect
from components.effects.blur.blur_gaussian_filter import BlurGaussianFilterEffect
from components.effects.blur.blur_median_filter import BlurMedianFilterEffect
from components.effects.border.border_canny import CannyBorderEffect
from components.effects.color_conversion.rgb_2_cielab import RGB2CIELABEffect
from components.effects.color_conversion.rgb_2_cieluv import RGB2CIELUVEffect
from components.effects.color_conversion.rgb_2_gray import RGB2GRAYEffect
from components.effects.color_conversion.rgb_2_hls import RGB2HLSEffect
from components.effects.color_conversion.rgb_2_hsv import RGB2HSVEffect
from components.effects.color_conversion.rgb_2_xyz import RGB2XYZEffect
from components.effects.color_conversion.rgb_2_ycrcb import RGB2YCRCBEffect
from components.effects.contrast.contrast import ContrastEffect
from components.effects.morphology.morph_dilatation import MorphDilatationEffect
from components.effects.morphology.morph_erosion import MorphErosionEffect
from components.effects.threshold.threshold_gray import ThresholdGrayEffect
from components.effects.threshold.threshold_rgb import ThresholdRGBEffect

class AppImageManipulation:
    def __init__(self, master):
        self.master = master
        self.image_path = None

        self.first_run = True

        self.original_image = None
        self.label_altered_image = None
        self.label_original_image = None
        self.altered_image = None
        self.resulted_image = None

        self.conversion_effect_applied = False
        self.filter_effect_applied = False
        self.border_effect_applied = False
        self.threshold_effect_applied = False
        self.morphology_effect_applied = False
        self.contrast_effect_applied = False
        self.applied_effects = []

        self.list_view_effects = None
        self.list_view_applied_effects = None

        self.frame_image = None

        self.frame_buttons = None
        self.load_image_button = None
        self.remove_effect_button = None
        self.save_image_button = None
        self.generate_histogram_button = None
        self.save_histogram_button = None

        self.count_save_files = 0

        self.directory = "images/"

        self.morph_dilatation_effect = MorphDilatationEffect(self)
        self.morph_erosion_effect = MorphErosionEffect(self)
        self.threshold_rgb_effect = ThresholdRGBEffect(self)
        self.threshold_gray_effect = ThresholdGrayEffect(self)
        self.canny_border_effect = CannyBorderEffect(self)
        self.blur_median_filter_effect = BlurMedianFilterEffect(self)
        self.blur_bilateral_filter_effect = BlurBilateralFilterEffect(self)
        self.blur_gaussian_filter_effect = BlurGaussianFilterEffect(self)
        self.contrast_effect = ContrastEffect(self)
        self.rgb_2_cielab_effect = RGB2CIELABEffect(self)
        self.rgb_2_ycrcb_effect = RGB2YCRCBEffect(self)
        self.rgb_2_hsv_effect = RGB2HSVEffect(self)
        self.rgb_2_hls_effect = RGB2HLSEffect(self)
        self.rgb_2_xyz_effect = RGB2XYZEffect(self)
        self.rgb_2_gray_effect = RGB2GRAYEffect(self)
        self.rgb_2_cieluv_effect = RGB2CIELUVEffect(self)

        config_frame(self)
        list_views_config(self)

    def morph_dilatation(self):
        self.morph_dilatation_effect.apply_morph_dilatation()

    def morph_erosion(self):
        self.morph_erosion_effect.apply_morph_erosion()

    def threshold_rgb(self):
        self.threshold_rgb_effect.apply_threshold_rgb()
    
    def threshold_gray(self):
        self.threshold_gray_effect.apply_threshold_gray()

    def canny_border_detector(self):
        self.canny_border_effect.apply_canny_border()    

    def blur_median_filter(self):
        self.blur_median_filter_effect.apply_median_blur()

    def blur_bilateral_filter(self):
        self.blur_bilateral_filter_effect.apply_blur_bilateral()

    def blur_gaussian_filter(self):
        self.blur_gaussian_filter_effect.apply_blur_gaussian()    

    def apply_contrast(self):
        self.contrast_effect.apply_contrast()

    def cvt_rgb_2_cielab(self):
        self.rgb_2_cielab_effect.cvt_rgb_2_cielab()
    
    def cvt_rgb_2_ycrcb(self):
        self.rgb_2_ycrcb_effect.cvt_rgb_2_ycrcb()

    def cvt_rgb_2_hsv(self):
        self.rgb_2_hsv_effect.cvt_rgb_2_hsv()
    
    def cvt_rgb_2_hls(self):
        self.rgb_2_hls_effect.cvt_rgb_2_hls()

    def cvt_rgb_2_xyz(self):
        self.rgb_2_xyz_effect.cvt_rgb_2_xyz()

    def cvt_rgb_2_gray(self):
        self.rgb_2_gray_effect.cvt_rgb_2_gray()

    def cvt_rgb_2_cieluv(self):
        self.rgb_2_cieluv_effect.cvt_rgb_2_cieluv()

    def clear_applied_effects(self):
        clear_applied_effects(self.list_view_applied_effects, self.applied_effects)

    def add_effect_to_list_view_applied_effects(self, effect_name, tag):
        add_effect_to_list_view_applied_effects(self.list_view_applied_effects, effect_name, tag)

    def remover_filtro(self, tag_item):
        # Remove o filtro que foi selecionado
        self.applied_effects = [op for op in self.applied_effects if op[0] != tag_item]

        # salva uma cópia da imagem original para reconstrução dos filtros
        imagem_sem_filtro = self.original_image.copy()

        # Tenta aplicar o filtro na ordem que foi aplicado inicialmente
        for effect_type, effect in self.applied_effects:
            if effect_type == "conversion":
                imagem_sem_filtro = effect.copy()
            elif effect_type == "morph":
                imagem_sem_filtro = effect.run_morphology(imagem_sem_filtro)
            elif effect_type == "filter":
                imagem_sem_filtro = effect.run_filter(imagem_sem_filtro)
            elif effect_type == "border":
                imagem_sem_filtro = effect.run_border(imagem_sem_filtro)
            elif effect_type == "threshold":
                imagem_sem_filtro = effect.run_threshold(imagem_sem_filtro)
            elif effect_type == "contrast":
                imagem_sem_filtro = effect.run_contrast(imagem_sem_filtro)

        # Atualiza a imagem alterada no frame
        if self.label_altered_image:
            self.label_altered_image.destroy()
            self.resize_altered_image(imagem_sem_filtro)

        # Remove os efeitos aplicados do Bottom List View
        for item in self.list_view_applied_effects.get_children():
            item_tags = self.list_view_applied_effects.item(item)["tags"]
            if tag_item in item_tags:
                self.list_view_applied_effects.delete(item)

        # Redefina as flags de efeitos aplicados
        if tag_item == "conversion":
            self.conversion_effect_applied = False
        elif tag_item == "morph":
            self.morphology_effect_applied = False
        elif tag_item == "filter":
            self.filter_effect_applied = False
        elif tag_item == "border":
            self.border_effect_applied = False
        elif tag_item == "threshold":
            self.threshold_effect_applied = False
        elif tag_item == "contrast":
            self.contrast_effect_applied = False

    def select_filter_to_remove(self):
        selected_item = self.list_view_applied_effects.selection()
        if selected_item:
            effect_text = self.list_view_applied_effects.item(selected_item)
            tag_item = str(effect_text.__getitem__("tags")[0])

            self.remover_filtro(tag_item)
        else:
            messagebox.showinfo("Warning", "Select a convertion to be deleted.")

    def save_image(self):

        # Cria diretorio de não existe
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        while True:
            filename = f'image_{self.count_save_files}.jpg'
            file_path = os.path.join(self.directory, filename)

            # Incrementa se já existir algum arquivo com o número atual
            if os.path.exists(file_path):
                self.count_save_files += 1
            else:
                cv2.imwrite(file_path, self.altered_image)
                print(f'Image save as {filename}')
                break

    def load_image(self):
        self.original_image = cv2.imread(self.image_path)
        self.altered_image = self.original_image.copy()

        self.clear_applied_effects()
        self.show_original_image(self.original_image.copy())
        self.resulted_image = None
        self.show_image_effect(self.altered_image.copy())

    def show_image_effect(self, img):

        if self.label_altered_image:
            self.label_altered_image.destroy()

        self.resize_altered_image(img)

    def resize_altered_image(self, img):
        image_width = 600
        image_height = 350

        resized_image = cv2.resize(img, (image_width, image_height))

        # Convert OpenCV BGR image to RGB
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        self.altered_image = resized_image

        pil_image = Image.fromarray(resized_image_rgb)
        tk_image = ImageTk.PhotoImage(image=pil_image)

        self.label_altered_image = tk.Label(self.frame_image, image=tk_image)
        self.label_altered_image.image = tk_image
        self.label_altered_image.pack(expand=True, fill="both", side="left")

        self.frame_image.update_idletasks()

    def show_original_image(self, img):
        if self.label_original_image and self.label_altered_image:
            self.label_original_image.destroy()
            self.label_altered_image.destroy()

        image_width = 600
        image_height = 350
        resized_image = cv2.resize(img, (image_width, image_height))

        # Convert OpenCV BGR image to RGB
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(resized_image_rgb)
        tk_image = ImageTk.PhotoImage(image=pil_image)

        self.label_original_image = tk.Label(self.frame_image, image=tk_image)
        self.label_original_image.image = tk_image
        self.label_original_image.pack(expand=True, fill="both", side="left")

        self.frame_image.update_idletasks()

    def open_file(self):
        self.image_path = filedialog.askopenfilename()

        if self.image_path:
            print('Selected Archive', self.image_path)
            self.load_image()
        else:
            print('No archive selected')

    def run(self):
        cv2.destroyAllWindows()
        self.master.mainloop()
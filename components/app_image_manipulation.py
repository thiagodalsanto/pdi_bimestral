import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from components.UI.config_frame import config_frame
from components.UI.list_views_config import list_views_config
from components.clear_applied_effects import clear_applied_effects
from components.add_effect_list_applied import add_effect_to_list_view_applied_effects

from components.effects.morphology.morph_dilatation import MorphDilatationEffect
from components.effects.morphology.morph_erosion import MorphErosionEffect
from components.effects.threshold.threshold_gray import ThresholdGrayEffect
from components.effects.threshold.threshold_rgb import ThresholdRGBEffect

from features.filter import Filter
from features.border import Border
from features.conversion import Conversion
from features.contrast import Contrast

class AppImageManipulation:
    def __init__(self, master):

        # Define variaveis no construtor
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
        if self.image_path:
            canny_border = Border(self.altered_image, "Canny Border", "canny")
            image_canny, final_value = canny_border.run_border()
            if image_canny is not None:
                effect_name = f"Canny Border ({final_value})"
                self.add_effect_to_list_view_applied_effects(effect_name, "border")
                self.border_effect_applied = True
                self.show_image_effect(image_canny)
                self.applied_effects.append(("border", canny_border))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def blur_bilateral_filter(self):
        if self.image_path:
            bilateral_filter = Filter(self.altered_image, "Filtro Bilateral", "bilateral")
            imagem_bilateral, final_value = bilateral_filter.run_filter()
            if imagem_bilateral is not None:
                effect_name = f"Filtro Bilateral Blur ({final_value})"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_bilateral)
                self.applied_effects.append(("filter", imagem_bilateral))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def blur_gaussian_filter(self):
        if self.image_path:
            gaussian_filter = Filter(self.altered_image, "Filter Gaussian", "gaussian")
            imagem_gaussian, final_value = gaussian_filter.run_filter()
            if imagem_gaussian is not None:
                effect_name = f"Filtro Gaussian Blur (Sigma: {final_value})"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_gaussian)
                self.applied_effects.append(("filter", gaussian_filter))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def blur_median_filter(self):
        if self.image_path:
            median_filter = Filter(self.altered_image, "Filter Median", "median")
            imagem_median, final_value = median_filter.run_filter()
            if imagem_median is not None:
                effect_name = f"Filtro Median Blur (Kernel Size: {final_value})"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_median)
                self.applied_effects.append(("filter", median_filter))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def apply_contrast(self):
        if self.image_path:
            contrast = Contrast(self.altered_image, "Contraste")
            imagem_contrast, final_value = contrast.run_contrast()
            if imagem_contrast is not None:
                effect_name = f"Contrast (Alpha: {final_value})"
                self.add_effect_to_list_view_applied_effects(effect_name, "contrast")
                self.contrast_effect_applied = True
                self.show_image_effect(imagem_contrast)
                self.applied_effects.append(("contrast", contrast))
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_cieluv(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> CIE L*u*v*"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_cielab(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> CIE L*a*b*"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_hls(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> HLS"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_hsv(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> HSV"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_ycrcb(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> YCrCb"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        # elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_xyz(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> XYZ"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def cvt_rgb_2_gray(self):
        if not self.conversion_effect_applied and self.image_path:
            effect_name = "RGB --> GRAY"
            conversion = Conversion(self.altered_image, " ", effect_name)
            converted_img = conversion.run_conversion()
            self.conversion_effect_applied = True
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

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
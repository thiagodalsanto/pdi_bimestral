import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from effects.filter import Filter
from effects.border import Border
from effects.threshold import Threshold
from effects.morphology import Morphology
from effects.conversion import Conversion
from effects.contrast import Contrast
import os
from matplotlib import pyplot as plt


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

        self.config_frame()
        self.list_views_config()

    def config_frame(self):
        self.master.title("Manipulação de Imagem")
        self.master.geometry("1200x550")
        self.master.configure(bg="#363636")

        self.frame_image = tk.Frame(self.master)
        self.frame_image.pack(expand=True, fill="both")

        self.frame_buttons = tk.Frame(self.master, bg="#363636")
        self.frame_buttons.pack(side="right", pady=10, padx=10)

        self.load_image_button = tk.Button(self.frame_buttons, text="Send Image", command=self.open_file, bg="black", fg="white")
        self.load_image_button.pack(side="top", pady=10)

        self.save_image_button = tk.Button(self.frame_buttons, text="Save Image", command=self.save_image, bg="black", fg="white")
        self.save_image_button.pack(side="top", pady=10)

        self.remove_effect_button = tk.Button(self.frame_buttons, text="Delete Conversion", command=self.select_filter_to_remove, bg="black", fg="white")
        self.remove_effect_button.pack(side="top", pady=10)


    def list_views_config(self):
        self.list_view_effects = ttk.Treeview(self.master)
        self.list_view_effects.column("#0", width=350, minwidth=210)

        self.list_view_effects.tag_configure("cvt_rgb_2_gray", background="white", foreground="black")
        self.list_view_effects.tag_configure("cvt_rgb_2_xyz", background="white", foreground="black")
        self.list_view_effects.tag_configure("cvt_rgb_2_ycrcb", background="white", foreground="black")
        self.list_view_effects.tag_configure("cvt_rgb_2_hsv", background="white", foreground="black")
        self.list_view_effects.tag_configure("cvt_rgb_2_hls", background="white", foreground="black")
        self.list_view_effects.tag_configure("cvt_rgb_2_cielab", background="white", foreground="black")
        self.list_view_effects.tag_configure("cvt_rgb_2_cieluv", background="white", foreground="black")

        # ListView Para conversões de cores
        self.list_view_effects.insert("", "end", text="Convert RGB --> GRAY", tags=("cvt_rgb_2_gray",))
        self.list_view_effects.insert("", "end", text="Convert RGB --> XYZ", tags=("cvt_rgb_2_xyz",))
        self.list_view_effects.insert("", "end", text="Convert RGB --> YCrCb", tags=("cvt_rgb_2_ycrcb",))
        self.list_view_effects.insert("", "end", text="Convert RGB --> HSV", tags=("cvt_rgb_2_hsv",))
        self.list_view_effects.insert("", "end", text="Convert RGB --> HLS", tags=("cvt_rgb_2_hls",))
        self.list_view_effects.insert("", "end", text="Convert RGB --> CIE L*a*b*", tags=("cvt_rgb_2_cielab",))
        self.list_view_effects.insert("", "end", text="Convert RGB --> CIE L*u*v*", tags=("cvt_rgb_2_cieluv",))

        # Atribuição de funções para as opções do ListView de conversão de cores.
        self.list_view_effects.tag_bind("cvt_rgb_2_gray", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_gray())
        self.list_view_effects.tag_bind("cvt_rgb_2_xyz", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_xyz())
        self.list_view_effects.tag_bind("cvt_rgb_2_ycrcb", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_ycrcb())
        self.list_view_effects.tag_bind("cvt_rgb_2_hsv", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_hsv())
        self.list_view_effects.tag_bind("cvt_rgb_2_hls", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_hls())
        self.list_view_effects.tag_bind("cvt_rgb_2_cielab", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_cielab())
        self.list_view_effects.tag_bind("cvt_rgb_2_cieluv", "<ButtonRelease-1>", lambda event: self.cvt_rgb_2_cieluv())

        self.list_view_effects.tag_configure("contrast", background="black", foreground="white")
        
        #ListView para Constraste
        self.list_view_effects.insert("", "end", text="Contrast", tags=("contrast", ))

        #Atribuição de funções para a opção de contraste
        self.list_view_effects.tag_bind("contrast", "<ButtonRelease-1>", lambda event: self.apply_contrast())

        self.list_view_effects.tag_configure("blur_median_filter", background="black", foreground="white")
        self.list_view_effects.tag_configure("blur_gaussian_filter", background="black", foreground="white")
        self.list_view_effects.tag_configure("blur_bilateral_filter", background="black", foreground="white")

        # ListView para Filtros
        self.list_view_effects.insert("", "end", text="Median Blur", tags=("blur_median_filter", ))
        self.list_view_effects.insert("", "end", text="Gaussian Blur", tags=("blur_gaussian_filter", ))
        self.list_view_effects.insert("", "end", text="Bilateral Blur", tags=("blur_bilateral_filter", ))

        # Atribuição de funções para as opções do ListView filtros.
        self.list_view_effects.tag_bind("blur_median_filter", "<ButtonRelease-1>", lambda event: self.blur_median_filter())
        self.list_view_effects.tag_bind("blur_gaussian_filter", "<ButtonRelease-1>", lambda event: self.blur_gaussian_filter())
        self.list_view_effects.tag_bind("blur_bilateral_filter", "<ButtonRelease-1>", lambda event: self.blur_bilateral_filter())

        self.list_view_effects.tag_configure("canny_border_detector", background="white", foreground="black")

        # ListView para detector de bordas
        self.list_view_effects.insert("", "end", text="Canny", tags=("canny_border_detector", ))

        # Atribuição de funções para as opções do ListView de detecção de bordas
        self.list_view_effects.tag_bind("canny_border_detector", "<ButtonRelease-1>", lambda event: self.canny_border_detector())

        self.list_view_effects.tag_configure("threshold_rgb", background="black", foreground="white")
        self.list_view_effects.tag_configure("threshold_gray", background="black", foreground="white")

        # ListView para threshold
        self.list_view_effects.insert("", "end", text="Threshold (RGB)", tags=("threshold_rgb", ))
        self.list_view_effects.insert("", "end", text="Threshold (GRAY)", tags=("threshold_gray", ))

        # Atribuição de funções para as opções de threshold
        self.list_view_effects.tag_bind("threshold_rgb", "<ButtonRelease-1>", lambda event: self.threshold_rgb())
        self.list_view_effects.tag_bind("threshold_gray", "<ButtonRelease-1>", lambda event: self.threshold_gray())

        self.list_view_effects.tag_configure("morph_erosion", background="white", foreground="black")
        self.list_view_effects.tag_configure("morph_dilatation", background="white", foreground="black")
        self.list_view_effects.tag_configure("morph_opening", background="white", foreground="black")
        self.list_view_effects.tag_configure("morph_closure", background="white", foreground="black")

        # ListView para Morfologias Matemáticas
        self.list_view_effects.insert("", "end", text="Erosion", tags=("morph_erosion", ))
        self.list_view_effects.insert("", "end", text="Dialtation", tags=("morph_dilatation", ))
        self.list_view_effects.insert("", "end", text="Openning", tags=("morph_opening", ))
        self.list_view_effects.insert("", "end", text="Closure", tags=("morph_closure", ))

        # Atribuição de funções para as opções de morfologia matemática
        self.list_view_effects.tag_bind("morph_erosion", "<ButtonRelease-1>", lambda evet: self.morph_erosion())
        self.list_view_effects.tag_bind("morph_dilatation", "<ButtonRelease-1>", lambda evet: self.morph_dilatation())
        self.list_view_effects.tag_bind("morph_opening", "<ButtonRelease-1>", lambda evet: self.morph_opening())
        self.list_view_effects.tag_bind("morph_closure", "<ButtonRelease-1>", lambda evet: self.morph_closure())

        self.list_view_effects.pack(side="left", fill="x")

        # Cria um ListView na parte de baixo do frame para mostrar os filtros aplicados
        self.list_view_applied_effects = ttk.Treeview(self.master)
        self.list_view_applied_effects.pack(side="left", fill="x")

    def morph_closure(self):
        if not self.morphology_effect_applied and self.image_path:
            effect_name = "Fechamento"
            self.morph_dilatation()
            self.morphology_effect_applied = False
            self.morph_erosion()
            for item in self.list_view_applied_effects.get_children():
                item_tags = self.list_view_applied_effects.item(item)["tags"]
                if 'morph' == item_tags[0]:
                    self.list_view_applied_effects.delete(item)
            self.add_effect_to_list_view_applied_effects(effect_name, "morph")
        elif self.morphology_effect_applied:
            messagebox.showinfo("Warning", "Morphology already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def morph_opening(self):
        if not self.morphology_effect_applied and self.image_path:
            effect_name = "Abertura"
            self.morph_erosion()
            self.morphology_effect_applied = False
            self.morph_dilatation()
            for item in self.list_view_applied_effects.get_children():
                item_tags = self.list_view_applied_effects.item(item)["tags"]
                if 'morph' == item_tags[0]:
                    self.list_view_applied_effects.delete(item)
            self.add_effect_to_list_view_applied_effects(effect_name, "morph")
        elif self.morphology_effect_applied:
            messagebox.showinfo("Warning", "Morphology already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def morph_dilatation(self):
        if not self.morphology_effect_applied and self.image_path:
            morphology = Morphology(self.altered_image, "Dilatacao", "dilatation")
            dilatation_image = morphology.run_morphology()
            if dilatation_image is not None:
                effect_name = "Dilatação"
                self.add_effect_to_list_view_applied_effects(effect_name, "morph")
                self.morphology_effect_applied = True
                self.show_image_effect(dilatation_image)
                self.applied_effects.append(("morph", morphology))
        elif self.morphology_effect_applied:
            messagebox.showinfo("Warning", "Morphology already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def morph_erosion(self):
        if not self.morphology_effect_applied and self.image_path:
            morphology = Morphology(self.altered_image, "Erosao", "erosion")
            erosion_image = morphology.run_morphology()
            if erosion_image is not None:
                effect_name = "Erosão"
                self.add_effect_to_list_view_applied_effects(effect_name, "morph")
                self.morphology_effect_applied = True
                self.show_image_effect(erosion_image)
                self.applied_effects.append(("morph", morphology))
        elif self.morphology_effect_applied:
            messagebox.showinfo("Warning", "Morphology already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def threshold_gray(self):
        if not self.threshold_effect_applied and self.image_path:
            threshold_gray = Threshold(self.altered_image, "Threshold GRAY", "binarize_gray")
            binarized_image = threshold_gray.run_threshold()
            if binarized_image is not None:
                effect_name = "Threshold Gray"
                self.add_effect_to_list_view_applied_effects(effect_name, "threshold")
                self.threshold_effect_applied = True
                self.show_image_effect(binarized_image)
                self.applied_effects.append(("threshold", threshold_gray))
        elif self.threshold_effect_applied:
            messagebox.showinfo("Warning", "Threshold already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def threshold_rgb(self):
        if not self.threshold_effect_applied and self.image_path:
            threshold_rgb = Threshold(self.altered_image, "Threshold RGB", "binarize_rgb")
            binarized_image = threshold_rgb.run_threshold()
            if binarized_image is not None:
                effect_name = "Threshold"
                self.add_effect_to_list_view_applied_effects(effect_name, "threshold")
                self.threshold_effect_applied = True
                self.show_image_effect(binarized_image)
                self.applied_effects.append(("threshold", threshold_rgb))
        elif self.threshold_effect_applied:
            messagebox.showinfo("Warning", "Threshold already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def canny_border_detector(self):
        if not self.border_effect_applied and self.image_path:
            canny_border = Border(self.altered_image, "Canny Border", "canny")
            image_canny = canny_border.run_border()
            if image_canny is not None:
                effect_name = "Detector de borda Canny"
                self.add_effect_to_list_view_applied_effects(effect_name, "border")
                self.border_effect_applied = True
                self.show_image_effect(image_canny)
                self.applied_effects.append(("border", canny_border))
        elif self.border_effect_applied:
            messagebox.showinfo("Warning", "Border already applied.")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def blur_bilateral_filter(self):
        if not self.filter_effect_applied and self.image_path:
            bilateral_filter = Filter(self.altered_image, "Filtro Bilateral", "bilateral")
            imagem_bilateral = bilateral_filter.run_filter()
            if imagem_bilateral is not None:
                effect_name = "Filtro Bilateral Blur"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_bilateral)
                self.applied_effects.append(("filter", imagem_bilateral))
        elif self.filter_effect_applied:
            messagebox.showinfo("Warning", "Filter already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def blur_gaussian_filter(self):
        if not self.filter_effect_applied and self.image_path:
            gaussian_filter = Filter(self.altered_image, "Filter Gaussian", "gaussian")
            imagem_gaussian = gaussian_filter.run_filter()
            if imagem_gaussian is not None:
                effect_name = "Filtro Gaussian Blur"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_gaussian)
                self.applied_effects.append(("filter", gaussian_filter))
        elif self.filter_effect_applied:
            messagebox.showinfo("Warning", "Filter already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def blur_median_filter(self):
        if not self.filter_effect_applied and self.image_path:
            median_filter = Filter(self.altered_image, "Filter Median", "median")
            imagem_median = median_filter.run_filter()
            if imagem_median is not None:
                effect_name = "Filtro Median Blur"
                self.add_effect_to_list_view_applied_effects(effect_name, "filter")
                self.filter_effect_applied = True
                self.show_image_effect(imagem_median)
                self.applied_effects.append(("filter", median_filter))
        elif self.filter_effect_applied:
            messagebox.showinfo("Warning", "Filter already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def apply_contrast(self):
        if not self.filter_effect_applied and self.image_path:
            contrast = Contrast(self.altered_image, "Contraste")
            imagem_contrast = contrast.run_contrast()
            if imagem_contrast is not None:
                effect_name = "Contraste"
                self.add_effect_to_list_view_applied_effects(effect_name, "contrast")
                self.contrast_effect_applied = True
                self.show_image_effect(imagem_contrast)
                self.applied_effects.append(("contrast", contrast))
        elif self.filter_effect_applied:
            messagebox.showinfo("Warning", "Contrast already applied.")
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
        elif self.conversion_effect_applied:
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
            self.add_effect_to_list_view_applied_effects(effect_name, "conversion")
            self.conversion_effect_applied = True
            self.show_image_effect(converted_img)
            self.applied_effects.append(("conversion", converted_img))
        elif self.conversion_effect_applied:
            messagebox.showinfo("Warning", "Conversion already applied")
        else:
            messagebox.showwarning("Warning", "Load image first, then convert.")

    def add_effect_to_list_view_applied_effects(self, effect_name, tag):
        if tag == "conversion":
            self.list_view_applied_effects.insert("", "end", text=effect_name, tags=("conversion",))
        elif tag == "morph":
            self.list_view_applied_effects.insert("", "end", text=effect_name, tags=("morph",))
        elif tag == "filter":
            self.list_view_applied_effects.insert("", "end", text=effect_name, tags=("filter",))
        elif tag == "border":
            self.list_view_applied_effects.insert("", "end", text=effect_name, tags=("border",))
        elif tag == "threshold":
            self.list_view_applied_effects.insert("", "end", text=effect_name, tags=("threshold",))
        elif tag == "contrast":
            self.list_view_applied_effects.insert("", "end", text=effect_name, tags=("contrast",))

    def clear_applied_effects(self):
        # Limpa todos os itens no Bottom List View
        for item in self.list_view_applied_effects.get_children():
            self.list_view_applied_effects.delete(item)
        self.morphology_effect_applied = False
        self.threshold_effect_applied = False
        self.border_effect_applied = False
        self.conversion_effect_applied = False
        self.filter_effect_applied = False
        self.contrast_effect_applied = False

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
       # self.original_image = cv2.cvtColor(self.original_image.copy(), cv2.COLOR_RGB2BGR)
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


if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageManipulation(root)
    app.run()
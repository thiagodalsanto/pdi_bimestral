import tkinter as tk
from tkinter import ttk

def list_views_config(self):
    self.list_view_effects = ttk.Treeview(self.master)
    self.list_view_effects.column("#0", width=525, minwidth=210)

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

    # ListView para Morfologias Matemáticas
    self.list_view_effects.insert("", "end", text="Erosion", tags=("morph_erosion", ))
    self.list_view_effects.insert("", "end", text="Dialtation", tags=("morph_dilatation", ))

    # Atribuição de funções para as opções de morfologia matemática
    self.list_view_effects.tag_bind("morph_erosion", "<ButtonRelease-1>", lambda evet: self.morph_erosion())
    self.list_view_effects.tag_bind("morph_dilatation", "<ButtonRelease-1>", lambda evet: self.morph_dilatation())

    self.list_view_effects.pack(side="left", fill="x")

    # Cria um ListView na parte de baixo do frame para mostrar os filtros aplicados
    style = ttk.Style()
    style.configure("Treeview", background="#FFFFFF", fieldbackground="#363636")

    self.list_view_applied_effects = ttk.Treeview(self.master, style="Treeview")
    self.list_view_applied_effects.pack(expand=True, side="left", fill="both")
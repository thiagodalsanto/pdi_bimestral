import tkinter.messagebox as messagebox

def clear_applied_effects(list_view_applied_effects, applied_effects):
    # Limpa todos os itens no Bottom List View
    for item in list_view_applied_effects.get_children():
        list_view_applied_effects.delete(item)

    # Redefina as flags de efeitos aplicados
    applied_effects.clear()

def add_effect_to_list_view_applied_effects(list_view_applied_effects, effect_name, tag):
    if tag == "conversion":
        list_view_applied_effects.insert("", "end", text=effect_name, tags=("conversion",))
    elif tag == "morph":
        list_view_applied_effects.insert("", "end", text=effect_name, tags=("morph",))
    elif tag == "filter":
        list_view_applied_effects.insert("", "end", text=effect_name, tags=("filter",))
    elif tag == "border":
        list_view_applied_effects.insert("", "end", text=effect_name, tags=("border",))
    elif tag == "threshold":
        list_view_applied_effects.insert("", "end", text=effect_name, tags=("threshold",))
    elif tag == "contrast":
        list_view_applied_effects.insert("", "end", text=effect_name, tags=("contrast",))

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
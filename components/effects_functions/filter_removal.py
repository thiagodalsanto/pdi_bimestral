class FilterRemoval:
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def remove_filter(self, tag_item):
        # Remove o filtro que foi selecionado
        self.app_instance.applied_effects = [op for op in self.app_instance.applied_effects if op[0] != tag_item]

        # salva uma cópia da imagem original para reconstrução dos filtros
        imagem_sem_filtro = self.app_instance.original_image.copy()

        # Tenta aplicar o filtro na ordem que foi aplicado inicialmente
        for effect_type, effect in self.app_instance.applied_effects:
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
        if self.app_instance.label_altered_image:
            self.app_instance.label_altered_image.destroy()
            self.app_instance.resize_altered_image(imagem_sem_filtro)

        # Remove os efeitos aplicados do Bottom List View
        for item in self.app_instance.list_view_applied_effects.get_children():
            item_tags = self.app_instance.list_view_applied_effects.item(item)["tags"]
            if tag_item in item_tags:
                self.app_instance.list_view_applied_effects.delete(item)

        # Redefina as flags de efeitos aplicados
        if tag_item == "conversion":
            self.app_instance.conversion_effect_applied = False
        elif tag_item == "morph":
            self.app_instance.morphology_effect_applied = False
        elif tag_item == "filter":
            self.app_instance.filter_effect_applied = False
        elif tag_item == "border":
            self.app_instance.border_effect_applied = False
        elif tag_item == "threshold":
            self.app_instance.threshold_effect_applied = False
        elif tag_item == "contrast":
            self.app_instance.contrast_effect_applied = False

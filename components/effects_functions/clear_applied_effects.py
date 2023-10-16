import tkinter.messagebox as messagebox

def clear_applied_effects(list_view_applied_effects, applied_effects):
    # Limpa todos os itens no Bottom List View
    for item in list_view_applied_effects.get_children():
        list_view_applied_effects.delete(item)

    # Redefina as flags de efeitos aplicados
    applied_effects.clear()
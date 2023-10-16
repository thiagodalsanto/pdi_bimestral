import tkinter.messagebox as messagebox

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
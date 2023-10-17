import tkinter as tk
from tkinter import ttk
from components.app_image_manipulation import AppImageManipulation
from components.effects_functions.clear_applied_effects import clear_applied_effects
from components.effects_functions.add_effect_list_applied import add_effect_to_list_view_applied_effects
from components.UI.config_frame import config_frame
from components.UI.list_views_config import list_views_config

from opencv_models.filter import Filter
from opencv_models.border import Border
from opencv_models.threshold import Threshold
from opencv_models.morphology import Morphology
from opencv_models.conversion import Conversion
from opencv_models.contrast import Contrast

if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageManipulation(root)
    app.run()
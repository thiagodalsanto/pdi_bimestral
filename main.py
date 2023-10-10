import tkinter as tk
from components.app_image_manipulation import AppImageManipulation
from effects.filter import Filter
from effects.border import Border
from effects.threshold import Threshold
from effects.morphology import Morphology
from effects.conversion import Conversion
from effects.contrast import Contrast

if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageManipulation(root)
    app.run()

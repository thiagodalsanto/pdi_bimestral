import tkinter as tk
from components.app_image_manipulation import AppImageManipulation
from features.filter import Filter
from features.border import Border
from features.threshold import Threshold
from features.morphology import Morphology
from features.conversion import Conversion
from features.contrast import Contrast


if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageManipulation(root)
    app.run()

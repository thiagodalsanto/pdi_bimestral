import os
import cv2

def save_image(self):

    if not os.path.exists(self.directory):
        os.makedirs(self.directory)

    while True:
        filename = f'image_{self.count_save_files}.jpg'
        file_path = os.path.join(self.directory, filename)

        if os.path.exists(file_path):
            self.count_save_files += 1
        else:
            cv2.imwrite(file_path, self.altered_image)
            print(f'Image save as {filename}')
            break
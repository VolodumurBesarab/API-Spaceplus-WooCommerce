from PIL import Image
import os

class PhotoResizer:
    def __init__(self, output_format='JPEG', output_size=(800, 600)):
        self.output_format = output_format
        self.output_size = output_size

    def resize_photo(self, input_path, output_path):
        """
        Resize a single photo and save it in the desired format.

        :param input_path: Path to the input photo.
        :param output_path: Path to save the resized photo.
        """
        with Image.open(input_path) as img:
            img = img.resize(self.output_size, Image.Resampling.LANCZOS)
            img.save(output_path, self.output_format)
        print(f"Photo saved to {output_path} in {self.output_format} format.")

    def resize_photos_in_folder(self, folder_path, output_folder):
        """
        Resize all photos in a folder and save them to the output folder.

        :param folder_path: Path to the folder containing photos to resize.
        :param output_folder: Path to the folder to save resized photos.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                input_path = os.path.join(folder_path, filename)
                output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.' + self.output_format.lower())
                self.resize_photo(input_path, output_path)
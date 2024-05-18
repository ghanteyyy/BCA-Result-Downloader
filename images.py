from PIL import Image, ImageTk
import utils

class Images:
    def __init__(self):
        self.icon_image = self.resize_image('icon.png', (0, 0))
        self.delete_image = self.resize_image(utils.resource_path('delete.png'))
        self.download_pdf_image = self.resize_image(utils.resource_path('download_pdf.png'))
        self.setting_image = self.resize_image(utils.resource_path('settings.png'), (25, 25))
        self.open_in_browser_image = self.resize_image(utils.resource_path('open_in_browser.png'))
        self.show_in_directory_image = self.resize_image(utils.resource_path('show_in_directory.png'))

    def resize_image(self, image_name, size=(20, 20)):
        """
        Resize the given image to the specified size using Lanczos resampling

        Args:
            - image_name (str): The image to be resized
            - size (tuple): A tuple representing the new size of the image. Default is (40, 40)

        Returns:
            - PIL.Image.Image: The resized image.
        """

        image_path = utils.resource_path(image_name)
        image = Image.open(image_path)

        if size[0] != 0 and size[1] != 0:
            image = image.resize(size, Image.Resampling.LANCZOS)

        image = ImageTk.PhotoImage(image)

        return image

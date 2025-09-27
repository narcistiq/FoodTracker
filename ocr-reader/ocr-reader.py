from typing import List

import easyocr
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os


def is_valid_image(filepath : str):
    """
    Takes in a `filepath`. Returns if it is a valid image or not.

    Returns:
        - True if filepath can be processed
        - False if filepath cannot be processed
    """
    try:
        with Image.open(filepath) as img:
            img.verify()  # Verify file integrity
        return True
    except (IOError, SyntaxError):
        return False

def get_files(folder_path : str) -> List[str]:
    """
    Returns list of files stored in `folder_path`
    """
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Add "/" if folder_path doesn't have it
    if folder_path[-1] != "/":
        folder_path = folder_path + "/"

    files = [folder_path + file for file in files]
    return files

def read_text(reader, image_path : str) -> List[str]:
    """
    Takes in an image path and returns a list of strings
    """

    # Load image from PIL
    image = Image.open(image_path)

    # Convert to grayscale for better results
    image = image.convert("L")

    # Increase contrast to make text stand out
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Resize to make text clearer
    image = image.resize((image.width * 2, image.height * 2))

    # Convert to numpy array
    numpy_image = np.array(image)

    # 3. Run OCR on the processed image
    results = reader.readtext(numpy_image)

    # 4. Print results
    results = reader.readtext(numpy_image)
    cleaned = [result for (_, result, _) in results]
    print(cleaned)


if __name__ == "__main__":
    # Get all images in folder
    FOLDER = "./uploads"
    files = get_files(FOLDER)
    print(files)

    # Initialize OCR reader
    reader = easyocr.Reader(['en'])


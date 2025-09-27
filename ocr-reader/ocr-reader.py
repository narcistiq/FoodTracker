import easyocr
from PIL import Image, ImageEnhance, ImageOps
import numpy as np


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
    # Folder containing all images
    FOLDER = "./uploads/"

    # Initialize OCR reader
    reader = easyocr.Reader(['en'])

# 4. Print results
results = reader.readtext(numpy_image)
cleaned = [result for (_, result, _) in results]
print(cleaned)
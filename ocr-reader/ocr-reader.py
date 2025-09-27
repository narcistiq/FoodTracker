import easyocr
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

# Load image from PIL
image_path = "receipt.jpg"
image = Image.open(image_path)

# Optional: Preprocess the image for better OCR results
# Convert to grayscale
image = image.convert("L")

# Increase contrast to make text stand out
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2.0)

# Resize to make text clearer
image = image.resize((image.width * 2, image.height * 2))

# Convert to numpy array
numpy_image = np.array(image)

# 2. Initialize EasyOCR
reader = easyocr.Reader(['en'])

# 3. Run OCR on the processed image
results = reader.readtext(numpy_image)

# 4. Print results
results = reader.readtext(numpy_image)
cleaned = [result for (_, result, _) in results]
print(cleaned)
import os
from PIL import Image, ImageDraw, ImageFont

def add_watermark(input_image_path, output_image_path, watermark_text):
    base_image = Image.open(input_image_path)
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))

    draw = ImageDraw.Draw(transparent)
    font = ImageFont.truetype("arial.ttf", 40)

    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = width - text_width - 10
    y = height - text_height - 10
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    transparent.save(output_image_path, "PNG")

def process_images_in_directory(input_directory, output_directory, watermark_text):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for image_name in os.listdir(input_directory):
        if image_name.endswith(('.jpg', '.png', '.jpeg')):
            input_image_path = os.path.join(input_directory, image_name)
            output_image_name = os.path.splitext(image_name)[0] + '_' + watermark_text + '.png'
            output_image_path = os.path.join(output_directory, output_image_name)
            add_watermark(input_image_path, output_image_path, watermark_text)

if __name__ == "__main__":
    input_path = input("Enter the path of the image or folder: ")
    watermark_text = input("Enter the watermark text: ")

    if os.path.isfile(input_path):
        # Process a single image
        output_directory = os.path.dirname(input_path)
        process_images_in_directory(os.path.dirname(input_path), output_directory, watermark_text)
    elif os.path.isdir(input_path):
        # Process images in a folder
        output_directory = input_path
        process_images_in_directory(input_path, output_directory, watermark_text)
    else:
        print("Invalid path.")
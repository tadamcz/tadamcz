import json
import os
from io import BytesIO

from PIL import Image, ImageDraw


import cairosvg

def svg_to_png(svg_string):
    output = BytesIO()
    cairosvg.svg2png(bytestring=svg_string.encode('utf-8'), write_to=output, output_width=96)
    output.seek(0)
    return Image.open(output)

def crop_transparent_pixels(image):
    image = image.crop(image.getbbox())
    return image

def add_padding(image: Image, padding: tuple[int, int, int, int]) -> Image:
    left, top, right, bottom = padding
    width, height = image.size

    new_width = width + left + right
    new_height = height + top + bottom

    padded_image = Image.new(image.mode, (new_width, new_height))
    padded_image.paste(image, (left, top))

    return padded_image

def generate_star():
    svg = """
    <svg aria-label="stars" role="img" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-star">
        <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path>
    </svg>
    """
    image = svg_to_png(svg)
    image = crop_transparent_pixels(image)
    top_padding = 16
    if not top_padding % 2 == 0:
        raise ValueError("top_padding must be even")
    padding = (top_padding//2, top_padding, top_padding//2, 0)
    image = add_padding(image, padding)
    image.save('img/star.png')

def generate_dot(color, file_name, size=32):
    img = Image.new('RGB', (size, size), color=color)
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size-1, size-1), fill=255)
    img.putalpha(mask)
    os.makedirs('img', exist_ok=True)
    img.save(f"img/{file_name}")

def color_hex_to_rgb(color_hex):
    return tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    # Load the colors data
    with open('colors.json') as f:
        colors = json.load(f)

    # Load the repos data
    with open('data.json') as f:
        data = json.load(f)

    # Collect the unique languages from the repos data
    languages = set(repo_data['language'] for repo_data in data.values())

    # Generate a PNG file for each unique language
    for language in languages:
        color_hex = colors.get(language, {}).get('color', '#000000').lstrip('#')
        color_rgb = color_hex_to_rgb(color_hex)
        file_name = f"{language.replace(' ', '_').lower()}.png"
        generate_dot(color_rgb, file_name)

    # Generate a PNG file for the star
    generate_star()

######################################################
# Title: Generate Images with Quotes
# File: generateInsta.py
# Author: Suhas Adhav
# Date: 18 April 2021
######################################################

from PIL import Image, ImageFont, ImageDraw
import textwrap
import sys
from settings import FONT_FILE, STORAGE_PATH, BACKGROUND_IMG

# Wraps text according to image size
def text_wrap(text, font, max_width):
    lines = []
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def draw_text(background, text, output):
    img = Image.open(background)
    # size() returns a tuple of (width, height)
    image_size = img.size

    # create the ImageFont instance
    font_file_path = FONT_FILE 
    font = ImageFont.truetype(font_file_path, size=50, encoding="unic")

    # get shorter lines
    lines = text_wrap(text, font, image_size[0]-180)
    # Character which will be largest in height
    line_height = font.getsize('ुठे')[1]
    
    d = ImageDraw.Draw(img)
    x = 120
    y = 540 - (line_height*len(lines)/2)
    for line in lines:
        line_w = font.getsize(line)[0]
        x = (1080 - line_w) /2

        # draw the line on the image
        d.text((x, y), line, fill=(235, 118, 13), font=font)

        # update the y position so that we can use it for next line
        y = y + line_height
    img.save(output)
    

# python generateInsta.py "outputfileName" "Quote to print on the image"
if __name__ == '__main__':
    img_name = sys.argv[1]
    title = sys.argv[2]

    background = BACKGROUND_IMG
    op = STORAGE_PATH + str(img_name) + ".png"

    draw_text(background, title, op)
    print(op)
from PIL import Image, ImageDraw, ImageFont, ImageColor
from io import BytesIO
from functools import partial
from os.path import join, dirname
import logging

### Set up Logging ###

logger = logging.getLogger('ImageManip')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)


def add_overlay_text(qr_in: BytesIO, text: str, font_size: int = 14) -> BytesIO:
    """
    Adds Overlay text to bytestring image coming in
    """
    logger.debug(f"Generating Overlay Image with text: {text}")
    with Image.open(qr_in) as newImg:
        width, height = newImg.size
        draw = ImageDraw.Draw(newImg)
        font_path = join(
            dirname(__file__), 'font', 'Roboto-BlackItalic.ttf')
        font = ImageFont.truetype(font_path, font_size)
        left, top, right, bottom = font.getbbox(text)
        fwidth = abs(right - left)
        fheight = abs(top - bottom)
        if fwidth > width:
            width = fwidth + font_size
        height += fheight
        fullImg = Image.new(newImg.mode, (width, height), color='white')
        fullImg.paste(newImg)
        draw = ImageDraw.Draw(fullImg)
        draw_text = partial(draw.text, font=font,
                            fill=ImageColor.getcolor('black', newImg.mode))
        print(top, bottom, left, right, width, height, fwidth)
        draw_text(((width-fwidth)-(width-fwidth)/2,
                  height-fheight-font_size), text)

        return fullImg

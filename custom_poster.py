from io import BytesIO
import logging
from typing import Dict, Optional, Tuple
from random import choice
import httpx
from constants import COLORS
from fast_colorthief import get_dominant_color
from PIL import Image, ImageDraw, ImageFilter, ImageFont

logger = logging.getLogger(__name__)


class CustomPoster:
    def __init__(
        self,
        poster_info: Dict,
        poster_url: str,
        backdrop_url: Optional[str],
        width: int = 1200,
        height: int = 628,
        offset: int = 50,
        cutoff_width: int = 444,
    ) -> None:
        self.poster_info = poster_info
        self.poster_url = poster_url
        self.backdrop_url = backdrop_url
        self.width = width
        self.height = height
        self.offset = offset
        self.cutoff_width = cutoff_width

    def crop(self, img: Image) -> Image:
        poster_width, poster_height = img.size
        res_width = self.width - self.cutoff_width + self.offset
        res_height = int(res_width / poster_width * poster_height)
        img = img.resize((res_width, res_height), Image.Resampling.LANCZOS)

        left = 0
        top = (res_height - self.height) // 2
        right = res_width
        bottom = (res_height + self.height) // 2

        return img.crop((left, top, right, bottom))

    def format_title(self, maxlen: int = 20, max_lines: int = 3) -> str:
        title = self.poster_info.get("title")
        words = title.split()
        lines = []
        current_line = []
        line_count = 0

        for word in words:
            if len(word) > maxlen:
                word = word[: maxlen - 3] + "..."
            if len(" ".join(current_line + [word])) <= maxlen:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                line_count += 1

            if line_count == max_lines:
                break

        # Add the last line
        if line_count != max_lines:
            lines.append(" ".join(current_line))
        else:
            last_line = lines[-1]
            lines[-1] = last_line[:maxlen] + "..."

        return "\n".join(lines)

    def generate_tags(
        self, draw: ImageDraw, x_axis: int = 50, y_axis: int = 538
    ) -> None:
        tagfont = ImageFont.truetype("Assets/Overpass-SemiBold.ttf", 24)
        font_color = (255, 255, 255)
        padding = 10
        tags = self.poster_info.get("tags")
        for tag in tags:
            text_width = draw.textlength(tag, tagfont)
            if x_axis + text_width + (padding * 4) > 750:
                break
            draw.rounded_rectangle(
                [
                    (x_axis, y_axis),
                    (x_axis + text_width + (padding * 2), y_axis + 30 + padding),
                ],
                fill=(*font_color, 50),
                radius=7,
            )
            draw.text(
                (x_axis + padding, y_axis + padding // 2),
                tag,
                fill=font_color,
                font=tagfont,
            )
            x_axis += text_width + (padding * 4)

        # Freeing memory that was occupied by font
        try:
            del tagfont
        except Exception as e:
            logger.error(str(e))

    def truncate(self, text, draw, font, maxlen=700) -> str:
        text_length = draw.textlength(text, font)
        if text_length > maxlen:
            cutoff = int(maxlen / text_length * len(text))
            return text[: cutoff - 2] + "..."
        else:
            return text

    def paste_star(self, image, logo_color):
        original_logo = Image.open("Assets/star.png")
        original_logo = original_logo.convert("RGBA")
        width, height = original_logo.size
        colored_logo = Image.new("RGBA", (width, height))

        for y in range(height):
            for x in range(width):
                original_pixel = original_logo.getpixel((x, y))
                if original_pixel[3] > 0:
                    colored_pixel = (*logo_color, original_pixel[3])
                    colored_logo.putpixel((x, y), colored_pixel)

        image.paste(colored_logo, (50, 432), colored_logo)

    def dl_poster_backdrop(self) -> Tuple[BytesIO, None]:
        poster_data = BytesIO(httpx.get(self.poster_url).content)
        if self.backdrop_url:
            backdrop_data = BytesIO(httpx.get(self.backdrop_url).content)
        else:
            backdrop_data = None

        return poster_data, backdrop_data

    def generate(self) -> BytesIO:
        background = Image.new("RGB", (self.width, self.height), 0)
        poster_data, backdrop_data = self.dl_poster_backdrop()

        poster = Image.open(poster_data)
        poster_width, poster_height = poster.size

        final_poster_width = int(self.height / poster_height * poster_width)
        if final_poster_width > self.cutoff_width:
            final_poster_width = self.cutoff_width
            crop_width = int(poster_height * self.cutoff_width / self.height)
            left = (poster_width - crop_width) // 2
            top = 0
            right = (poster_width + crop_width) // 2
            bottom = poster_height
            poster = poster.crop((left, top, right, bottom))
        else:
            final_poster_width = self.cutoff_width

        poster = poster.resize(
            (final_poster_width, self.height), resample=Image.Resampling.LANCZOS
        )

        if backdrop_data:
            backdrop = Image.open(backdrop_data)
            backdrop_width, backdrop_height = backdrop.size
            backdrop = backdrop.resize(
                (int(self.height / backdrop_height * backdrop_width), self.height),
                resample=Image.Resampling.LANCZOS,
            )
            backdrop_width, backdrop_height = backdrop.size
            crop_width = self.width - self.cutoff_width + self.offset
            left = (backdrop_width - crop_width) // 2
            top = 0
            right = (backdrop_width + crop_width) // 2
            bottom = backdrop_height
            backdrop = backdrop.crop((left, top, right, bottom))
        else:
            backdrop = self.crop(poster)

        background.paste(poster, (self.width - final_poster_width, 0))

        r, g, b = get_dominant_color(poster_data, quality=10)
        overlay = Image.new(
            "RGBA",
            (self.width - self.cutoff_width + self.offset, self.height),
            (int(r * 0.12), int(g * 0.12), int(b * 0.12), 135),
        )
        poster_overlay = Image.alpha_composite(backdrop.convert("RGBA"), overlay)
        poster_overlay = poster_overlay.filter(ImageFilter.GaussianBlur(radius=10))

        mask_width, mask_height = (
            self.width - self.cutoff_width + self.offset,
            self.height,
        )
        factor = 5
        mask_im = Image.new("L", (mask_width * factor, mask_height * factor), 0)
        draw = ImageDraw.Draw(mask_im)
        draw.polygon(
            [
                (0, 0),
                (mask_width * factor, 0),
                ((mask_width - self.offset) * factor, mask_height * factor),
                (0, mask_height * factor),
            ],
            fill=255,
        )
        mask_im = mask_im.resize(
            (mask_width, mask_height),
            resample=Image.Resampling.LANCZOS,
        )

        background.paste(poster_overlay, (0, 0), mask_im)

        opacity_layer = Image.new("RGBA", background.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(opacity_layer, mode="RGBA")
        boldfont = ImageFont.truetype("Assets/Overpass-SemiBold.ttf", 65)
        normalfont = ImageFont.truetype("Assets/Overpass-SemiBold.ttf", 35)
        smallfont = ImageFont.truetype("Assets/Overpass-Medium.ttf", 25)

        font_color = (255, 255, 255)
        random_font_color = choice(COLORS)

        # premiered
        draw.text(
            (50, 50),
            self.poster_info.get("subtitle"),
            fill=(*font_color, 150),
            font=smallfont,
        )

        # title
        title = self.format_title()
        title_bounds = draw.multiline_textbbox(
            (50, 100),
            title,
            font=boldfont,
            spacing=15,
        )

        draw.multiline_text(
            (50, 100),
            title,
            fill=font_color,
            font=boldfont,
            spacing=15,
        )

        # makers
        draw.text(
            (50, title_bounds[3] + 30),
            self.truncate(", ".join(self.poster_info.get("makers")), draw, normalfont),
            fill=random_font_color,
            font=normalfont,
        )

        # score
        self.paste_star(opacity_layer, random_font_color)
        draw.text(
            (118, 428),
            self.poster_info.get("score"),
            fill=font_color,
            font=boldfont,
        )

        # tags
        self.generate_tags(draw)

        custom_poster = BytesIO()
        result = Image.alpha_composite(background.convert("RGBA"), opacity_layer)
        result.save(custom_poster, format="PNG")

        # Freeing memory that was occupied by image
        try:
            del result
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del poster
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del backdrop
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del poster_overlay
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del mask_im
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del background
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del opacity_layer
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by image
        try:
            del overlay
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by font
        try:
            del boldfont
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by font
        try:
            del normalfont
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by font
        try:
            del smallfont
        except Exception as e:
            logger.error(str(e))

        # Freeing memory that was occupied by draw object
        try:
            del draw
        except Exception as e:
            logger.error(str(e))

        return custom_poster

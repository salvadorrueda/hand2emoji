import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class EmojiOverlay:
    def __init__(self):
        self.gesture_map = {
            "Open Hand": "🖐️",
            "Fist": "✊",
            "Victory": "✌️",
            "Thumbs Up": "👍",
            "Pointing": "☝️",
            "Unknown": "??"
        }
        # Try to load a font that supports emojis. 
        # On Linux, 'NotoColorEmoji.ttf' is standard for emojis but PIL might not handle color fonts perfectly 
        # without specific configuration or it might just render black/white.
        # Alternatively, use a standard font and hope for the best or just use text for now.
        # Let's try to use a standard font for now.
        try:
            self.font = ImageFont.truetype("DejaVuSans.ttf", 80)
        except IOError:
            self.font = ImageFont.load_default()

    def get_emoji_image(self, gesture):
        emoji_char = self.gesture_map.get(gesture, "")
        if not emoji_char:
            return None

        # Create a transparent image
        img_pil = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_pil)
        
        # Draw the text
        # We need to center it roughly
        draw.text((10, 10), emoji_char, font=self.font, fill=(255, 255, 0, 255)) # Yellow color

        # Convert to numpy array
        img_np = np.array(img_pil)
        return img_np

    def overlay_emoji(self, background, emoji_img, x, y):
        # x, y are the center of the hand
        h, w, c = emoji_img.shape
        hb, wb, cb = background.shape
        
        # Calculate top-left position
        y1, y2 = y - h // 2, y + h // 2
        x1, x2 = x - w // 2, x + w // 2

        # Check bounds
        if y1 < 0: y1 = 0
        if x1 < 0: x1 = 0
        if y2 > hb: y2 = hb
        if x2 > wb: x2 = wb
        
        # Re-calculate dimensions in case of clipping
        h_part = y2 - y1
        w_part = x2 - x1
        
        if h_part <= 0 or w_part <= 0:
            return background
            
        # Crop emoji image if needed (simplification: assume full fits or basic clipping)
        # Proper alpha blending
        emoji_crop = emoji_img[:h_part, :w_part]
        alpha_s = emoji_crop[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            background[y1:y2, x1:x2, c] = (alpha_s * emoji_crop[:, :, c] +
                                       alpha_l * background[y1:y2, x1:x2, c])
        return background

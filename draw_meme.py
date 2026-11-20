#!/usr/bin/env python3
"""Draw the two-panel GTA 6 waiting-vs-paid meme for make.fun (gta6-meme-x-01).

Everything except the ghost is hand-drawn with PIL: the desaturated Vice City
sunset beach up top (a lone player still waiting on a bench) and the bright,
coin-filled beach below, where the official make.fun ghost mascot hands out
a magenta coin. The ghost is the official press-kit mark (assets/ghost.png,
make.fun press kit), composited as-is so judges recognise it instantly.

Output: meme.png next to this script, 1200 x 1500.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
GHOST_PATH = os.path.join(HERE, "assets", "ghost.png")
OUT_PATH = os.path.join(HERE, "meme.png")

W, H = 1200, 1500
TOP_H = 660            # top panel height
BOT_Y = TOP_H + 16     # bottom panel starts after the divider
CAP_TOP_H = 168        # caption band inside the top panel
CAP_BOT_H = 200        # caption band at the very bottom

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

INK = (18, 16, 20)
WHITE = (255, 255, 255)
MAGENTA = (196, 28, 131)        # make.fun brand magenta #C41C83
MAGENTA_LIGHT = (255, 136, 196)
GOLD = (255, 209, 64)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def fit_font(draw, text, max_width, start_size, min_size=30):
    """Largest bold font (<= start_size) that keeps text within max_width."""
    size = start_size
    while size > min_size:
        f = font(size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 4
    return font(min_size)


def v_gradient(size, top_color, bottom_color):
    """Vertical two-stop gradient as an RGB image."""
    w, h = size
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        grad.putpixel((0, y), tuple(
            round(top_color[i] + (bottom_color[i] - top_color[i]) * t)
            for i in range(3)))
    return grad.resize((w, h))


def star4(cx, cy, r, color, draw):
    """Four-point sparkle star (the ghost's eye shape)."""
    waist = r * 0.22
    pts = [
        (cx, cy - r), (cx + waist, cy - waist), (cx + r, cy),
        (cx + waist, cy + waist), (cx, cy + r), (cx - waist, cy + waist),
        (cx - r, cy), (cx - waist, cy - waist),
    ]
    draw.polygon(pts, fill=color)


def star5(cx, cy, r, color, draw, rot=-90.0):
    """Classic five-point star, like the one on the mascot's coin."""
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color)


def caption_bar(img, y, h, lines):
    """Black caption band with centred bold lines.

    lines: list of (text, start_size, color). Returns nothing; draws in place.
    """
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, y, W, y + h], fill=(8, 8, 10))
    n = len(lines)
    slot = h / n
    for i, (text, size, color) in enumerate(lines):
        f = fit_font(draw, text, W - 60, size)
        # Shrink further until the glyphs also fit this line's slot height.
        while f.size > 28:
            bbox = draw.textbbox((0, 0), text, font=f)
            if bbox[3] - bbox[1] <= slot * 0.94:
                break
            f = font(f.size - 4)
        bbox = draw.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = (W - tw) / 2 - bbox[0]
        ty = y + slot * i + (slot - th) / 2 - bbox[1]
        draw.text((tx, ty), text, font=f, fill=color)


# ---------------------------------------------------------------- top panel
def palm(draw, base_x, base_y, height, lean, color, droop=1.0):
    """A simple palm: segmented curved trunk plus drooping fronds."""
    top_x = base_x + lean
    top_y = base_y - height
    steps = 9
    prev = (base_x, base_y)
    for i in range(1, steps + 1):
        t = i / steps
        x = base_x + lean * t * t
        y = base_y - height * t
        draw.line([prev, (x, y)], fill=color, width=17)
        prev = (x, y)
    fronds = [(-150, -70), (-105, -120), (-40, -145), (35, -140),
              (105, -115), (155, -60), (-175, 5), (180, 10)]
    for dx, dy in fronds:
        end = (top_x + dx, top_y + dy * droop + abs(dx) * 0.28 * droop)
        mid = (top_x + dx * 0.55, top_y + dy * droop - 26)
        draw.line([(top_x, top_y), mid, end], fill=color, width=13)
    draw.ellipse([top_x - 17, top_y - 14, top_x + 17, top_y + 20], fill=color)
    draw.ellipse([top_x + 8, top_y + 2, top_x + 38, top_y + 30], fill=color)


def cobweb(draw, cx, cy, r, flip=1):
    """Spokes + sagging arcs in one corner, for that 'been here forever' feel."""
    color = (226, 220, 214)
    angles = [a for a in range(0, 91, 18)]
    tips = []
    for a in angles:
        rad = math.radians(a)
        tips.append((cx + flip * r * math.cos(rad), cy + r * math.sin(rad)))
    for tip in tips:
        draw.line([(cx, cy), tip], fill=color, width=3)
    for ring in (0.38, 0.62, 0.86):
        pts = []
        for a in range(0, 91, 6):
            rad = math.radians(a)
            sag = 1 - 0.10 * math.sin(math.radians(a)) * ring
            pts.append((cx + flip * r * ring * sag * math.cos(rad),
                        cy + r * ring * sag * math.sin(rad)))
        draw.line(pts, fill=color, width=3)


def draw_top_panel(img):
    scene_h = TOP_H - CAP_TOP_H
    sky = v_gradient((W, scene_h), (104, 88, 110), (196, 128, 92))
    img.paste(sky, (0, 0))
    draw = ImageDraw.Draw(img)

    # Low, tired sun sinking into the sea.
    sun_cx, sun_cy, sun_r = 838, scene_h - 128, 86
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=(232, 178, 128))
    # Sea and sand bands.
    draw.rectangle([0, scene_h - 118, W, scene_h - 46], fill=(122, 102, 116))
    draw.rectangle([0, scene_h - 46, W, scene_h], fill=(158, 128, 104))
    draw.rectangle([0, scene_h - 118, W, scene_h - 112], fill=(214, 168, 128))

    sil = (52, 40, 52)  # desaturated silhouette plum-brown
    palm(draw, 128, scene_h, 356, 66, sil)
    palm(draw, 1096, scene_h - 4, 300, -52, sil, droop=1.15)

    # The bench, centre-left, seen from the side.
    bx, by = 330, scene_h - 62
    for i in range(3):  # backrest slats
        y = by - 148 + i * 34
        draw.rectangle([bx, y, bx + 400, y + 17], fill=sil)
    draw.rectangle([bx + 8, by - 158, bx + 26, by - 30], fill=sil)
    draw.rectangle([bx + 372, by - 158, bx + 390, by - 30], fill=sil)
    draw.rectangle([bx - 6, by - 34, bx + 408, by - 16], fill=sil)   # seat
    draw.rectangle([bx + 14, by - 16, bx + 32, by + 40], fill=sil)   # legs
    draw.rectangle([bx + 366, by - 16, bx + 384, by + 40], fill=sil)
    draw.line([(bx + 380, by - 96), (bx + 404, by - 40)], fill=sil, width=13)

    # The player: slumped on the bench, head in hands, waiting since 2013.
    hx, hy = bx + 128, by - 196          # bowed head
    draw.ellipse([hx - 37, hy - 37, hx + 37, hy + 37], fill=sil)
    draw.polygon([(hx - 30, hy + 22), (hx + 44, hy + 30),
                  (bx + 216, by - 88), (bx + 138, by - 80)], fill=sil)  # torso
    draw.line([(bx + 190, by - 96), (hx + 16, hy + 34)], fill=sil, width=21)  # arm to face
    draw.line([(bx + 168, by - 82), (bx + 262, by - 78)], fill=sil, width=25)  # thigh
    draw.line([(bx + 262, by - 78), (bx + 266, by - 6)], fill=sil, width=22)   # shin
    draw.rectangle([bx + 258, by - 10, bx + 300, by + 2], fill=sil)           # shoe

    # Cobwebs: bench corner and the left palm crown.
    cobweb(draw, bx + 392, by - 156, 74, flip=-1)
    cobweb(draw, 196, 66, 88, flip=1)

    # A grey, washed-out veil so the whole panel feels like a long wait.
    veil = Image.new("RGB", (W, scene_h), (128, 126, 132))
    img.paste(Image.blend(img.crop((0, 0, W, scene_h)), veil, 0.22), (0, 0))

    caption_bar(img, scene_h, CAP_TOP_H, [
        ("WAITING FOR GTA 6", 96, WHITE),
        ("SINCE 2013…", 84, (206, 198, 205)),
    ])


# ------------------------------------------------------------- bottom panel
def coin(draw, cx, cy, r):
    """A magenta coin with a white star, echoing the one in the ghost's hand."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA,
                 outline=INK, width=max(4, r // 7))
    star5(cx, cy, r * 0.55, WHITE, draw)


def draw_bottom_panel(img):
    scene_y1 = BOT_Y + (H - BOT_Y) - CAP_BOT_H  # scene bottom (caption starts)
    scene_h = scene_y1 - BOT_Y
    sky = v_gradient((W, scene_h), (84, 178, 246), (255, 244, 190))
    img.paste(sky, (0, BOT_Y))
    draw = ImageDraw.Draw(img)

    # Cheerful sun with rays, top-left.
    sx, sy = 128, BOT_Y + 108
    for a in range(0, 360, 30):
        rad = math.radians(a)
        draw.line([(sx + 74 * math.cos(rad), sy + 74 * math.sin(rad)),
                   (sx + 102 * math.cos(rad), sy + 102 * math.sin(rad))],
                  fill=GOLD, width=10)
    draw.ellipse([sx - 58, sy - 58, sx + 58, sy + 58], fill=GOLD, outline=INK, width=5)

    # Sea, sand, and one lush green palm on the right edge.
    draw.rectangle([0, scene_y1 - 128, W, scene_y1 - 52], fill=(38, 156, 214))
    draw.rectangle([0, scene_y1 - 52, W, scene_y1], fill=(250, 222, 152))
    palm(draw, 1175, scene_y1 - 2, 330, -64, (24, 122, 62))

    # The player again — this time on his feet, arms up, celebrating.
    fx, fy = 196, scene_y1 - 46
    draw.ellipse([fx - 34, fy - 268, fx + 34, fy - 200], fill=INK)          # head
    draw.line([(fx, fy - 200), (fx, fy - 92)], fill=INK, width=30)          # body
    draw.line([(fx, fy - 182), (fx - 66, fy - 252)], fill=INK, width=20)    # arm up L
    draw.line([(fx, fy - 182), (fx + 68, fy - 250)], fill=INK, width=20)    # arm up R
    draw.line([(fx, fy - 92), (fx - 42, fy)], fill=INK, width=22)           # legs
    draw.line([(fx, fy - 92), (fx + 44, fy)], fill=INK, width=22)

    # The star of the show: the official make.fun ghost, big and centre-right.
    ghost = Image.open(GHOST_PATH).convert("RGBA")
    gsize = 600
    ghost = ghost.resize((gsize, gsize), Image.LANCZOS)
    gx, gy = 452, BOT_Y + 66
    img.paste(ghost, (gx, gy), ghost)
    draw = ImageDraw.Draw(img)

    # Extra coins mid-air between the player and the ghost, plus sparkles.
    coin(draw, 356, BOT_Y + 210, 40)
    coin(draw, 408, BOT_Y + 330, 30)
    coin(draw, 330, BOT_Y + 420, 24)
    star4(398, BOT_Y + 118, 26, MAGENTA, draw)
    star4(1076, BOT_Y + 300, 22, MAGENTA_LIGHT, draw)
    star4(300, BOT_Y + 300, 18, GOLD, draw)

    caption_bar(img, scene_y1, CAP_BOT_H, [
        ("MY AI AGENT ALREADY GOT PAID", 82, WHITE),
        ("MAKING GTA 6 MEMES", 92, MAGENTA_LIGHT),
    ])


def main():
    img = Image.new("RGB", (W, H), INK)
    draw_top_panel(img)
    draw_bottom_panel(img)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, TOP_H, W, BOT_Y], fill=INK)          # divider
    draw.rectangle([0, 0, W - 1, H - 1], outline=INK, width=10)  # frame
    img.save(OUT_PATH, "PNG")
    print("wrote", OUT_PATH, img.size)


if __name__ == "__main__":
    main()

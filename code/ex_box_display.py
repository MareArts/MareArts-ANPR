import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random

def plot_one_box_PIL(box, img, color=None, label=None, line_thickness=None):
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    line_thickness = line_thickness or max(int(min(img.size) / 200), 2)
    draw.rectangle(box, width=line_thickness, outline=tuple(color))  # plot
    if label:
        fontsize = max(round(max(img.size) / 70), 10)
        #refer to fonts.google.com there are many fonts useable
        font = ImageFont.truetype("NanumBarunGothicBold.ttf", fontsize)
        txt_width, txt_height = font.getsize(label)
        draw.rectangle([box[0], box[1] - txt_height, box[0] + txt_width, box[1]+2], fill=tuple(color))
        draw.text((box[0], box[1] - txt_height + 1), label, fill=(255, 255, 255), font=font)
    return np.asarray(img)


def drawing_rect(drawing_img, lp_result):

    #make gray 3ch image
    drawing_img = cv2.cvtColor(drawing_img, cv2.COLOR_BGR2GRAY)
    drawing_img = cv2.cvtColor(drawing_img,cv2.COLOR_GRAY2RGB)

    #drawing rect
    colors = [random.randint(0, 128) for _ in range(3)]
    for dict_el in lp_result['lp_detect']:
        x1, y1, x2, y2 = dict_el['ltrb']
        han_lp = dict_el['lp_rec']
        lp_d_conf = dict_el['lp_detect_conf']
        lp_r_conf = dict_el['lp_detect_conf']

        label = '{} D{}/R{}'.format(han_lp, int(lp_d_conf*100), int(lp_r_conf*100))
        drawing_img = plot_one_box_PIL([int(x1), int(y1), int(x2), int(y2)], drawing_img, color=colors, label=label, line_thickness=3)

    #resize 840 x Y image
    target_w = 840.0
    if drawing_img.shape[1] > target_w:
        ratio = target_w /drawing_img.shape[1]
        width = int(target_w)
        height = int(drawing_img.shape[0] * ratio)
        dim = (width, height)
        # resize image
        drawing_img = cv2.resize(drawing_img, dim)

    #return gray & green drawing box by 640 size thubnail image
    return drawing_img
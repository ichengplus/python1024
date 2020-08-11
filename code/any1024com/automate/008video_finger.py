'''
手指舞

需要提前安装好paddlehub的ace2p人体部分分割识别模型：
* hub install ace2p

Author: 程一初
'''
# coding=utf-8
import pathlib
import time
import numpy as np
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip
import paddlehub as hub

path = pathlib.Path(
    '~/dev/python/python1024/data/automate/008video/008video_case_finger').expanduser()
mp4_path = path.joinpath('finger.mp4')
parts_path = path.joinpath('human_parts')
label_path = pathlib.Path(
    '~/.paddlehub/modules/ace2p/label_list.txt').expanduser()
finger_out = path.joinpath('finger_out')
ace2p = hub.Module(name='ace2p')
# PART_LIST[灰度值]=名称
with open(label_path, 'r') as f:
    PART_LIST = f.read().splitlines()


def get_palette(num_cls):
    """
    Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """
    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3
    return palette


def save_all(gray_im, cnt):
    """
    根据灰度图，生成整体识别，其中各部分用不同色块标注

    :param gray: 灰度图数据，np.ndarray格式
    :param cnt: 最大灰度值，0表示背景
    :return Image: 返回PIL.Image
    """
    # 对应PIL.Image的L模式，每个像素8bit，0～255表示灰度
    img_pil = Image.fromarray(gray_im)
    palette = get_palette(cnt)
    # 对应PIL.Image的P模式（真彩色），每个像素8bit，根据自定义调色板查询其色彩
    img_pil.putpalette(palette)
    return img_pil


def save_parts(gray_im, cnt, img, out_path):
    """
    根据灰度图生成各个部分的
    :param gray_im: 灰度图, np.ndarray格式
    :param gvsal: 最大灰度值
    :param img: 原图PIL.Image
    :param out_path: 输出目录路径
    """
    gray = Image.fromarray(gray_im)
    for gv in range(cnt):
        image = img.copy().convert('RGBA')
        table = [1 if i == gv else 0 for i in range(256)]
        # 转二值图
        mask = gray.point(table, '1')
        image.putalpha(mask)
        image.save(parts_path.joinpath(f'{PART_LIST[gv]}.png'))


def fl_alpha(im):
    """
    定义每个帧图像处理：只显示脸和四肢
    Face的index是13（从0开始）
    左右手臂：14-15，左右脚：16-17
    """
    im_cv2 = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    results = ace2p.segmentation(images=[im_cv2])
    gray_im = results[0]['data']
    # frame = np.array(im)
    gray = Image.fromarray(gray_im)
    img = Image.fromarray(im).convert('RGBA')
    table = [1 if i in [14, 15] else 0 for i in range(256)]
    mask = gray.point(table, '1')
    img.putalpha(mask)
    img_bg = Image.new('RGBA', img.size, (0, 0, 0))
    img_bg.paste(img, (0, 0), mask=img)
    # img_bg.save(finger_out.joinpath(f'{int(time.time())}.png'))
    # 注意moviepy内部用'RGB'模式
    return np.array(img_bg.convert('RGB'))


if __name__ == "__main__":
    img_path = path.joinpath('finger.png')
    # clip.save_frame(img_path, 5)
    im = cv2.imread(str(img_path))
    results = ace2p.segmentation(images=[im])
    # 这里返回的图像只包含alpha值
    gray_im = results[0]['data']
    # count of options in ~/.paddlehub/modules/ace2p/label_list.txt
    cnt = 20
    img_pil = save_all(gray_im, cnt)
    img_pil.save(path.joinpath('finger_out.png'))

    # 也可以根据灰度图中灰度值，单独生成各个部分的alpha通道，单独保存
    img = Image.open(img_path)
    save_parts(gray_im, cnt, img, parts_path)

    # 生成手指舞
    clip = VideoFileClip(str(mp4_path)).subclip(0, 8).set_fps(5).resize(0.5)
    clip_finger = clip.fl_image(fl_alpha)
    clip_finger.write_videofile(str(path.joinpath(
        'finger_out.mp4')), audio_codec='aac')

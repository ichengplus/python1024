'''
人物重影视频
在处理时，2个注意点：
1. 最好找一些穿纯色衣服的视频，否则可能会出现人物空白点。
2. 背景场地够宽，本例中在原人物左右分别复制了人物。

需要提前安装好paddlehub的人像识别模型：
* hub install deeplabv3p_xception65_humanseg

Author: 程一初
'''
# coding=utf-8
import pathlib
import numpy as np
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip
import paddlehub as hub

path = pathlib.Path(
    '~/dev/python/python1024/data/automate/008video/008video_case_cp').expanduser()
mp4_path = path.joinpath('K2.mp4')
humanseg = hub.Module(name='deeplabv3p_xception65_humanseg')


def fl_alpha(im):
    frame = np.array(im)
    img = Image.fromarray(frame)
    img_cv2 = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    result = humanseg.segmentation(images=[img_cv2])
    img_hum = result[0]['data'].astype(np.uint8)
    image = Image.fromarray(cv2.cvtColor(
        img_hum, cv2.COLOR_BGR2RGBA)).convert('1')
    image_human = img.copy()
    image_human.putalpha(image)
    img.paste(image_human, (img.size[0]//3, 0), mask=image_human)
    img.paste(image_human, (-img.size[0]//3, 0), mask=image_human)
    return np.array(img)


if __name__ == "__main__":
    clip = VideoFileClip(str(mp4_path)).subclip(0, 20).set_fps(5).resize(0.3)
    img_path = path.joinpath('single.png')
    clip.save_frame(img_path, 10)
    img = Image.open(img_path)
    # 转opencv数据格式BGR
    img_cv2 = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    # 识别人像
    result = humanseg.segmentation(images=[img_cv2])
    img_hum = result[0]['data'].astype(np.uint8)
    image = Image.fromarray(cv2.cvtColor(
        img_hum, cv2.COLOR_BGR2RGBA)).convert('1')
    # 生成彩色人像
    image_human = img.copy()
    image_human.putalpha(image)
    # 把彩色人像贴入原图，放在原图人物两边
    img.paste(image_human, (img.size[0]//3, 0), mask=image_human)
    img.paste(image_human, (-img.size[0]//3, 0), mask=image_human)
    img.save(path.joinpath('008video_alpha.png'))

    # 生成视频
    clip_alpha = clip.fl_image(fl_alpha)
    clip_alpha.write_videofile(
        str(path.joinpath('008video_alpha.mp4')), audio_codec='aac')

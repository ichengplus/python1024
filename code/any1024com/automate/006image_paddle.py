'''
需要提前安装好paddlehub及其模型：
* pip install paddlepaddle
* pip install paddlehub
* hub install stylepro_artistic

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
    '~/dev/python/python1024/data/automate/006image/006image_case').expanduser()
style_path = path.joinpath('paddle_styles')
out_folder_path = path.joinpath('006images_case_styles_out')
styleart = hub.Module(name='stylepro_artistic')


def styles_all(im, styles):
    """
    :param im: 要转换风格的原图，cv2图像格式
    :param styles: 风格图像和名字的Tuple列表，(cv2_image, name)
    """
    # 每个风格生成一个图片
    for style, name in styles:
        print(f'生成 {name} 中...')
        result = styleart.style_transfer(
            images=[{
                'content': im,
                'styles': [style]
            }],
            alpha=0.5
        )
        cv2.imwrite(str(out_folder_path.joinpath(
            f'{name}_out.png')), result[0]['data'])


if __name__ == "__main__":
    # 加载所有风格图片
    styles = [(cv2.imread(str(f)), f.stem)
              for f in style_path.iterdir() if f.is_file()]
    img = cv2.imread(str(path.joinpath('moon2.jpg')))
    styles_all(img, styles)

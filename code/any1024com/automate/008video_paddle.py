'''
需要提前安装好paddlehub的两个模型：
* hub install stylepro_artistic
* hub install deeplabv3p_xception65_humanseg

Author: 程一初
'''
# coding=utf-8
import pathlib
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
import paddlehub as hub

path = pathlib.Path(
    '~/dev/python/python1024/data/automate/008video').expanduser()
flv_path = path.joinpath('lisa.flv')
out_style_path = path.joinpath('008video_case_style.mp4')
out_human_path = path.joinpath('008video_case_human.mp4')
out_human_style_path = path.joinpath('008video_case_human_style.mp4')
out_folder_path = path.joinpath('008video_case_style')
style_path = path.joinpath('style2.jpg')

styleart = hub.Module(name='stylepro_artistic')
humanseg = hub.Module(name='deeplabv3p_xception65_humanseg')
img_style = cv2.imread(str(style_path))


def fl_style(im):
    # 应用艺术风格，由于paddlehub内部采用cv2处理，需要先转为BGR模式
    result = styleart.style_transfer(
        images=[{
            'content': cv2.cvtColor(im, cv2.COLOR_RGB2BGR),
            'styles': [img_style]
        }],
        alpha=0.5
    )
    # 转换回RGB模式
    return cv2.cvtColor(result[0]['data'], cv2.COLOR_BGR2RGB)


def fl_human(im):
    # 同样为BGR模式
    result = humanseg.segmentation(images=[im])
    img_hum = result[0]['data'].astype(np.uint8)  # 转单通道
    # 去掉背景
    image = cv2.add(im, np.zeros(np.shape(im), dtype=np.uint8), mask=img_hum)
    # 返回RGB图像
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def fl_human_style(im):
    frame = np.array(im)
    # 先抠人像图，加黑底
    result = humanseg.segmentation(images=[im])
    img_hum = result[0]['data'].astype(np.uint8)
    image = cv2.add(im, np.zeros(np.shape(im), dtype=np.uint8), mask=img_hum)
    # 应用艺术风格
    result = styleart.style_transfer(
        images=[{
            'content': image,
            'styles': [img_style]
        }],
        alpha=0.5
    )
    return cv2.cvtColor(result[0]['data'], cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    clip = VideoFileClip(str(flv_path)).subclip(0, 10).set_fps(5).resize(0.5)
    img_path = out_folder_path.joinpath('single.png')
    clip.save_frame(img_path, 70)
    # 人像抠图
    img = cv2.imread(str(img_path))
    result = humanseg.segmentation(images=[img])
    img_hum = result[0]['data'].astype(np.uint8)
    image = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=img_hum)
    cv2.imwrite(str(out_folder_path.joinpath(
        '008video_case_human_only.png')), image)

    # 单独应用风格
    result = styleart.style_transfer(
        images=[{
            'content': img,
            'styles': [img_style]
        }],
        alpha=0.5
    )
    cv2.imwrite(str(out_folder_path.joinpath(
        '008video_case_style_only.png')), result[0]['data'])

    # 人物应用风格
    result = styleart.style_transfer(
        images=[{
            'content': image,
            'styles': [img_style]
        }],
        alpha=0.5
    )
    cv2.imwrite(str(out_folder_path.joinpath(
        '008video_case_human_style.png')), result[0]['data'])

    # 输出纯黑背景人物
    clip_human = clip.fl_image(fl_human)
    clip_human.write_videofile(str(out_style_path), audio_codec='aac')
    # 直接加style
    clip_style = clip.fl_image(fl_style)
    clip_style.write_videofile(str(out_human_path), audio_codec='aac')
    # 先抠图再应用Style
    clip_hustyle = clip.fl_image(fl_human_style)
    clip_hustyle.write_videofile(str(out_human_style_path), audio_codec='aac')

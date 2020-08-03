'''
@Author: 程一初
'''
# coding=utf-8
import pathlib
from PIL import Image, ImageFont, ImageDraw


def _draw_dash(draw, x1, y1, x2, y2, xstep=10, ystep=0, fill=128):
    '''
    Pillow不支持直接画虚线，我们可以自己实现，画一段段的直线，组合起来就是虚线
    :params draw: ImageDraw对象
    :params x1, y1, x2, y2: 起点，终点
    :params xstep, ystep: 步长，每段虚线长度，这里和空格长度一致
    :params fill: 线条颜色
    '''
    x, y = x1, y1
    while x+xstep <= x2 and y+ystep <= y2:
        draw.line((x, y, x+xstep, y+ystep), fill=fill)
        x += xstep*2
        y += ystep*2


def gen_cards(txt_lines, qrcode_path, imgpath_list, font_path, font_quote_path, out_path):
    '''
    从自选图片生成卡片，带上二维码和金句
    卡片规格：640x1136

    :params txt_lines: 句子
    :params imgpath_list: 图片路径列表
    :params qrcode_path: 二维码路径
    :params out_path: 卡片输出路径
    '''
    if len(txt_lines) != len(imgpath_list):
        print('句子数量需要与图片数量一致')
        return
    W, H = 640, 1136
    TXT_H = int(H*(1-0.618))  # 黄金分割
    TXT_X, TXT_Y = 40, int(H*0.618)+40  # 文案起点
    # 二维码宽、海报边距margin、二维码图片内留白padding
    QR_W, QR_MARGIN, QR_PADDING = TXT_H//3, 40, 10
    QR_X, QR_Y = TXT_X, H-QR_W-QR_MARGIN
    QUOTE = '只差一个程序员了'
    font_quote = ImageFont.truetype(str(font_quote_path), 20)
    quote_w, quote_h = font_quote.getsize(QUOTE)
    QUOTE_X, QUOTE_Y = QR_MARGIN+QR_W, H-QR_MARGIN-quote_h-QR_PADDING-10
    SQUARE_W = quote_h
    SQUARE_X, SQUARE_Y = W-QR_MARGIN-SQUARE_W, QUOTE_Y+QR_PADDING
    font = ImageFont.truetype(str(font_path), 35)
    qrcode_img = Image.open(qrcode_path)
    qrcode_img = qrcode_img.resize((QR_W, QR_W))
    imgpath_list.sort()

    for i, img_path in enumerate(imgpath_list):
        img = Image.new('RGB', (W, H), (255, 255, 255))
        img_bg = Image.open(img_path)
        # 抗锯齿滤镜
        img_bg = img_bg.resize((W, H-TXT_H), Image.ANTIALIAS)
        img.paste(img_bg, (0, 0))
        # 贴上背景图
        draw = ImageDraw.Draw(img)
        # 主体文案
        # 取消尾部换行，中间的换行取消转义
        txt = txt_lines[i].strip('\n').replace('\\n', '\n')
        draw.multiline_text(
            (TXT_X, TXT_Y), txt, font=font, spacing=32, fill=(0, 0, 0))
        # draw.multiline_text(
        #     (TXT_X, TXT_Y), '原来爱情是：我正要表白，\n而你也刚好“正在输入”。', font=font, spacing=32, fill=(0, 0, 0))
        # 画条虚线
        _draw_dash(draw, QUOTE_X, H-QR_MARGIN-QR_PADDING, W-QR_MARGIN-SQUARE_W,
                   H-QR_MARGIN-QR_PADDING, xstep=5, fill=(96, 96, 96))
        # 只差一个程序员了
        draw.text((QUOTE_X, QUOTE_Y), QUOTE, font=font_quote, fill=(0, 0, 0))
        # 画个空心句号，更细腻的可以生成图像贴图，再resize缩小用ANTIALIAS抗锯齿
        draw.ellipse((SQUARE_X, SQUARE_Y, SQUARE_X+SQUARE_W,
                      SQUARE_Y+SQUARE_W), fill=(96, 96, 96), width=0)
        draw.ellipse((SQUARE_X+SQUARE_W//4, SQUARE_Y+SQUARE_W//4,
                      SQUARE_X+SQUARE_W*3//4, SQUARE_Y+SQUARE_W*3//4),
                     fill=(255, 255, 255), width=0)
        # 贴上二维码
        img.paste(qrcode_img, (QR_X, QR_Y))
        # img.show()
        img.save(out_path.joinpath(img_path.name))


if __name__ == "__main__":
    path = pathlib.Path(
        '~/dev/python/python1024/data/automate/006image/006image_case'
    ).expanduser()
    bgimg_path = path.joinpath('images')
    txt_path = path.joinpath('lines.txt')
    qrcode_path = path.joinpath('qrcode.jpg')
    with open(txt_path) as f:
        txt_lines = f.readlines()
    imgpath_list = [f for f in bgimg_path.iterdir() if f.is_file()]
    font_path = path.joinpath('FZKTJW.TTF')
    font_quote_path = path.joinpath('SourceHanSerifSC-Light.otf')
    out_path = path.joinpath('006images_case_cards_out')
    if not out_path.is_dir():
        out_path.mkdir()
    gen_cards(txt_lines, qrcode_path, imgpath_list,
              font_path, font_quote_path, out_path)

# 重新打开带水印文件，去水印
from pdf2image import convert_from_path
from skimage import io
import fitz
import pdfplumber
import pathlib
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from PyPDF2.pdf import ContentStream
from PyPDF2.generic import NameObject
from PyPDF2.pagerange import PageRange
from PyPDF2.utils import b_
import numpy as np

path = pathlib.Path(
    '~/dev/python/python1024').expanduser().joinpath('data/automate/002pdf')
with_wm_path = path.joinpath('002pdf_with_watermark.pdf')
nowm_out_path = path.joinpath('002pdf_no_watermark.pdf')

# 需要提前分析watermark的PDF，查找特征数据
# 穷举法：把某个类别元素，如图片类(cm)输出值，一个个消除测试
TARGET_TXT = np.array([
    [20, 0, 0, 20, 0, 0],
])
TARGET_IMG = np.array([
    [1.5, 0, 0, 1.5, -51, 39],
    # [197.2, 0, 0, 51.05, 213.42, 193.92]
])


def match_location(location, target, epsilon=1e-5):
    """
    计算与特征值的相似度，借用numpy矩阵计算
    """
    loc = np.array([i.as_numeric() for i in location])
    diff = np.abs(loc - target)
    return np.any(diff.max(axis=1) < epsilon)


# 从结果看，MS-Word加的水印，有些指令混在正常数据中，需要更精细调试处理
with open(with_wm_path, 'rb') as f, open(nowm_out_path, 'wb') as f_out:
    pdf = PdfFileReader(f)
    pdf_out = PdfFileWriter()
    # print(pdf.getDocumentInfo())
    cn_pages = pdf.getNumPages()
    for i in range(cn_pages):
        page = pdf.getPage(i)
        content = page.getContents()
        cs = ContentStream(content, pdf)
        for operands, operator in cs.operations:
            # `b_`只是python2/3中bytes类型转换的冗余代码
            if operator == b_('Tm') and match_location(operands, TARGET_TXT):
                operands[:] = []
            elif operator == b_('cm') and match_location(operands, TARGET_IMG):
                operands[:] = []
            elif operator == b_('gs'):
                if operands[0] == '/GS0':
                    operands[:] = []
            elif operator == b_('Do'):
                # 引用图片名称
                if operands[0] == '/Im0':
                    pass
                elif operands[0] == '/Fm0':
                    operands[:] = []
        page.__setitem__(NameObject('/Contents'), cs)
        pdf_out.addPage(page)
    pdf_out.write(f_out)

# 以下对单页测试，图片是加了MS-Word的水印，涉及gs, Do, cm三个指令，文字是Tm指令
# wm_path = path.joinpath('watermark.pdf')
# with open(with_wm_path, 'rb') as f, open(nowm_out_path, 'wb') as f_out:
#     pdf = PdfFileReader(f)
#     pdf_out = PdfFileWriter()
#     page = pdf.getPage(0)
#     content = page.getContents()
#     cs = ContentStream(content, pdf)
#     for operands, operator in cs.operations:
#         # if operator not in [b_('Tm'), b_('Tj'), b_(''), b_('EMC'), b_('Td'), b_('TD'), b_('TJ'), b_('Tf'), b_('Tc'), b_('Q'), b_('q')]:
#         #     print(operator, operands)
#         # print(operator, operands)
#         if operator == b_('Tm') and match_location(operands, TARGET_TXT):
#             operands[:] = []
#         elif operator == b_('cm') and match_location(operands, TARGET_IMG):
#             operands[:] = []
#         elif operator == b_('gs'):
#             if operands[0] == '/GS0':
#                 operands[:] = []
#         elif operator == b_('Do'):
#             # 引用图片名称
#             if operands[0] == '/Im0':
#                 pass
#             elif operands[0] == '/Fm0':
#                 operands[:] = []
#         # elif operator == b_('BDC') and operands[0] == '/Artifact':
#         #     # operands[:] = []
#         #     if operands[1]['/Subtype'] == '/Watermark':
#         #         # operands[:] = []
#         #         print(operands)

#     page.__setitem__(NameObject('/Contents'), cs)
#     pdf_out.addPage(page)
#     pdf_out.write(f_out)

# 以下用pdfplumber识别页面内的图片
# with pdfplumber.open(nowm_out_path) as pdf:
#     page = pdf.pages[0]
#     im = page.to_image()
#     im.draw_rects(page.images)
#     im.save(path.joinpath('002_pdf_wm_img.png'))
#     for img in page.images:
#         print(img['height'], img['width'])

# 以下测试PyMuPDF类库处理指令，能识别和消除图片，但无法处理WS-Word高级的隐藏指令
# doc = fitz.open(nowm_out_path)
# for page in range(doc.pageCount):
#     images = doc.getPageImageList(page)
#     for content in doc[page]._getContents():
#         c = doc._getXrefStream(content)
#         # print(c)
#         for _, _, width, height, _, _, _, img, _ in images:
#             if width == 476 and height == 476:
#                 c = c.replace("/{} Do".format(img).encode(), b"")
#         doc._updateStream(content, c)
# tmp_path = path.joinpath('002_pdf_wm_pymupdf.pdf')
# doc.save(tmp_path)

# 以下演示用图像算法消除水印
# 借助pdf2image库把PDF转图片
# 可以消除图片背景，但因为是图像点阵处理算法，速度很慢，很耗计算资源。
# https://github.com/Belval/pdf2image
'''
首先安装包和依赖
`brew install poppler`
`pip install pdf2image`
`pip install scikit-image`
'''


# def judge(x, y):
#     temp = -(600.0/1575.0) * x
#     if y > 1350 + temp and y < 1500 + temp:
#         return True
#     else:
#         return False


# def select_pixel(r, g, b):
#     if (r == 208 and g == 208 and b == 208) or (r == 196 and g == 196 and b == 196) \
#             or (r == 206 and g == 206 and b == 206):
#         return True
#     else:
#         return False


# def select_pixel2(r, g, b):
#     if r > 175 and r < 250 and g > 175 and g < 250 and b > 175 and b < 250:
#         return True
#     else:
#         return False


# def handle(imgs):
#     for i in range(imgs.shape[0]):
#         for j in range(imgs.shape[1]):
#             if select_pixel2(imgs[i][j][0], imgs[i][j][1], imgs[i][j][2]):
#                 imgs[i][j][0] = imgs[i][j][1] = imgs[i][j][2] = 255
#     return imgs


# images = convert_from_path(with_wm_path)
# index = 0
# img_path = path.joinpath('002_pdf_wm_imgs')
# if not img_path.is_dir():
#     img_path.mkdir()
# for i, img in enumerate(images):
#     img = np.array(img)
#     print(img.shape)
#     img = handle(img)
#     io.imsave(img_path.joinpath(f'{i}.jpg'), img)
#     # break

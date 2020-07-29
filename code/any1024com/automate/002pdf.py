# coding=utf-8
import pathlib
from PyPDF2 import PdfFileReader, PdfFileWriter


def remove_wmpage(file_path, out_path):
    """
    删除PDF中的水印页
    固定删除第二页和最后一页

    Version: 0.0.1
    Author : yichu.cheng
    """
    with open(file_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
        pdf = PdfFileReader(f_in)
        pdf_out = PdfFileWriter()
        cnt_pages = pdf.getNumPages()
        print(f'源文件共 {cnt_pages} 页')
        for i in range(cnt_pages):
            if i not in [1, cnt_pages-1]:
                pdf_out.addPage(pdf.getPage(i))
        pdf_out.write(f_out)


if __name__ == '__main__':
    path = pathlib.Path(
        '~/dev/python/python1024/data/automate/002pdf').expanduser()
    path = path.joinpath('002pdf_case_wm')
    file_path_list = path.glob('*.pdf')
    for file_path in file_path_list:
        out_name = f'{file_path.stem}_nowm.{file_path.suffix}'
        out_path = path.joinpath(out_name)
        remove_wmpage(file_path, out_path)

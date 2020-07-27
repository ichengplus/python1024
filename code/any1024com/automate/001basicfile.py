# coding=utf-8
import pathlib


def file_rw():
    """
    基本文件处理

    Version: 0.0.1
    Author : yichu.cheng
    """
    path = list(pathlib.Path(__file__).parents)[3].joinpath('data/automate')
    if not path.is_dir():
        path.mkdir(exist_ok=True)
    file_path = path.joinpath('001file.txt')
    # 写文件
    with open(file_path, 'w') as f:
        f.write('文件处理测试')
    # 获取文件信息
    print(f'文件名: {file_path.stem}, 文件后缀: {file_path.suffix}')
    print(f'文件大小(字节): {file_path.stat().st_size}')
    # 读文件
    with open(file_path, 'r') as f:
        txt = f.read()
        print(txt)


if __name__ == '__main__':
    file_rw()

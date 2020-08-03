# coding=utf-8
import pathlib
import random

EXT_DICT = {
    '图片': ['jpeg', 'jpg', 'tiff', 'gif', 'bmp', 'png', 'svg', 'psd'],
    '视频': ['avi', 'flv', 'mov', 'mp4', 'webm', 'mpeg', '3gp', 'mkv'],
    '文档': ['txt', 'epub', 'pages', 'key', 'numbers',
           'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'csv', 'pdf'],
    '压缩文件': ['rar', 'tar', 'gz', '7z', 'dmg', 'zip', 'iso'],
    '音频': ['aac', 'm4a', 'mp3', 'ogg', 'raw', 'wav', 'wma'],
    '代码': ['py', 'html', 'js', 'c', 'cpp', 'java', 'css'],
    '应用程序': ['exe'],
}


def file_rw():
    """
    基本文件处理

    Version: 0.0.1
    Author : yichu.cheng
    """
    path = list(pathlib.Path(__file__).parents)[
        3].joinpath('data/automate/001basic')
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


def folder_iter():
    """
    列出当前文件夹下所有python代码文件

    Version: 0.0.1
    Author : yichu.cheng
    """
    path = pathlib.Path().cwd()
    all_py_files = list(path.glob('**/*.py'))
    for f in all_py_files:
        print(f)


def auto_arrange_files(file_folder):
    """
    自动根据文件后缀名分类文件夹
    在文件所在目录下整理到arraged_folder子目录
    :params file_folder: 文件所在目录路径

    Version: 0.0.1
    Author : yichu.cheng
    """
    out_path = file_folder.joinpath('arraged_folder')
    if not out_path.is_dir():
        out_path.mkdir()

    # 为每个类型创建一个子文件夹
    for key in EXT_DICT.keys():
        folder = out_path.joinpath(key)
        if not folder.is_dir():
            folder.mkdir()
    # 找出所有文件的路径
    file_list = [f for f in file_folder.iterdir() if f.is_file()]
    for f in file_list:
        # 找出所属分类
        clz = [k for k, v in EXT_DICT.items() if f.suffix[1:] in v]
        clz = clz[0] if clz else ''
        f.rename(out_path.joinpath(clz).joinpath(f.name))


def gen_random_fake_files(file_folder):
    """
    随机生成一些假文件，随机的后缀名
    :params file_folder: 文件所在目录路径

    Version: 0.0.1
    Author : yichu.cheng
    """

    for i in range(100):
        key = random.choice(list(EXT_DICT.keys()))
        ext = random.choice(EXT_DICT[key])
        f = file_folder.joinpath(f'{i}.{ext}')
        if not f.is_file():
            f.touch()


if __name__ == '__main__':
    file_rw()
    folder_iter()
    path = pathlib.Path().cwd().joinpath('data/automate/001basic')
    in_path = path.joinpath('001file_folder')
    if not in_path.is_dir():
        in_path.mkdir()
    # 先随机生成一批文档
    # gen_random_fake_files(in_path)
    auto_arrange_files(in_path)

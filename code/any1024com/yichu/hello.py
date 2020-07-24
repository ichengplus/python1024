# coding=utf-8
def hello(name):
    """some notes"""
    msg = 'Hello Python!'
    print('{}: {}'.format(name, msg))


import logging

logger = logging.getLogger('hello.test')
logger.setLevel(logging.DEBUG)
log_fmt = logging.Formatter(
    '%(asctime)s : %(name)s : %(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 用FileHandler输出到文件
f_handler = logging.FileHandler('hello.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(log_fmt)
# 用StreamHandler输出到Console
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(log_fmt)
# 添加两个Handler
logger.addHandler(f_handler)
logger.addHandler(c_handler)

logger.debug("This is a debug log.")
logger.info("This is a info log.")
logger.warning("This is a warning log.")
logger.error("This is a error log.")
logger.critical("This is a critical log.")

if __name__ == '__main__':
    hello('yichu')

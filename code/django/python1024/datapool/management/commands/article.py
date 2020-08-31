from django.core.management.base import BaseCommand
import requests
from lxml import etree
from datapool.models import Article


def extract_articles(url):
    """
    从链接中抽取文章，保存到数据库
    """
    r = requests.get(url)
    root = etree.HTML(r.content)
    link_list = root.xpath('//*[@id="js_content"]//a')
    articles = [Article(title=link.xpath('.//text()')[0],
                        url=link.get('href')) for link in link_list]
    for article in articles:
        article.save()
    print(f'一共发现 {len(articles)} 篇文章，数据库共 {Article.objects.count()} 篇文章。')


class Command(BaseCommand):
    """
    继承Django提供的命令行基本类
    https://mp.weixin.qq.com/s/JFEASRL17bnr6fRJfezixA
    """
    help = '文章抓取'

    def add_arguments(self, parser):
        """接收命令行参数"""
        parser.add_argument(
            '-u', '--url', type=str, help='汇总类文章链接')

    def handle(self, *args, **kwargs):
        """命令行处理入口"""
        # 获取参数
        url = kwargs['url']
        if url:
            extract_articles(url)
        else:
            print('请输入包含文章链接的访问地址')

from django.db import models


class Article(models.Model):
    """
    文章模型类
    """
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=256)

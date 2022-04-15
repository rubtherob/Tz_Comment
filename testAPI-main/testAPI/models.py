from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class Article(models.Model):
    text = models.CharField(max_length=140, blank=False)
    recorded_at = models.DateTimeField(blank=False)
    modified_at = models.DateTimeField(auto_now_add=True)


class Comment(MPTTModel):
    message = models.CharField(max_length=140, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='parent',
        related_name='replys',
    )
    article = models.ForeignKey('Article', on_delete=models.CASCADE, default=1, related_name='article')

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['message']
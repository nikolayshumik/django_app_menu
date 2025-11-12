from django.db import models
from django.urls import reverse

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Menu name')

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    url = models.CharField(max_length=500, blank=True, null=True,
                           help_text='Absolute URL or relative path, e.g. /about/')
    named_url = models.CharField(max_length=200, blank=True, null=True,
                                 help_text='Optional: name of URL pattern (for reverse())')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'

    def __str__(self):
        return self.title

    def get_url(self):
        # prefer named_url if set
        if self.named_url:
            try:
                return reverse(self.named_url)
            except Exception:
                # fall back to raw url if reverse fails
                pass
        return self.url or '#'

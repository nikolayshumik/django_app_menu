from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import MenuItem, Menu


def clear_menu_cache(menu_name=None):
    """Clear cache of menu"""
    if menu_name:
        cache.delete(f"menu_cache_{menu_name}")
    else:
        cache.clear()


@receiver(post_save, sender=MenuItem)
def clear_cache_on_menuitem_change(sender, instance, **kwargs):
    """clear cache if menu item is changed"""
    if instance.menu:
        clear_menu_cache(instance.menu.name)


@receiver(post_delete, sender=MenuItem)
def clear_cache_on_menuitem_delete(sender, instance, **kwargs):
    """Clear cache if menu item is deleted"""
    if instance.menu:
        clear_menu_cache(instance.menu.name)


@receiver(post_save, sender=Menu)
def clear_cache_on_menu_change(sender, instance, **kwargs):
    """Clear cache if menu is changed"""
    clear_menu_cache(instance.name)


@receiver(post_delete, sender=Menu)
def clear_cache_on_menu_delete(sender, instance, **kwargs):
    """Clear cache if menu is deleted"""
    clear_menu_cache(instance.name)

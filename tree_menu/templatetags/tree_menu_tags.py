from django import template
from django.urls import resolve
from django.core.cache import cache
from tree_menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    path = request.path if request is not None else None

    # without cache
    # items = list(MenuItem.objects.filter(menu__name=menu_name).select_related('parent'))
    #
    # if not items:
    #     return {'menu_items': [], 'expanded_ids': set(), 'active_item_id': None}

    cache_key = f"menu_cache_{menu_name}"
    items = cache.get(cache_key)
    if not items:
        # One sql
        items = list(MenuItem.objects.filter(menu__name=menu_name).select_related('parent'))
        cache.set(cache_key, items, 300)

    if not items:
        return {'menu_items': [], 'expanded_ids': set(), 'active_item_id': None}

    # Build mapping and children lists
    item_by_id = {}
    for it in items:
        it.children_list = []
        item_by_id[it.id] = it

    roots = []
    for it in items:
        if it.parent_id and it.parent_id in item_by_id:
            item_by_id[it.parent_id].children_list.append(it)
        else:
            roots.append(it)

    # Determine active item by comparing resolved URL paths.
    active_item = None
    for it in items:
        try:
            if path and it.get_url() == path:
                active_item = it
                break
        except Exception:
            continue

    # Determine expanded ids: all ancestors of active_item + the active_item itself.
    expanded_ids = set()
    if active_item:
        expanded_ids.add(active_item.id)
        parent = active_item.parent
        while parent:
            expanded_ids.add(parent.id)
            parent = parent.parent

    return {
        'menu_items': roots,
        'expanded_ids': expanded_ids,
        'active_item_id': active_item.id if active_item else None,
    }

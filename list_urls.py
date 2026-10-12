from django.urls import get_resolver


def walk(patterns, prefix=''):
    for p in patterns:
        full = prefix + str(p.pattern)
        if hasattr(p, 'url_patterns'):
            if not full.startswith('admin/'):
                walk(p.url_patterns, full)
        else:
            cb = p.callback
            view = getattr(cb, 'view_class', cb).__name__
            print(full.ljust(38), (p.name or '-').ljust(20), view)


walk(get_resolver().url_patterns)
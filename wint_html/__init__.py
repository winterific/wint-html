import html as m_html
import collections

html5doctype = "<!DOCTYPE html>"


def is_list(obj):
    return not isinstance(obj, str) and isinstance(obj, collections.Iterable)


def flatten(items, new_list):
    for item in items:
        if is_list(item):
            flatten(item, new_list)
        else:
            new_list.append(item)


class H:
    def __init__(self, *args, self_closing=False, **kwargs):
        self.name = ""
        self.attrs = {}
        self.children = []
        self.self_closing = self_closing
        for i, arg in enumerate(args):
            if i == 0 and type(arg) is str:
                self.name = arg
            elif type(arg) is dict:
                self.attrs = arg
            elif is_list(arg):
                flattened_arg = []
                flatten(arg, flattened_arg)
                self.children += flattened_arg
            else:
                self.children.append(arg)
        for k, v in kwargs.items():
            self.attrs[k] = v

    def __repr__(self):
        attributes = ""
        if self.attrs:
            for k, v in self.attrs.items():
                if isinstance(v, bool):
                    if v:
                        attributes += f" {k}"
                elif isinstance(v, (str, int, float)):
                    val = f"{v}"
                    attributes += f" {k}=\"{m_html.escape(m_html.unescape(val))}\""
        child_html = ""
        if self.children:
            for child in self.children:
                if child is None:
                    pass
                elif type(child) is str and self.name not in ("script", "style"):
                    child_html += m_html.escape(m_html.unescape(child),
                                                quote=False)
                else:
                    child_html += str(child)
        if self.self_closing:
            return f"<{self.name}{attributes}/>"
        return f"<{self.name}{attributes}>{child_html}</{self.name}>"


def self_closing_tag(name):
    def tag(*args, **kwargs):
        return H(name, kwargs, *args, self_closing=True)
    return tag


self_closing_tags = ("meta", "link", "br", "img", "hr", "input")
for tag in self_closing_tags:
    globals()[tag] = self_closing_tag(tag)


def regular_tag(name):
    def tag(*args, **kwargs):
        return H(name, *args, **kwargs)
    return tag


regular_tags = ("html", "body", "head",
                "script", "style", "ul", "li",
                "title", "header", "footer", "main", "nav", "aside", 'section', "p", "b", "i", "div", "span", "a", "form", 'em', 'strong', 'dl', 'dd',
                "h1", "h2", "h3", "h4", "h5", "h6")
for tag in regular_tags:
    globals()[tag] = regular_tag(tag)

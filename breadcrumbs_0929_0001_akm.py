# 代码生成时间: 2025-09-29 00:01:31
import django.urls
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import Context

"""
A Django app component for a breadcrumb navigation system.
It provides a way to generate breadcrumb trails dynamically
based on the URL conf.
"""

class Breadcrumb:
    """
    A simple breadcrumb generator class.
    It uses the URL conf to generate a list of breadcrumbs.
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = []

    def add(self, name, url):
        """
        Adds a breadcrumb to the trail.
        Args:
            name (str): The display name of the breadcrumb.
            url (str): The URL for the breadcrumb.
        """
        self.breadcrumbs.append((name, url))

    def clear(self):
        """
        Clears the breadcrumb trail.
        """
        self.breadcrumbs = []

    def get_breadcrumbs(self):
        """
        Returns the breadcrumb trail as a list of tuples.
        Returns:
            list: A list of tuples, each containing the name and URL of a breadcrumb.
        """
        return self.breadcrumbs

    def render(self):
        """
        Renders the breadcrumb trail as HTML.
        Returns:
            str: The HTML representation of the breadcrumb trail.
        """
        if not self.breadcrumbs:
            return ''
        
        context = Context({'breadcrumbs': self.breadcrumbs})
        return mark_safe(render_to_string('breadcrumbs.html', context))

# Sample usage in a view
# def my_view(request):
#     bread = Breadcrumb(request)
#     bread.add('Home', '/')
#     bread.add('Category', '/category/')
#     bread.add('Product', '/product/')
#     return render(request, 'my_template.html', {'breadcrumbs': bread.render()})

# breadcrumbs.html
# {% for breadcrumb in breadcrumbs %}
#     {% if forloop.last %}
#         <span>{{ breadcrumb.0 }}</span>
#     {% else %}
#         <a href="{{ breadcrumb.1 }}">{{ breadcrumb.0 }}</a>
#         {% if not forloop.last %}
#             &gt;
#         {% endif %}
#     {% endif %}
# {% endfor %}

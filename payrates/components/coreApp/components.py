from django_viewcomponent import component
from django_viewcomponent.fields import RendersOneField
@component.register("hello")
class HelloComponent(component.Component):
    template = "<h1>Hello, {{ self.name }}!</h1>"

    def __init__(self, **kwargs):
        self.name = kwargs['name']      
        
@component.register("blog")
class BlogComponent(component.Component):
    header = RendersOneField(required=True)

    template = """
        {% load viewcomponent_tags %}
        
        {{ self.header.value }}
    """
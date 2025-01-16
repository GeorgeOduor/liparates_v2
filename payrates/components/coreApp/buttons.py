from django_viewcomponent import component


@component.register("button")
class ButtonComponent(component.Component):
    template = """
    <button class="{{ self.classes }}" type="{{ self.type }}" onclick="{{ self.onclick }}">
        {% if self.icon %}
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{{ self.icon_path }}" />
        </svg>
        {% endif %}
        {{ self.label }}
    </button>
    """

    def __init__(self, label, type="button", classes="", icon=False, icon_path="", onclick=""):
        self.label = label
        self.type = type
        self.classes = classes
        self.icon = icon
        self.icon_path = icon_path
        self.onclick = onclick

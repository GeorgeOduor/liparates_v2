from django_viewcomponent import component


@component.register("form")
class FormComponent(component.Component):
    template_name = "core/partials/form_template.html"

    # Pass context data to the template
    def get_context_data(self):
        return {
            "form": self.form,  # Use self.form from __init__
            "method": self.method,
            "submit_label": self.submit_label,
            "title": self.title,
            "description": self.description,
        }

    # Initialize the form component
    def __init__(self, form, method="post", submit_label="Submit", title=None, description=None):
        self.form = form
        self.method = method
        self.submit_label = submit_label
        self.title = title
        self.description = description
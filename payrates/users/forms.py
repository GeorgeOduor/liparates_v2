from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "placeholder": "someone@domain.com",
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-2 focus:bg-transparent  transition-all",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-2 focus:bg-transparent  transition-all",
            }
        ),
    )
    rememberme = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 shrink-0 border-gray-300 rounded py-2 mb-4",
            }
        ),
    )


# register form


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your first name", 
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-0 focus:bg-transparent  transition-all",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your last name",
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-0 focus:bg-transparent  transition-all",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter email",
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-0 focus:bg-transparent  transition-all",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-0 focus:bg-transparent  transition-all",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "class": "bg-gray-100 w-full text-sm text-gray-800 px-4 py-0 focus:bg-transparent  transition-all",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error("confirm_password", "The two passwords do not match.")

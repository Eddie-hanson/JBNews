from .models import ContactMessage, Comment, NewsletterSubscriber
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class":       "form-control",
                "placeholder": "Your Name",
            }),
            "email": forms.EmailInput(attrs={
                "class":       "form-control",
                "placeholder": "Your Email",
            }),
            "subject": forms.TextInput(attrs={
                "class":       "form-control",
                "placeholder": "Subject",
            }),
            "message": forms.Textarea(attrs={
                "class":       "form-control",
                "placeholder": "Message",
                "rows":        4,
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class":       "form-control",
                "placeholder": "Your Name",
            }),
            "email": forms.EmailInput(attrs={
                "class":       "form-control",
                "placeholder": "Your Email",
            }),
            "body": forms.Textarea(attrs={
                "class":       "form-control",
                "placeholder": "Write your comment...",
                "rows":        4,
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class":       "form-control",
                "placeholder": "Your email here",
            })
        }

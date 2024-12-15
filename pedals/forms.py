from django import forms
from .models import Comment
from better_profanity import profanity
import re

class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = Comment
        fields = ['author_name', 'email', 'content', 'rating']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment', 'rows': 4}),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        
        # Check for URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        if re.search(url_pattern, content):
            raise forms.ValidationError("URLs are not allowed in comments.")
        
        # Filter profanity
        filtered_content = profanity.censor(content)
        if filtered_content != content:
            raise forms.ValidationError("Please keep comments family-friendly and avoid inappropriate language.")
        
        return content

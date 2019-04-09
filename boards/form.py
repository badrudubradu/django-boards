from django import forms
from .models import Topic, Board, Post

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
    widget=forms.Textarea(attrs={'rows':5, 'placeholder':'Your first message'}),
    max_length=4000,
    help_text='Maximum length is 4000 characters.')

    class Meta:
        model = Topic
        fields = ['subject','message']

class NewBoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ['name','description']

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['message']

# store/forms.py
from django import forms
from .models import Review

# ... (your other forms if any) ...

class ReviewForm(forms.ModelForm):
    # Use a RadioSelect widget for a star-like rating input
    rating = forms.IntegerField(
        widget=forms.RadioSelect(
            attrs={'class': 'rating-stars'}, 
            choices=[(i, str(i)) for i in range(1, 6)]
        ),
        min_value=1,
        max_value=5
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts...'}
        ),
        required=False # Make comment optional
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
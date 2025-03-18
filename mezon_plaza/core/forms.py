from django import forms
from .models import Comment, Unit


class CommentForm(forms.ModelForm):
    """Форма для добавления комментария"""
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Введите комментарий..."}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    """Кастомный виджет для загрузки нескольких файлов"""
    allow_multiple_selected = True  # Включаем множественный выбор файлов


class FileUploadForm(forms.Form):
    """Форма загрузки файлов отдельно от комментария"""
    files = forms.FileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False,
        label="Прикрепить файлы"
    )


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'number',
            'floor',
            'area',
            'height',
            'status',
            'tenant',
            'lease_start',
            'lease_end'
        ]
        labels = {
            'number': 'Номер помещения',
            'floor': 'Этаж',
            'area': 'Площадь (кв.м)',
            'height': 'Высота потолка (м)',
            'status': 'Статус аренды',
            'tenant': 'Арендатор',
            'lease_start': 'Дата начала аренды',
            'lease_end': 'Дата окончания аренды',
        }
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control border-dark',
                'placeholder': 'Например, 101A',
                'aria-label': 'Имя пользователя',
                'aria-describedby': 'InputNumber'
            }),
            'floor': forms.Select(attrs={
                'class': 'form-select border-dark',
                'id': 'inputGroupFloor'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control border-dark',
                'placeholder': 'Площадь помещения',
                'aria-label': 'Площадь помещения',
                'aria-describedby': 'InputArea'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control border-dark',
                'placeholder': 'Высота потолков',
                'aria-label': 'Высота потолков',
                'aria-describedby': 'InputHeight'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select border-dark',
                'id': 'inputGroupStatus'
            }),
            'tenant': forms.Select(attrs={
                'class': 'form-select border-dark',
                'id': 'inputGroupTenant'
            }),
            'lease_start': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control border-dark',
                "id": "lease_start_datepicker"
            }),
            'lease_end': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control border-dark',
                "id": "lease_end_datepicker"
            }),
        }

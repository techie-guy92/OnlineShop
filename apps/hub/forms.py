from django import forms 


class CommentForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput(),required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(),required=False)
    comment = forms.CharField(
        label="",
        error_messages={"required":"این فیلد نمیتواند خالی باشد"},
        widget=forms.Textarea(attrs={"class":"form-control","placeholder":"نظر خود را وارد کنید","rows":"4"},
                              )
        )
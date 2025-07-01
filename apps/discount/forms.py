from django import forms 



class DiscountForm(forms.Form):
    discount_code = forms.CharField(label="",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={"class":"form-control","placeholder":"کد تخفیف را وارد کنید"}))
# coding=utf-8
from django import forms


class IcdUploadForm(forms.Form):
    icd_type = forms.ChoiceField(label='ICD工具类型', help_text='目前只有ICDSys', choices=(('ICDSys', 'ICDSys'),),
                                 required=True)
    file = forms.FileField(label='ICD文件', help_text='备注：该文件必须符合ICDSys的格式', required=True)

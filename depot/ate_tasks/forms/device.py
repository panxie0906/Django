# coding=utf-8

from django import forms


class DeviceUploadForm(forms.Form):
    file = forms.FileField(label='资源管理文件', help_text='备注：该文件必须符合device.xml中的格式')

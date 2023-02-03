from django import forms
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        # print(self.fields)
        for field in self.fields:
            
            field_n = self.fields[field]
            
            # TODO - check if is checkbox and reduce the ifs
            # If class exists in field, append and not replace class
            if "class" in field_n.widget.attrs:
                field_n.widget.attrs["class"] += " form-control"
            else:
                field_n.widget.attrs["class"] = "form-control"

            # Check if is type of checkbox and add class "form-check-input"
            
            # Check if the type of fiel is not TinyMCE
            if not isinstance(field_n.widget, TinyMCE):
            
                if field_n.widget.input_type == "checkbox":                    
                    field_n.widget.attrs["class"] = field_n.widget.attrs["class"].replace("form-control", "form-check-input")

                if field_n.widget.input_type == "select":
                    field_n.widget.attrs["class"] += " form-select"
                
                # Append validate class to all fields
                if "validate" in field_n.widget.attrs:
                    if field_n.widget.attrs["validate"] == "telefono_movil":
                        field_n.widget.attrs['pattern'] = "[0]{1}[9]{1}[0-9]{8}"
                        field_n.widget.attrs['validate'] = "Núm. móvil incorrecto. Ejm: 0987654321"
                    elif field_n.widget.attrs["validate"] == "telefono_fijo":
                        field_n.widget.attrs['pattern'] = "[0]{1}[2-8]{1}[0-9]{7}"
                        field_n.widget.attrs['validate'] = "Núm. fijo incorrecto. Ejm: 022345678"
                    elif field_n.widget.attrs["validate"] == "cedula":
                        field_n.widget.attrs['pattern'] = "[0-9]{10}"
                        field_n.widget.attrs['validate'] = "La cédula debe tener 10 dígitos"

            # field_n.widget.attrs.update({'class': 'form-control'})
            if field_n.required:
                field_n.label = mark_safe(field_n.label + '<span class="text-danger">*</span> ')


class ModelBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelBaseForm, self).__init__(*args, **kwargs)

        # print(self.fields)
        for field in self.fields:
            
            field_n = self.fields[field]
            
            # TODO - check if is checkbox and reduce the ifs
            # If class exists in field, append and not replace class
            if "class" in field_n.widget.attrs:
                field_n.widget.attrs["class"] += " form-control"
            else:
                field_n.widget.attrs["class"] = "form-control"

            # Check if is type of checkbox and add class "form-check-input"
            
            # Check if the type of fiel is not TinyMCE
            if not isinstance(field_n.widget, TinyMCE):
            
                if field_n.widget.input_type == "checkbox":                    
                    field_n.widget.attrs["class"] = field_n.widget.attrs["class"].replace("form-control", "form-check-input")

                if field_n.widget.input_type == "select":
                    field_n.widget.attrs["class"] += " form-select"
                
                # Append validate class to all fields
                if "validate" in field_n.widget.attrs:
                    if field_n.widget.attrs["validate"] == "telefono_movil":
                        field_n.widget.attrs['pattern'] = "[0]{1}[9]{1}[0-9]{8}"
                        field_n.widget.attrs['validate'] = "Núm. móvil incorrecto. Ejm: 0987654321"
                    elif field_n.widget.attrs["validate"] == "telefono_fijo":
                        field_n.widget.attrs['pattern'] = "[0]{1}[2-8]{1}[0-9]{7}"
                        field_n.widget.attrs['validate'] = "Núm. fijo incorrecto. Ejm: 022345678"
                    elif field_n.widget.attrs["validate"] == "cedula":
                        field_n.widget.attrs['pattern'] = "[0-9]{10}"
                        field_n.widget.attrs['validate'] = "La cédula debe tener 10 dígitos"

            # field_n.widget.attrs.update({'class': 'form-control'})
            if field_n.required:
                field_n.label = mark_safe(field_n.label + '<span class="text-danger">*</span> ')
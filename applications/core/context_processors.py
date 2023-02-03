from .models import Alerta
from applications.core.models import AplicacionWeb, Alerta

def main_context(request):
    return
    # return {
    #     'alertas': Alerta.objects.filter(activo=True),
    #     'application': AplicacionWeb.objects.first(),
    #     'webpush': {"group": "precavidos"}
    # }
import json

from django.http import JsonResponse, Http404

from django.core.mail import send_mail
from django.conf import settings

import requests
import json
import base64
from django.utils import timezone
import math
from threading import Thread
from django.core.mail import EmailMessage

# from webpush import send_user_notification
# from webpush.models import Group
from threading import Thread
from django.core.management.color import no_style
from django.db import connection

# class UserNotificationThread(Thread):
#     def __init__(self, user, payload, ttl=0):
#         self.user = user
#         self.payload = payload
#         self.ttl = ttl
#         Thread.__init__(self)

#     def run(self):
#         try:
#             send_user_notification(user=self.user, payload=self.payload, ttl=self.ttl)
#         except Exception as e:
#             pass
        

# def send_notification_to_user(user, payload, ttl=0):
#     UserNotificationThread(user, payload, ttl).start()
#     return

# def send_notification_to_group(group_name, payload, ttl=0):

#     push_infos = Group.objects.get(name=group_name).webpush_info.select_related("subscription")
    
#     for push_info in push_infos:
#         print(push_info.subscription)
#         try:
#             send_user_notification(user=push_info.subscription, payload=payload, ttl=ttl)
#             # send_notification_to_user(push_info.subscription, payload, 0)
#         except Exception as e:
#             print("Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             print(push_info.subscription)
#             pass

# class GroupNotificationThread(Thread):
#     def __init__(self, group_name, payload, ttl=0):
#         self.group_name = group_name
#         self.payload = payload
#         self.ttl = ttl
#         Thread.__init__(self)
        
#     def run(self):
#         try:
#             send_notification_to_group(self.group_name, self.payload, self.ttl)
#         except Exception as e:
#             pass
        
# # Create a Thread to send the notification to group
# def send_notification_to_group_thread(group_name, payload, ttl=0):
#     GroupNotificationThread(group_name, payload, ttl).start()
#     return


# Envio de Correos ******************************************************
class EmailThread(Thread):
    def __init__(self, subject, body, to):
        self.subject = subject
        self.body = body
        self.to = to
        Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.body, to=self.to)
        msg.content_subtype = "html"
        msg.send()


def send_mail(subject, body, to):
    EmailThread(subject, body, to).start()

# ***********************************************************************
    

def reset_model(model):
    model.objects.all().delete()
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [model])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)
    return

def null_safe_float_to_int(value):
    if pd.isnull(value):
        return None
    else:
        return int(value)

def null_safe_string(value):
    
    if pd.isnull(value):
        return None
    else:
        return str(value)


def success_json(mensaje=None, resp=None, url=None):

    data = {'result': 'ok'}

    if resp:
        data['resp'] = resp

    if url:
        data['url'] = url
        data['redirected'] = True
    else:
        data['redirected'] = False
        
    if mensaje:
        data['mensaje'] = mensaje

    return JsonResponse(data)

def bad_json(mensaje=None, error=None, extradata=None):
    data = {'result': 'bad'}
    if mensaje:
        data['mensaje'] = mensaje
    if error:
        if error >= 0:
            if error == 0:
                data['mensaje'] = "Solicitud incorrecta"
            elif error == 1:
                data['mensaje'] = "Error al guardar los datos"
            elif error == 2:
                data['mensaje'] = "Error al eliminar los datos"
    if extradata:
        data.update(extradata)
    return JsonResponse(data)

def get_query_params(request):
    action = request.GET.get('action', '')
    data = json.loads(request.body)
    if action == "":
        if action in data:
            action = data['action']
        else:
            action == None            
    return action, data

def get_hace_tiempo(created):
    
    ahora = timezone.now()
    diferencia = ahora - created
    segundos = round(diferencia.total_seconds())
    minutos = math.floor(segundos / 60)
    horas = math.floor(minutos / 60)
    dias = math.floor(horas / 24)
    meses = math.floor(dias / 30)

    if meses == 1:
        return "hace un mes"
    elif meses > 1:
        return f"hace {meses} meses"
    elif dias == 1:
        return f"hace {dias} día"
    elif dias > 0:
        return f"hace {dias} días"
    elif horas == 1:
        return f"hace {horas} hora"
    elif horas > 0:
        return f"hace {horas} horas"
    elif minutos == 1:
        return f"hace {minutos} minuto"
    elif minutos > 0:
        return f"hace {minutos} minutos"
    else:
        return f"hace {segundos} segundos"
    
def get_tiempo_string(tiempo):
    horas = tiempo // 3600
    tiempo = tiempo % 3600
    minutos = tiempo // 60
    tiempo = tiempo % 60
    segundos = tiempo
    
    if horas > 0 and minutos > 0 and segundos > 0:
        return f"{horas} horas {minutos} minutos {segundos} segundos"
    if horas > 0 and minutos > 0 and segundos == 0:
        return f"{horas} horas {minutos} minutos"
    if horas > 0 and minutos == 0 and segundos > 0:
        return f"{horas} horas {segundos} segundos"
    if horas > 0 and minutos == 0 and segundos == 0:
        return f"{horas} horas"
    if horas == 0 and minutos > 0 and segundos > 0:
        return f"{minutos} minutos {segundos} segundos"
    if horas == 0 and minutos > 0 and segundos == 0:
        return f"{minutos} minutos"
    else:
        return f"{segundos} segundos"
    
def get_seconds_to_string(seconds): # Convert seconds to 20:10
    
    if seconds >= 3600:
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{hours}:{minutes}:{seconds}"
    else:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds}"
    
def check_is_superuser(request):
    if request.user.is_superuser:
        return
    else:
        raise Http404("Página no encontrada")

def get_url_params(request):
    url_parameters = request.GET.copy()
    if 'pagina' in url_parameters:
        del url_parameters['pagina']
    return url_parameters.urlencode() 

    bucket = storage.bucket("pre-online.appspot.com")

    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        imagen = img['src']

        if not imagen.startswith('data:image'):
            response = requests.get(imagen)
            if response.status_code == 200:
                blob = bucket.blob("precavidos/" + str(bson.ObjectId()))
                blob.upload_from_string(response.content, content_type=response.headers['content-type'])
                blob.make_public()
                img['src'] = blob.public_url

                if "alt" in img.attrs:
                    img["alt"] = "Banco de preguntas Precavidos"
                else:
                    img["alt"] = "Banco de preguntas Precavidos"

        else :
            # Upload image to firebase storage
            imagen = imagen.replace('data:image/png;base64,', '')
            imagen = imagen.replace('data:image/jpeg;base64,', '')
            imagen = imagen.replace('data:image/jpg;base64,', '')
            imagen = imagen.replace('data:image/gif;base64,', '')
            imagen = imagen.replace('data:image/svg+xml;base64,', '')
            imagen = imagen.replace('data:image/webp;base64,', '')
            imagen = imagen.replace('data:image/bmp;base64,', '')
            imagen = imagen.replace('data:image/tiff;base64,', '')
            imagen = imagen.replace('data:image/vnd.microsoft.icon;base64,', '')
            imagen = imagen.replace('data:image/x-icon;base64,', '')
            imagen = imagen.replace('data:image/vnd.wap.wbmp;base64,', '')
            imagen = imagen.replace('data:image/x-xbitmap;base64,', '')
            imagen = imagen.replace('data:image/x-xbm;base64,', '')
            imagen = imagen.replace('data:image/x-win-bitmap;base64,', '')
            imagen = imagen.replace('data:image/x-windows-bmp;base64,', '')
            imagen = imagen.replace('data:image/x-ms-bmp;base64,', '')
            imagen = imagen.replace('data:image/bmp;base64,', '')
            imagen = imagen.replace('data:image/x-bmp;base64,', '')
            imagen = imagen.replace('data:image/x-bitmap;base64,', '')
            imagen = imagen.replace('data:image/x-xbitmap;base64,', '')
            imagen = imagen.replace('data:image/x-win-bitmap;base64,', '')

            imagen = imagen.encode('utf-8')
            imagen = base64.b64decode(imagen)

            blob = bucket.blob("precavidos/" + str(bson.ObjectId()))
            blob.upload_from_string(imagen, content_type="image/png")
            blob.make_public()
            img['src'] = blob.public_url

            if "alt" in img.attrs:
                img["alt"] = "Banco de preguntas Precavidos"
            else:
                img["alt"] = "Banco de preguntas Precavidos"

    return str(soup)
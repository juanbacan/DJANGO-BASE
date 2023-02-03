from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# Create your models here.

import datetime

class CustomUser(AbstractUser):
    uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    premium = models.BooleanField(default=False)
    
    def get_photo_user(self):
        
        if self.socialaccount_set.exists():
            social_account = self.socialaccount_set.first()
            return social_account.get_avatar_url()
        else:
            return None

CustomUser._meta.get_field('email').blank = True
CustomUser._meta.get_field('email').null = True

import inspect
class ModeloBase(models.Model):
    """
    Clase base para todos los modelos de la aplicación.
    """
    created_by = models.ForeignKey(CustomUser, related_name='%(class)s_created', editable=False, on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(CustomUser, related_name='%(class)s_modified', editable=False, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    # created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.created is None:
            self.created = datetime.datetime.now()

        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request = None

        user_id = request.user.id if request else 1
        
        if not self.pk and not self.created_by:
            self.created_by_id = user_id
        self.modified_by_id = user_id
        super(ModeloBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % self.id
    
        
class AplicacionWeb(ModeloBase):
    favicon = models.ImageField(upload_to='aplicacion_web', null=True, blank=True)
    logo = models.ImageField(upload_to='aplicacion_web', null=True, blank=True)
    logo_webpush = models.ImageField(upload_to='aplicacion_web', null=True, blank=True)
    image_content = models.ImageField(upload_to='aplicacion_web', null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    meta_title = models.CharField(max_length=300, null=True, blank=True)
    meta_description = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Aplicación Web'
        verbose_name_plural = 'Aplicación Web'
        

class Alerta(ModeloBase):
    titulo = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True, max_length=200, verbose_name=u'URL')
    boton = models.CharField(max_length=100, null=True, blank=True)
    orden = models.IntegerField(default=1)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
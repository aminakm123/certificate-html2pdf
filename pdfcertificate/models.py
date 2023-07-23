from django.db import models
from django.utils.translation import gettext_lazy as _


class Certificate(models.Model):
    verification_code = models.CharField(max_length=100,unique=True,primary_key=True)
    name = models.CharField(max_length=100)
    subtitle = models.TextField()
    custom_content = models.TextField(null=True,blank=True)
    date = models.DateField()
    sign = models.CharField(max_length=100)    

    class Meta:
        db_table = ('certificate_certificate')
        verbose_name = _('certificate')
        verbose_name_plural = _('certificates')

    def __str__(self):
        return str(self.verification_code)


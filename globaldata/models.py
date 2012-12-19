from django.db import models

# Create your models here.
class GlobalData(models.Model):
    name = models.CharField(max_length=30)
    stage = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return self.name

    def getDataDict(self):
        return {
                'id': self.id,
                'name': self.name,
                'stage': self.stage,
                }

from django.db import models


class RoleTemplate(models.Model):
    name = models.CharField(max_length=100)
    main = models.TextField()

    class Meta:
        ordering = ("name", )


class Tasks(models.Model):
    name = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    content = models.TextField()


    class Meta:
        ordering = ("name", )
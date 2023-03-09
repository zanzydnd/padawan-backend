from django.db import models


class Orderable(models.Model):
    order = models.PositiveIntegerField(blank=True, null=True, editable=True, )

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.order:
            max = self.__class__.objects.all().aggregate(models.Max("order"))
            try:
                self.order = max["order__max"] + 1
            except TypeError:
                self.order = 1
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
        ordering = ('order',)

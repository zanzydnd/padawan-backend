from django.db import models


# Create your models here.
class Schema(models.Model):
    pass


class SchemaField(models.Model):
    """
        number	–	Any numbers.
        number	float	Floating-point numbers.
        number	double	Floating-point numbers with double precision.
        integer	–	Integer numbers.
        integer	int32	Signed 32-bit integers (commonly used integer type).
        integer	int64	Signed 64-bit integers (long type).
    """

    class DataType(models.TextChoices):
        string = "string", "string"
        number = "number", "number"
        integer = "integer", "integer"
        boolean = "boolean", "boolean"
        array = "array", "array"
        object = "object", "object"

    data_type = models.CharField(max_length=255, choices=DataType.choices, default=DataType.string)
    value = models.TextField()
    description = models.TextField()
    nullable = models.BooleanField(default=False)
    pattern = models.CharField(max_length=255, null=True, blank=True)


class Step(models.Model):
    request = models.JSONField(null=True, blank=True)

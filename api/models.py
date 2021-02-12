from django.db import models

# Create your models here.




class StateChices(models.TextChoices):
    TRUE = "True", "True"
    FALSE = "False", "False"
    DELETED = "Deleted", "Deleted"


class TestModelApi(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)

    value = models.TextField(blank=False, null=False)

    # default
    state = models.CharField(
        max_length=16, choices=StateChices.choices, default=StateChices.TRUE
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = "test_tabel_api"

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    def clean(self):
        super().clean()

    def str(self):
        return str(self.id)

    @staticmethod
    def protected():
        return ["updated_at", "created_at", "state"]


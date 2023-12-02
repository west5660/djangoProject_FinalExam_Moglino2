from django.contrib.auth.models import User
from django.db import models



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    production_type = models.CharField(max_length=255, blank=True, null=True)
    project_status = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Переопределяем метод save для сохранения organization_name в first_name
        self.user.first_name = self.organization_name
        self.user.save()
        super().save(*args, **kwargs)


class ServiceType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    unit_of_measurement = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_services')

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_processed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Пересчитываем общую сумму при сохранении заказа
        self.total_cost = self.quantity * self.service.cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.service.title}"


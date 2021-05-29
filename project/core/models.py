from django.db import models


class Thing(models.Model):
    """Модель предмета"""
    name = models.CharField("Название предмета", max_length=64)


class Master(models.Model):
    """Модель мастера"""
    name = models.CharField("Имя мастера", max_length=64)
    surname = models.CharField("Фамилия мастера", max_length=64)
    birthday = models.DateField("Дата рождения")
    residence_address = models.CharField("Место проживания", max_length=64)
    birthday_address = models.CharField("Место рождения", max_length=64)
    repairs_thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    work_price = models.DecimalField("Стоимость ремонта", max_digits=20, decimal_places=1)


class Order(models.Model):
    """Модель заказа"""
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    num_of_things = models.PositiveIntegerField("Количество ремонтируемой техники")
    price = models.DecimalField("Цена заказа", max_digits=20, decimal_places=1)
    order_date = models.DateField("Дата заказа")

    def save(self, *args, **kwargs):
        self.price = self.master.work_price * self.num_of_things
        super(Order, self).save(*args, **kwargs)

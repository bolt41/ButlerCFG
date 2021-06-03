from django.db import models


# Модель уровней [стартовый, нормальный, супер]
class Levels(models.Model):
    name = models.CharField('Наименование', max_length=20)

    class Meta:
        unique_together = ['name']
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель наименования локаций (этажность)
class Floor(models.Model):
    name = models.CharField('Тип этажа', max_length=50)

    class Meta:
        unique_together = ['name']
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель перечня помещений (перечень помещений]
class Rooms(models.Model):
    name = models.CharField('Название помещения', max_length=50)

    class Meta:
        unique_together = ['name']
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель перечня подсистем
class Systems(models.Model):
    name = models.CharField('Название подсистемы', max_length=100)
    icon = models.CharField('Иконка fontawesome', max_length=50, blank=True)
    is_visible = models.BooleanField('Видимость в меню')
    public_text = models.CharField('В печатной форме', max_length=300, blank=True)

    class Meta:
        unique_together = ['name']
        verbose_name = 'Подсистема'
        verbose_name_plural = 'Подсистемы'
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель перечня параметров
class Params(models.Model):
    name = models.CharField('Название параметра', max_length=100)
    system = models.ForeignKey(Systems, verbose_name='Подсистема', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'system']
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        ordering = ['system']

    def __str__(self):
        return self.name
        #return f"{self.name} - {self.system.name}"


# Модель шаблонов
class Templates(models.Model):
    room = models.ForeignKey(Rooms, verbose_name='Помещение', on_delete=models.CASCADE)
    param = models.ForeignKey(Params, verbose_name='Параметр', on_delete=models.CASCADE)
    count = models.PositiveIntegerField('Количество')

    class Meta:
        unique_together = ['room', 'param']
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['room']

    def __str__(self):
        return f"{self.room} - {self.param.system} - {self.param} - Количество: {self.count}"

    def get_system(self):  # функция получения подсистемы к которой относится шаблон
        return self.param.system

    get_system.short_description = "Подсистема"


# Модель перечня брендов поставщиков
class Vendors(models.Model):
    name = models.CharField('Вендор', max_length=50)

    class Meta:
        verbose_name = 'Вендор'
        verbose_name_plural = 'Вендоры'
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель оборудования
class Devices(models.Model):
    vendor = models.ForeignKey('Vendors', verbose_name='Бренд', on_delete=models.CASCADE)
    model = models.CharField('Модель', max_length=200, blank=True)
    caption = models.CharField('Номенклатура', max_length=200)
    level = models.ManyToManyField('Levels', verbose_name='Уровень')
    count = models.PositiveIntegerField('Кол-во вх/вых', blank=True, default=0)
    system = models.ForeignKey('Systems', verbose_name='Подсистема', null=True, on_delete=models.SET_NULL)
    param = models.ForeignKey('Params',verbose_name='Связаный параметр', null = True, blank = True, default=None, on_delete=models.SET_NULL)
    is_main = models.BooleanField('Базовый элемент подсистемы', default=False)
    price = models.FloatField('Цена', blank=True, null = True)

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Оборудование'

    def __str__(self):
        return f"{self.vendor.name},{self.model}"

    # Функция возвращает перечень систем в которых может использоваться устройство
    def get_levels(self):
        return ", ".join([p.name for p in self.level.all()])

    # Для отображения в админке поля с "человеческим" названием
    get_levels.short_description = "Уровни"

class Constant(models.Model): # таблица констант (будущее расширение)
    name = models.CharField('Наименование', max_length=200)
    caption = models.CharField('Описание', max_length=400)
    value = models.IntegerField('Значение', blank=True, null=True)

    class Meta:
        verbose_name = 'Константа'
        verbose_name_plural = 'Константы'

    def __str__(self):
        return self.name
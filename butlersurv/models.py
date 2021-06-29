from django.db import models
from django.utils.safestring import mark_safe


class SystemSurv(models.Model):
    name = models.CharField('Наименование', max_length=100)
    is_use = models.BooleanField('Использовать в опросах', default=True)

    class Meta:
        unique_together = ['name']
        verbose_name = 'Подсистема'
        verbose_name_plural = 'Подсистемы'
        ordering = ['name']

    def __str__(self):
        return self.name


class PartitionSurv(models.Model):
    name = models.CharField('Наименование', max_length=100)
    is_use = models.BooleanField('Использовать в опросах', default=True)
    type = models.ForeignKey(SystemSurv, verbose_name='Подсистема', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class QuestionSurv(models.Model):
    partition = models.ForeignKey(PartitionSurv, verbose_name='Связаный раздел', on_delete=models.CASCADE)
    question = models.CharField('Наименование', max_length=600)
    is_use = models.BooleanField('Использовать в опросах', default=True)

    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметр'

    def __str__(self):
        return self.question

    def get_variable(self):
        return mark_safe(';<br>'.join([p.variable for p in self.answersurv_set.all()]))

    get_variable.short_description = "Варианты выбора"

class AnswerSurv(models.Model):
    question = models.ForeignKey(QuestionSurv, verbose_name='Связаный вопрос', null=True, on_delete=models.CASCADE)
    variable = models.CharField('Вариант выбора', max_length=600)
    is_use = models.BooleanField('Использовать в опросах', default=True)

    class Meta:
        verbose_name = 'Вариант выбора'
        verbose_name_plural = 'Варианты выбора'

    def __str__(self):
        return self.variable

    def get_partition(self):
        return self.question.partition

    get_partition.short_description = "Подсистема"
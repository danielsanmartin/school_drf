from django.db import models


class Base(models.Model):
    created_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Course(Base):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Evaluation(Base):
    course = models.ForeignKey(Course, related_name='evaluations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField(blank=True, default='')
    evaluation = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        unique_together = ['email', 'course']
        ordering = ['id']

    def __str__(self):
        return f'{self.name} evaluated the course {self.course} with note {self.evaluation}'

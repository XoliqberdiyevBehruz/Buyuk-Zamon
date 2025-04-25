from django.db import models

from account.models import BaseModel, Student

class Course(BaseModel):
    name = models.CharField(max_length=70)
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.name} - {self.price}'
    

class Payment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    paid = models.PositiveBigIntegerField()
    debt = models.PositiveBigIntegerField()
    is_debt = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} - {self.course} - {self.paid}'
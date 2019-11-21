import jsonfield

from django.db import models

class User_Registration(models.Model):
    Username = models.CharField(max_length=100, unique=True)
    Name = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=50)
    Age = models.IntegerField()
    DOB = models.DateField()
    Gender = models.CharField(max_length=10)
    Address = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}'.format(self.Username, self.Name, self.Email, self.Password, self.Age,
                                                       self.DOB, self.Gender, self.Address)

    class Meta:
        db_table = 'user'

class Category(models.Model):
    Name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'category'

class SubCategory(models.Model):
    product_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)

    def __str__(self):
        return '{}, {}'.format(self.product_category, self.Name)

    class Meta:
        db_table = 'sub_category'

class Product(models.Model):
    product_subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    features = jsonfield.JSONField()

    def __str__(self):
        return '{}, {}'.format(self.product_subcategory, self.Name, self.model, self.features)

    class Meta:
        db_table = 'product'
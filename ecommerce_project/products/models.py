from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=500)
    active = models.BooleanField(default=False)
    max_per_order = models.IntegerField(default=3)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.id}-{self.name}'


class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    image = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.id}-{self.name}'

class ProductCategory(models.Model):
    product_id = models.ManyToManyField(Product)
    category_id = models.ManyToManyField(Category)# We can delete a category, check this relation ship. It should be something like delete on cascade kild of thing


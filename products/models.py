from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    # feature_image = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace(" ", "-"))
        super().save(*args, **kwargs)

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='sub_categories')
    status = models.BooleanField(default=True)

    # feature_image = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace(" ", "-"))
        super().save(*args, **kwargs)

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='brand')
    status = models.BooleanField(default=True)

    # feature_image = models.CharField(max_length=255)


    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.SET_NULL)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    # images = models.ManyToManyField('ProductImage', related_name='products')

    def __str__(self):
        return f"{self.name} - {self.quantity}"

class ProductImage(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # image = models.ImageField(upload_to='product_images/')
    pass

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    feature = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.product} - ({self.title}, {self.feature})"
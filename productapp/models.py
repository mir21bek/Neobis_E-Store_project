from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название категория', max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    product_name = models.CharField(verbose_name='Название товара', max_length=255)
    product_description = models.TextField(verbose_name='Описание', max_length=1000)
    product_price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)
    product_image = models.ImageField(verbose_name='Фото товара',
                                      upload_to='product_images/',
                                      default='product_images/download.png')
    available = models.BooleanField(verbose_name='В наличии?', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукции'

    def __str__(self):
        return self.product_name


class SaleProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    sale = models.BooleanField(verbose_name='скидка на товар', default=False)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.sale

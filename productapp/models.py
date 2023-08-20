from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(verbose_name='Название категория', max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

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
                                      upload_to='media/product_images/',
                                      default='product_images/download.png')
    available = models.BooleanField(verbose_name='В наличии?', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def discounted_price(self):
        sale_product = self.saleproduct_set.filter(sale=True).first()
        if sale_product:
            sale_percentage = sale_product.sale_percentage
            return float(self.product_price) * (1 - float(sale_percentage) / 100)
        return self.product_price

    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукции'

    def __str__(self):
        return self.product_name


class SaleProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.BooleanField(verbose_name='скидка на товар', default=False)
    sale_percentage = models.DecimalField(verbose_name='Процент скидки',
                                          max_digits=5,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f"Rating {self.rating}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

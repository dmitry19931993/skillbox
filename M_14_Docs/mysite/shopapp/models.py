from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

def products_preview_directory_path(instance: "Product", filename : str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        # db_table = "tech_products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    preview = models.ImageField(null=True, blank=True, upload_to=products_preview_directory_path)

    # @property
    # def description_short(self):
    #     if len(self.description) < 50:
    #         return self.description
    #     return self.description[:48] + "..."

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

def products_images_directory_path(instance: "ImageProduct", filename : str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )

class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=products_images_directory_path)
    description = models.CharField(max_length=50, null=False, blank=True)

class Order(models.Model):
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to="orders/receipt/")
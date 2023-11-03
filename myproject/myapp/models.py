from enum import Enum

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CategoryEnum(Enum):
    HOT = "Горячее"
    COLD = "Холодное"
    SNACK = "Закуска"
    DESERT = "Десерт"


CATEGORY_CHOICE = (
    (CategoryEnum.HOT.value, "Горячее"),
    (CategoryEnum.COLD.value, "Холодное"),
    (CategoryEnum.SNACK.value, "Закуска"),
    (CategoryEnum.DESERT.value, "Десерт"),
)


class Category(models.Model):
    name = models.CharField(
        verbose_name="Название категории", max_length=50, choices=CATEGORY_CHOICE
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Recipe(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    description = models.CharField(verbose_name="Описание", max_length=500)
    steps = models.CharField(verbose_name="Этапы приготовления", max_length=500)
    coocking_time = models.IntegerField(verbose_name="Время приготовления, мин")
    image = models.ImageField(verbose_name="Фото блюда", upload_to="images/")
    create_at = models.DateTimeField(verbose_name="Время приготовления", auto_now=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    # def get_absolute_url(self):
    #     return reverse('blog:category_page', args=[int(self.pk), str(self.slug)])

    # def __str__(self):
    #     return self.title


class CoockingItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

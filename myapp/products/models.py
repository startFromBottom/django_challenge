from django.db import models


class OtherCharException(Exception):
    pass


class SkinTypes:
    OILY = "oily"
    SENSITIVE = "sensitive"
    DRY = "dry"


class Ingredient(models.Model):

    """ Cosmetic Ingredients Model Definition """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    oily = models.CharField(max_length=1)
    dry = models.CharField(max_length=1)
    sensitive = models.CharField(max_length=1)

    def __str__(self):
        return self.name


class Product(models.Model):

    """ Cosmectic Produdcts Model Definition """

    CATEGORY_SKIN = "skincare"
    CATEGORY_MASK = "maskpack"
    CATEGORY_SUN = "suncare"
    CATEGORY_BASE = "baskemakeup"

    CATEGORY_CHOICES = (
        (CATEGORY_SKIN, "Skin care"),
        (CATEGORY_MASK, "Mask pack"),
        (CATEGORY_SUN, "Sun care"),
        (CATEGORY_BASE, "Base makeup"),
    )

    id = models.IntegerField(primary_key=True)
    imageId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    gender = models.CharField(max_length=6)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=11, default=CATEGORY_SKIN
    )
    ingredients = models.ManyToManyField("Ingredient", related_name="products",)
    monthlySales = models.IntegerField()

    def imgUrl(self):
        """
        imageId to url
        """
        folder = "thumbnail"
        base_url = f"https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/{folder}/"

        return base_url + self.imageId

    def ingredient_str(self):
        """
        convert id's list to string
        ex)
        ingredients : [220,241,262,765,820,821,896,911]
        to
        ingredients : "resignation,goalkeeper,relinquish,calf,runner,tumour,planet,morale"
    
        """
        names = [ingredient.name for ingredient in self.ingredients.all()]
        return ",".join(names)

    def calculate_score(self, skin_type):
        """
        calculate oily score of product
        by adding each score of ingredient
        """
        score = 0
        if skin_type not in (SkinTypes.OILY, SkinTypes.SENSITIVE, SkinTypes.DRY):
            raise OtherCharException("skin type must be one of oily, sensitive, dry")
        for ingredient in self.ingredients.all():
            if skin_type == SkinTypes.OILY:
                score += Product.convert_char_to_score(ingredient.oily)
            elif skin_type == SkinTypes.SENSITIVE:
                score += Product.convert_char_to_score(ingredient.sensitive)
            else:  # SkinTypes.DRY
                score += Product.convert_char_to_score(ingredient.dry)

        return score

    @staticmethod
    def convert_char_to_score(char):
        """
        유익함("O") -> +1
        영향없음("") -> +0
        유해함("X") -> -1
        """
        if char == "O":
            return 1
        elif char == "X":
            return -1
        elif char == "":
            return 0
        else:
            raise OtherCharException("Invalid Character")

    def __str__(self):
        return self.name


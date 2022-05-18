from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        if not self.parent:
            return f'{self.name}'
        else:
            return f'{self.parent} --> {self.name}'


class Location(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self): return self.name


class Worker_card(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13)
    profil = models.ImageField(upload_to='images/', blank=True)
    owner = models.ForeignKey('auth.User', related_name='card', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='card')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.owner} - {self.first_name} {self.last_name}'


class Worker_cardImages(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    card = models.ForeignKey(Worker_card, on_delete=models.CASCADE, related_name='card')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    @staticmethod
    def generate_name():
        import random
        return 'image' + str(random.randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(Worker_cardImages, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title} -> {self.card.id}'


class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    card = models.ForeignKey(Worker_card, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} -> {self.card} -> {self.created_at}'


class Likes(models.Model):
    card = models.ForeignKey(Worker_card, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['card', 'user']
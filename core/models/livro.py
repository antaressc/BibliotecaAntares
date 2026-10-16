from django.db import models
from .categoria import Categoria
from .editora import Editora
from .autor import Autor
from uploader.models import Image

class Livro(models.Model):

    capa = models.ForeignKey(
        Image,
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    class Status(models.TextChoices):
        DISPONIVEL = 'disponivel', 'Disponível'
        RESERVADO = 'reservado', 'Reservado'

    titulo = models.CharField(max_length=255)
    isbn = models.CharField(max_length=32, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DISPONIVEL)
    sinopse = models.TextField(
        blank=True,
        null=True,
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='livros', null=True, blank=True)
    editora = models.ForeignKey(Editora, on_delete=models.PROTECT, related_name='livros', null=True, blank=True)
    autores = models.ManyToManyField(Autor, related_name='livros', blank=True)

    class Formato(models.TextChoices):
        LIVRO = 'Livro', 'livro'
        REVISTA = 'Revista', 'revista'
        APOSTILA = 'Apostila', 'apostila'
        MANUAL = 'Manual', 'manual'
        NORMA_TECNICA = 'norma_tecnica', 'Norma técnica'

    formato = models.CharField(
        max_length=20,
        choices=Formato.choices,
        default=Formato.LIVRO,
        verbose_name='Formato'
    )

    def __str__(self):
        return f'{self.titulo}'
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    IntegerField,
    SerializerMethodField,
)

from core.models import Livro, Reserva
from uploader.models import Image
from uploader.serializers import ImageSerializer



class LivroSerializer(ModelSerializer):

    capa_attachment_key = SlugRelatedField(
        source='capa',
        queryset=Image.objects.all(),
        slug_field='attachment_key',
        required=False,
        write_only=True,
    )

    capa = ImageSerializer(
        required=False,
        read_only=True,
    )

    class Meta:
        model = Livro
        fields = '__all__'

    @staticmethod
    def normalizar(valor):
        return ' '.join(
            str(valor or '').strip().casefold().split()
        )

    @staticmethod
    def normalizar_isbn(valor):
        return ''.join(
            caractere
            for caractere in str(valor or '').casefold()
            if caractere.isalnum()
        )

    def validate(self, attrs):
        titulo = attrs.get(
            'titulo',
            self.instance.titulo if self.instance else '',
        )

        isbn = attrs.get(
            'isbn',
            self.instance.isbn if self.instance else '',
        )

        if 'autores' in attrs:
            autores = list(attrs['autores'])
        elif self.instance:
            autores = list(self.instance.autores.all())
        else:
            autores = []

        if 'categoria' in attrs:
            categoria = attrs['categoria']
        elif self.instance:
            categoria = self.instance.categoria
        else:
            categoria = None

        isbn_normalizado = self.normalizar_isbn(isbn)

        livros = Livro.objects.all().select_related(
            'categoria',
        ).prefetch_related('autores')

        if self.instance:
            livros = livros.exclude(pk=self.instance.pk)

        if isbn_normalizado:
            for existente in livros:
                if (
                    self.normalizar_isbn(existente.isbn)
                    == isbn_normalizado
                ):
                    raise serializers.ValidationError({
                        'isbn': [
                            'Já existe um livro cadastrado com este ISBN.'
                        ],
                    })

        titulo_normalizado = self.normalizar(titulo)

        autores_normalizados = sorted(
            self.normalizar(autor.nome)
            for autor in autores
        )

        categoria_normalizada = (
            self.normalizar(categoria.descricao)
            if categoria else ''
        )

        if titulo_normalizado:
            for existente in livros:
                if (
                    self.normalizar(existente.titulo)
                    != titulo_normalizado
                ):
                    continue

                autores_existentes = sorted(
                    self.normalizar(autor.nome)
                    for autor in existente.autores.all()
                )

                categoria_existente = (
                    self.normalizar(existente.categoria.descricao)
                    if existente.categoria else ''
                )

                if (
                    autores_existentes == autores_normalizados
                    and categoria_existente == categoria_normalizada
                ):
                    raise serializers.ValidationError({
                        'titulo': [
                            'Já existe um livro com o mesmo título, '
                            'autores e categoria.'
                        ],
                    })

        return attrs

class LivroRetrieveSerializer(ModelSerializer):

    capa = ImageSerializer(required=False)

    class Meta:
        model = Livro
        fields = '__all__'
        depth = 1



class LivroListSerializer(ModelSerializer):

    capa = ImageSerializer(
        required=False,
        read_only=True
    )

    data_devolucao_prevista = SerializerMethodField()

    class Meta:
        model = Livro
        fields = (
            'id',
            'titulo',
            'quantidade',
            'capa',
            'status',
            'sinopse',
            'data_devolucao_prevista',
        )

    def get_data_devolucao_prevista(self, obj):
        reserva = Reserva.objects.filter(
            itens__livro=obj,
            status__in=[
                Reserva.StatusReserva.RETIRADO,
            ],
            data_devolucao_prevista__isnull=False,
        ).order_by(
            'data_devolucao_prevista'
        ).first()

        if reserva:
            return reserva.data_devolucao_prevista

        return None



class LivroMaisReservadoSerializer(ModelSerializer):

    total_reservas = IntegerField()

    class Meta:
        model = Livro
        fields = (
            'id',
            'titulo',
            'total_reservas',
        )
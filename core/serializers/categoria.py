from rest_framework import serializers
from core.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

    def validate_descricao(self, value):
        descricao_normalizada = ' '.join(value.split()).casefold()

        categorias = Categoria.objects.all()

        if self.instance:
            categorias = categorias.exclude(pk=self.instance.pk)

        for categoria in categorias.only('id', 'descricao'):
            descricao_existente = ' '.join(
                categoria.descricao.split()
            ).casefold()

            if descricao_existente == descricao_normalizada:
                raise serializers.ValidationError(
                    'Já existe uma categoria cadastrada com essa descrição.'
                )

        return ' '.join(value.split())
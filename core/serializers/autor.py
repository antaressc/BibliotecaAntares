from rest_framework import serializers
from core.models import Autor

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

    def validate_nome(self, value):
        nome_normalizado = ' '.join(value.split()).casefold()

        autores = Autor.objects.all()

        if self.instance:
            autores = autores.exclude(pk=self.instance.pk)

        for autor in autores.only('id', 'nome'):
            nome_existente = ' '.join(autor.nome.split()).casefold()

            if nome_existente == nome_normalizado:
                raise serializers.ValidationError(
                    'Já existe um autor cadastrado com esse nome.'
                )

        return ' '.join(value.split())

from rest_framework import serializers
from core.models import Editora

class EditoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

    def validate_nome(self, value):
        nome_normalizado = ' '.join(value.split()).casefold()

        editoras = Editora.objects.all()

        if self.instance:
            editoras = editoras.exclude(pk=self.instance.pk)

        for editora in editoras.only('id', 'nome'):
            nome_existente = ' '.join(editora.nome.split()).casefold()

            if nome_existente == nome_normalizado:
                raise serializers.ValidationError(
                    'Já existe uma editora cadastrada com esse nome.'
                )

        return ' '.join(value.split())

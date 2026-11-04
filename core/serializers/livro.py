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
        read_only=True
    )

    class Meta:
        model = Livro
        fields = '__all__'


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
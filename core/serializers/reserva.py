from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    CurrentUserDefault,
    HiddenField,
    ValidationError,
)
from core.models import Reserva, ItensReserva, Livro
from django.db import transaction

class ItensReservaSerializer(ModelSerializer):
    class Meta:
        model = ItensReserva
        fields = ('livro',)


class ReservaSerializer(ModelSerializer):
    usuario = CharField(source='usuario.name', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensReservaSerializer(many=True, read_only=True)

    class Meta:
        model = Reserva
        fields = (
            'id',
            'usuario',
            'status',
            'data_criacao',
            'data_atualizacao',
            'itens',
        )


class ItensReservaCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensReserva
        fields = ('livro',)

class ReservaCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensReservaCreateUpdateSerializer(many=True)

    class Meta:
        model = Reserva
        fields = ('id', 'usuario', 'itens')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens', [])
        usuario = validated_data['usuario']
    
        reserva_ativa = Reserva.objects.filter(
            usuario=usuario,
            status__in=[
                Reserva.StatusReserva.RESERVADO,
                Reserva.StatusReserva.RETIRADO,
            ]
        ).exists()
    
        if reserva_ativa:
            raise ValidationError(
                'O usuário já possui uma reserva ativa. '
                'É necessário devolver o livro antes de fazer uma nova reserva.'
            )
    
        for item in itens:
            livro = item['livro']
    
            if livro.quantidade <= 0:
                raise ValidationError(
                    f'O livro "{livro.titulo}" não está disponível para reserva.'
                )
    
        reserva = Reserva.objects.create(**validated_data)
    
        for item in itens:
            ItensReserva.objects.create(
                reserva=reserva,
                livro=item['livro']
            )
    
        return reserva

    @transaction.atomic
    def update(self, reserva, validated_data):
        itens = validated_data.pop('itens', [])

        if itens:
            reserva.itens.all().delete()

            for item in itens:
                ItensReserva.objects.create(
                    reserva=reserva,
                    **item
                )

        return super().update(reserva, validated_data)

class ItensReservaListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensReserva
        fields = ('livro',)


class ReservaListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.name', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensReservaListSerializer(many=True, read_only=True)

    class Meta:
        model = Reserva
        fields = (
            'id',
            'usuario',
            'itens',
            'data_criacao',
            'status',
            'data_retirada',
            'data_devolucao_prevista',
            'data_devolucao',
        )
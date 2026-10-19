
from django.db import models, transaction
from .livro import Livro
from .user import User

class Reserva(models.Model):

    class StatusReserva(models.IntegerChoices):

        RESERVADO = 1, 'Reservado'
        RETIRADO = 2, 'Retirado'
        DEVOLVIDO = 3, 'Devolvido'
        CANCELADO = 4, 'Cancelado'

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    status = models.IntegerField(
        choices=StatusReserva.choices,
        default=StatusReserva.RESERVADO
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    data_retirada = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de retirada'
    )

    data_devolucao_prevista = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data prevista de devolução'
    )

    data_devolucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de devolução'
    )

    @transaction.atomic
    def delete(self, *args, **kwargs):
        for item in self.itens.all():
            item.delete()

        return super().delete(*args, **kwargs)



class ItensReserva(models.Model):

    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    livro = models.ForeignKey(
        Livro,
        on_delete=models.PROTECT,
        related_name='itens_reserva'
    )

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.reserva.status in [
                Reserva.StatusReserva.DEVOLVIDO,
                Reserva.StatusReserva.CANCELADO
            ]:
                raise ValueError(
                    'Não é possível adicionar itens a uma reserva '
                    'devolvida ou cancelada.'
                )

            livro = Livro.objects.select_for_update().get(
                pk=self.livro_id
            )

            if livro.quantidade <= 0:
                raise ValueError(
                    f'O livro "{livro.titulo}" não possui '
                    'quantidade disponível.'
                )

            livro.quantidade -= 1

            if livro.quantidade == 0:
                livro.status = Livro.Status.RESERVADO
            else:
                livro.status = Livro.Status.DISPONIVEL

            livro.save(
                update_fields=['quantidade', 'status']
            )

        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.reserva.status not in [
            Reserva.StatusReserva.DEVOLVIDO,
            Reserva.StatusReserva.CANCELADO
        ]:
            livro = Livro.objects.select_for_update().get(
                pk=self.livro_id
            )

            livro.quantidade += 1
            livro.status = Livro.Status.DISPONIVEL

            livro.save(
                update_fields=['quantidade', 'status']
            )

        return super().delete(*args, **kwargs)
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from core.models import Reserva, Livro
from core.services import enviar_email_cancelamento

def adicionar_dias_uteis(data_inicio, quantidade):
    """Avança dias úteis, contando de segunda a sexta, sem feriados."""
    data = data_inicio
    dias_contados = 0

    while dias_contados < quantidade:
        data += timedelta(days=1)

        if data.weekday() < 5:
            dias_contados += 1

    return data

class Command(BaseCommand):
    help = (
        "Cancela reservas não retiradas após três dias úteis "
        "e devolve os exemplares ao estoque."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Apenas lista as reservas elegíveis, sem alterar dados.",
        )

    def handle(self, *args, **options):
        hoje = timezone.localdate()
        simular = options["dry_run"]

        reservas = Reserva.objects.filter(
            status=Reserva.StatusReserva.RESERVADO
        ).order_by("data_criacao")

        elegiveis = []

        for reserva in reservas.iterator():
            data_criacao = timezone.localtime(
                reserva.data_criacao
            ).date()

            #aqui é definida a data limite para cancelamento
            data_limite = adicionar_dias_uteis(data_criacao, 3)

            if hoje >= data_limite:
                elegiveis.append((reserva.pk, data_criacao, data_limite))

        if not elegiveis:
            self.stdout.write("Nenhuma reserva vencida encontrada.")
            return

        self.stdout.write(
            f"{len(elegiveis)} reserva(s) elegível(is) para cancelamento."
        )

        for reserva_id, data_criacao, data_limite in elegiveis:
            self.stdout.write(
                f"Reserva #{reserva_id} | "
                f"criada em {data_criacao} | "
                f"vencimento: {data_limite}"
            )

        if simular:
            self.stdout.write(
                self.style.WARNING(
                    "SIMULAÇÃO: nenhuma alteração foi realizada."
                )
            )
            return

        
        canceladas = 0

        for reserva_id, _, _ in elegiveis:
            with transaction.atomic():
                try:
                    reserva = (
                        Reserva.objects.select_for_update()
                        .get(pk=reserva_id)
                    )
                except Reserva.DoesNotExist:
                    continue

                # Confirma novamente o status antes de alterar o estoque.
                if reserva.status != Reserva.StatusReserva.RESERVADO:
                    continue

                itens = list(
                    reserva.itens.select_related("livro").all()
                )

                for item in itens:
                    livro = Livro.objects.select_for_update().get(
                        pk=item.livro_id
                    )
                    livro.quantidade += 1
                    livro.status = Livro.Status.DISPONIVEL
                    livro.save(update_fields=["quantidade", "status"])

                reserva.status = Reserva.StatusReserva.CANCELADO
                reserva.save(update_fields=["status"])
                canceladas += 1

                # Envia o e-mail somente após confirmar a transação.
                transaction.on_commit(
                    lambda reserva_id=reserva.pk:
                        enviar_email_cancelamento(reserva_id)
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"{canceladas} reserva(s) cancelada(s) com sucesso."
            )
        )
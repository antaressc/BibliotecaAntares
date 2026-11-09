from django.core.management.base import BaseCommand, CommandError

from core.models import Livro
from core.services import enviar_email_livro_novo


class Command(BaseCommand):
    help = "Envia e-mail sobre um novo livro para os usuários elegíveis."

    def add_arguments(self, parser):
        parser.add_argument(
            "livro_id",
            type=int,
            help="ID do livro que será divulgado.",
        )

        parser.add_argument(
            "--email",
            type=str,
            help="Envia somente para este e-mail.",
        )

    def handle(self, *args, **options):
        livro_id = options["livro_id"]
        email_teste = options.get("email")

        if not Livro.objects.filter(pk=livro_id).exists():
            raise CommandError(
                f"Livro com ID {livro_id} não encontrado."
            )

        resultado = enviar_email_livro_novo(
            livro_id,
            email_teste=email_teste,
        )

        if resultado["total"] == 0:
            self.stdout.write(
                self.style.WARNING(
                    "Nenhum usuário elegível possui e-mail cadastrado."
                )
            )
            return

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"Total de usuários elegíveis: "
                f"{resultado['total']}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"E-mails enviados: "
                f"{resultado['enviados']}"
            )
        )

        if resultado["falhas"]:
            self.stdout.write(
                self.style.ERROR(
                    f"E-mails com falha: "
                    f"{resultado['falhas']}"
                )
            )
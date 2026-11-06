from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from core.models import Livro


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

        try:
            livro = Livro.objects.select_related(
                "categoria",
                "editora",
            ).get(pk=livro_id)
        except Livro.DoesNotExist:
            raise CommandError(
                f"Livro com ID {livro_id} não encontrado."
            )

        User = get_user_model()

        usuarios = (
            User.objects
            .filter(
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            .exclude(
                email__isnull=True,
            )
            .exclude(
                email="",
            )
        )

        if email_teste:
            usuarios = usuarios.filter(email=email_teste)

        total = usuarios.count()

        if total == 0:
            self.stdout.write(
                self.style.WARNING(
                    "Nenhum usuário elegível possui e-mail cadastrado."
                )
            )
            return

        capa_url = None

        if livro.capa and livro.capa.file:
            capa_url = (
                "https://192.168.0.245/biblioteca-api/media/"
                f"{livro.capa.file.name}"
            )

        enviados = 0
        falhas = 0

        for usuario in usuarios:
            nome = (
                getattr(usuario, "name", None)
                or usuario.get_username()
            )

            contexto = {
                "livro": livro,
                "nome": nome,
                "biblioteca_url": (
                    "https://192.168.0.245/biblioteca/"
                ),
                "capa_url": capa_url,
            }

            mensagem_html = render_to_string(
                "emails/livro_novo.html",
                contexto,
            )

            mensagem_texto = (
                f"Olá, {nome}!\n\n"
                "Um novo livro foi cadastrado na Biblioteca Antares.\n\n"
                f"Título: {livro.titulo}\n"
                f"ISBN: {livro.isbn or 'Não informado'}\n"
                f"Formato: {livro.formato or 'Não informado'}\n"
                f"Editora: {livro.editora or 'Não informado'}\n"
                f"Categoria: {livro.categoria or 'Não informado'}\n\n"
                f"{livro.sinopse or 'Sinopse não informada.'}\n\n"
                "Acesse a Biblioteca Antares para consultar os detalhes:\n"
                f"{contexto['biblioteca_url']}"
            )

            email = EmailMultiAlternatives(
                subject=(
                    f"Biblioteca Antares - Novo livro: "
                    f"{livro.titulo}"
                ),
                body=mensagem_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[usuario.email],
            )

            email.attach_alternative(
                mensagem_html,
                "text/html",
            )

            if livro.capa and livro.capa.file:
                with livro.capa.file.open("rb") as arquivo:
                    imagem = MIMEImage(
                        arquivo.read(),
                        _subtype="webp",
                    )

                imagem.add_header(
                    "Content-ID",
                    f"<capa-livro-{livro.id}>",
                )

                imagem.add_header(
                    "Content-Disposition",
                    "inline",
                    filename=f"capa-livro-{livro.id}.webp",
                )

                email.attach(imagem)

            try:
                email.send(fail_silently=False)
                enviados += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"E-mail enviado para {usuario.email}"
                    )
                )

            except Exception as e:
                falhas += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Falha ao enviar para "
                        f"{usuario.email}: {e}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Total de usuários elegíveis: {total}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"E-mails enviados: {enviados}"
            )
        )

        if falhas:
            self.stdout.write(
                self.style.ERROR(
                    f"E-mails com falha: {falhas}"
                )
            )
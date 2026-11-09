from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

def enviar_email_cancelamento(reserva_id):
    from core.models import Reserva

    reserva = Reserva.objects.select_related("usuario").get(
        pk=reserva_id
    )

    usuario = reserva.usuario

    if not usuario.email:
        return False

    itens = reserva.itens.select_related("livro").all()
    titulos = [item.livro.titulo for item in itens]

    contexto = {
        "nome": usuario.get_username(),
        "reserva_id": reserva.pk,
        "livro_titulo": ", ".join(titulos) or "Não informado",
        "biblioteca_url": (
            "https://192.168.0.245/biblioteca/"
        ),
    }

    assunto = "Biblioteca Antares - Reserva cancelada"

    mensagem_texto = (
        f"Olá, {contexto['nome']}!\n\n"
        "Sua reserva foi cancelada automaticamente porque "
        "o prazo para retirada expirou.\n\n"
        f"Número da reserva: #{reserva.pk}\n"
        f"Livro(s): {contexto['livro_titulo']}\n\n"
        "Acesse a Biblioteca Antares para consultar "
        "a disponibilidade dos livros."
    )

    mensagem_html = render_to_string(
        "emails/reserva_cancelada.html",
        contexto,
    )

    email = EmailMultiAlternatives(
        subject=assunto,
        body=mensagem_texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[usuario.email],
    )

    email.attach_alternative(mensagem_html, "text/html")
    email.send(fail_silently=False)

    return True

def enviar_email_livro_novo(livro_id, email_teste=None):
    from django.contrib.auth import get_user_model
    from core.models import Livro
    from email.mime.image import MIMEImage

    try:
        livro = Livro.objects.select_related(
            "categoria",
            "editora",
        ).get(pk=livro_id)
    except Livro.DoesNotExist:
        return {
            "total": 0,
            "enviados": 0,
            "falhas": 0,
        }

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
        return {
            "total": 0,
            "enviados": 0,
            "falhas": 0,
        }

    capa_url = None

    if livro.capa and livro.capa.file:
        capa_url = (
            "https://192.168.0.245/biblioteca-api/media/"
            f"{livro.capa.file.name}"
        )

    enviados = 0
    falhas = 0

    conexao = get_connection()

    try:
        conexao.open()

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
                "Um novo livro foi cadastrado na "
                "Biblioteca Antares.\n\n"
                f"Título: {livro.titulo}\n"
                f"ISBN: {livro.isbn or 'Não informado'}\n"
                f"Formato: {livro.formato or 'Não informado'}\n"
                f"Editora: {livro.editora or 'Não informado'}\n"
                f"Categoria: {livro.categoria or 'Não informado'}\n\n"
                f"{livro.sinopse or 'Sinopse não informada.'}\n\n"
                "Acesse a Biblioteca Antares para "
                "consultar os detalhes:\n"
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
                connection=conexao,
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

            except Exception as erro:
                print(
                    f"ERRO ao enviar para {usuario.email}: "
                    f"{type(erro).__name__}: {erro}"
                )
                falhas += 1

    finally:
        conexao.close()

    return {
        "total": total,
        "enviados": enviados,
        "falhas": falhas,
    }
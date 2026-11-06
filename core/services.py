from django.conf import settings
from django.core.mail import EmailMultiAlternatives
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

from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import Autor, Categoria, Editora, Livro, User, Reserva
from core import models
from core.models.reserva import ItensReserva

@register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ('id',)
    list_display = ('email', 'name')
    search_fields = ('email', 'name', 'groups__name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'foto')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

@register(Autor)
class AutorAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 10

@register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    list_filter = ('descricao',)
    ordering = ('descricao',)
    list_per_page = 10

@register(Editora)
class EditoraAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 10

@register(Livro)
class LivroAdmin(ModelAdmin):
    list_display = ('titulo', 'editora', 'categoria')
    search_fields = ('titulo', 'editora__nome', 'categoria__descricao')
    list_filter = ('editora', 'categoria')
    ordering = ('titulo', 'editora', 'categoria')
    list_per_page = 25

class ItensReservaInline(admin.TabularInline):
    model = ItensReserva
    extra = 1
    
@register(Reserva)
class ReservaAdmin(ModelAdmin):
    list_display = (
        'usuario',
        'status',
        'data_criacao',
        'data_retirada',
        'data_devolucao_prevista',
        'data_devolucao',
    )

    ordering = ('usuario', 'status', 'data_criacao')
    search_fields = ('usuario__email', 'status')

    list_filter = (
        'status',
        'data_criacao',
        'data_retirada',
        'data_devolucao_prevista',
        'data_devolucao',
    )

    list_per_page = 10
    inlines = [ItensReservaInline]

    readonly_fields = (
        'data_criacao',
        'data_retirada',
        'data_devolucao_prevista',
        'data_devolucao',
    )
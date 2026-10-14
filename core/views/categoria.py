
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from core.models import Categoria
from core.serializers import CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [SearchFilter]
    search_fields = ['descricao']
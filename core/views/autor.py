
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from core.models import Autor
from core.serializers import AutorSerializer

class AutorViewSet(ModelViewSet):
    queryset = Autor.objects.all().order_by('nome')
    serializer_class = AutorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']
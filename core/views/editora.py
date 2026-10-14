
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from core.models import Editora
from core.serializers import EditoraSerializer

class EditoraViewSet(ModelViewSet):
    queryset = Editora.objects.all()
    serializer_class = EditoraSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']
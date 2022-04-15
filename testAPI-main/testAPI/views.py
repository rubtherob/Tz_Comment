from rest_framework import mixins, viewsets, generics, status
from rest_framework.response import Response

from testAPI.models import Comment, Article
from testAPI.serializers import ArticleSerializer, CommentSerializer


class ArticleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):

        queryset = Comment.objects.filter(article=kwargs['pk'], level__lte=2)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        article = Article.objects.get(id=kwargs['pk'])
        new_data = request.POST.copy()
        new_data['article'] = article.id
        new_data['level'] = 1
        new_data['parent'] = None
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class CommentsDetail(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = Comment.get_descendants(Comment.objects.get(id=kwargs['pk']))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs['pk'])
        new_data = request.POST.copy()
        new_data['parent'] = comment.id
        new_data['article'] = comment.article_id
        new_data['level'] = comment.level + 1
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
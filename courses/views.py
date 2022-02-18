from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

from .models import Course, Evaluation
from .serializers import CourseSerializer, EvaluationSerializer
from .permissions import IsSuperUser

"""
API v1
"""


class CoursesAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for Retrieve, Update or Delete a Course.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EvaluationsAPIView(generics.ListCreateAPIView):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        if self.kwargs.get('course_pk'):
            return self.queryset.filter(course_id=self.kwargs.get('course_pk'))
        return self.queryset.all()


class EvaluationAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for Retrieve, Update or Delete an Evaluation.
    """
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    def get_object(self):
        if self.kwargs.get('course_pk'):
            return get_object_or_404(self.get_queryset(),
                                     course_id=self.kwargs.get('course_pk'),
                                     pk=self.kwargs.get('evaluation_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('evaluation_pk'))


"""
API v2

In this version of API, I simplified the code and included tests.
"""


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsSuperUser,
        permissions.DjangoModelPermissions,
    )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # The default pagination doesn't impact this method. We need to implement
    # the pagination manually.
    @action(detail=True, methods=['get'])
    def evaluations(self, request, pk=None):
        self.pagination_class.page_size = 1
        evaluations = Evaluation.objects.filter(course_id=pk)
        page = self.paginate_queryset(evaluations)

        if page is not None:
            serializer = EvaluationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EvaluationSerializer(evaluations, many=True)
        return Response(serializer.data)


# class EvaluationsViewSet(viewsets.ModelViewSet):
#     queryset = Evaluation.objects.all()
#     serializer_class = EvaluationSerializer

# This code does the same that the last code. But, now, it is easy to
# realize that if you want to remove the possibility of creating a new
# evaluation, you only need to remove the mixins.DestroyModelMixin.
class EvaluationsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

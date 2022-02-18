from rest_framework import serializers
from .models import Course, Evaluation
from django.db.models import Avg


class EvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = Evaluation
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'evaluation',
            'created_at',
            'active'
        )

    def validate_evaluation(self, value):
        if value in range(1, 6):  # 1, 2, 3, 4 or 5.
            return value
        raise serializers.ValidationError('The evaluation need to be an integer from 0 to 5.')


class CourseSerializer(serializers.ModelSerializer):
    # Nested relationship
    # evaluations = EvaluationSerializer(many=True, read_only=True)

    # HyperLinked related field
    # evaluations = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='evaluation-detail'
    # )

    # PrimaryKey related field
    evaluations = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    average_evaluations = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'url',
            'created_at',
            'active',
            'evaluations',
            'average_evaluations'
        )

    def get_average_evaluations(self, obj):
        average = obj.evaluations.aggregate(Avg('evaluation')).get('evaluation__avg')
        if average is None:
            return 0
        return round(average * 2) / 2
from rest_framework import serializers
from .models import User, Project, Votes

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['UID', 'name', 'surname', 'role', 'password', 'login']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            surname=validated_data['surname'],
            role=validated_data['role'],
            login=validated_data['login']
        )
        user.set_hash_password(validated_data['password'])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['PID', 'name', 'date_start', 'date_end', 'description', 'vote_scale']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ['VID', 'PID', 'UID', 'value', 'vote_timestamp']
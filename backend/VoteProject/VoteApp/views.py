from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import User, Project
from .serializers import UserSerializer, ProjectSerializer, VoteSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
def register(request):
    '''
    {
    "name": <string: example>,
    "surname": <string: example>,
    "role": "user" || "admin",
    "password": <string: example>,
    "login": <string: example>
    }

    '''

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully', 'UID': user.UID}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    '''
    {
    "password": <string: example>,
    "login": <string: example>
    }
    '''

    login = request.data['login']
    password = request.data['password']

    try:
        user = User.objects.get(login=login)
        if user.check_password(password):
            return Response({'message': 'Login successful', 'UID': user.UID, 'name': user.name, 'surname': user.surname, 'role': user.role}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid login or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid login or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def create_project(request):
    '''
    {
    "name": "<string: project name>",
    "description": "<string: project description>",
    "date_start": "<string: YYYY-MM-DD>",
    "date_end": "<string: YYYY-MM-DD>",
    "vote_scale": <int: 5 || 10 || 15>
    }
    '''

    serializer = ProjectSerializer(data=request.data)
    
    if serializer.is_valid():
        project = serializer.save()
        return Response({'message': 'Project created successfully', 'PID': project.PID}, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def vote(request):
    '''
    {
    "PID": <int: project id>,
    "UID": <int: user id>,
    "value": <int: 123>
    }
    '''

    pid = request.data['PID']
    uid = request.data['UID']
    value = request.data['value']
    project = get_object_or_404(Project, PID=pid)
    user = get_object_or_404(User, UID=uid) # checking if user exists

    if not 0 <= value <= project.vote_scale:
        return Response({'error': f'Value must be between 0 and {project.vote_scale}.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        vote = serializer.save()
        return Response({'message': 'Project created successfully', 'VID': vote.VID}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

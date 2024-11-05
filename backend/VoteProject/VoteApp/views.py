from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import User, Project, Votes
from .serializers import UserSerializer, ProjectSerializer, VoteSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db.models import Count, Sum
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from .functions import create_histogram
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse, FileResponse



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
        return Response({'error': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)


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


@api_view(['GET'])
def get_stats(request, PID):
    pass


@api_view(['GET'])
def get_project_data(request, pid):
    '''
    if pid == PID:
        {
            "PID" = <int: project id>,
            "name" = <string: project name>,
            "date_start" = <string: YYYY-MM-DD>",
            "date_end" = <string: YYYY-MM-DD>",
            "description" = <string: project decription>,
            "vote_scale" = <int: 5 || 10 || 15>
        }

    elif pid == "all":
        {
            <int: project id>:  {
                                    "name": "name" = <string: project name>,
                                    "date_start": <string: YYYY-MM-DD>",
                                    "date_end": <string: YYYY-MM-DD>",
                                    "description": <string: project decription>,
                                    "vote_scale": <int: 5 || 10 || 15>
                                },
            
            <int: project id>:  {
                                    "name": <string: project name>,
                                    "date_start": <string: YYYY-MM-DD>",
                                    "date_end": <string: YYYY-MM-DD>",
                                    "description": <string: project decription>,
                                    "vote_scale": <int: 5 || 10 || 15>
                                },
  
        }
     '''

    if not pid == 'all':
        try:
            project = Project.objects.get(PID=pid)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Unknown error'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProjectSerializer(project)
        return JsonResponse(serializer.data)
    
    else:
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        projects_dict = {project.pop('PID'): project for project in serializer.data}

        return JsonResponse(projects_dict, safe=False) 


@api_view(['GET'])
def get_report(request, pid):
    
    # Checking whether project exists
    try:
        Project.objects.get(PID=pid)
    except Project.DoesNotExist:
        return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Unknown error'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    styles = getSampleStyleSheet() # Style settings

    # Title
    title = f"Report for PID: {pid}"
    title_paragraph = Paragraph(title, styles['Title'])
    elements = []
    elements.append(title_paragraph)
    elements.append(Spacer(1, 12))

    # Calculate statistics
    pid_count = Votes.objects.filter(PID=pid).count()
    pid_value_sum = Votes.objects.filter(PID=pid).aggregate(Sum('value'))['value__sum']
    
    total_count = Votes.objects.count()
    total_value_sum = Votes.objects.aggregate(Sum('value'))['value__sum']

    percentage_result = round(pid_value_sum/total_value_sum * 100)
    average_value = round(pid_value_sum/pid_count, 1)

    # Paragraph presenting statistics
    project_name = Project.objects.get(PID=pid).name
    vote_scale = Project.objects.get(PID=pid).vote_scale
    stats = [   f"1. Number of voters (PID: {pid}, name: {project_name}): {pid_count}",
                f"2. Number of voters (all projects): {total_count}",
                f"3. Average grade: {average_value}/{vote_scale}",
                f"4. Percentage result in scale of all projects: {percentage_result}%" ]
    
    stats_text = "<br/>".join(stats)

    # Paragraph style
    text_style = ParagraphStyle(name="NormalText", fontSize=12, leading=14)

    # Paragraph with stats
    stats_paragraph = Paragraph(stats_text, text_style)
    elements.append(stats_paragraph)
    elements.append(Spacer(1,12))

    
    votes = Votes.objects.filter(PID_id=pid).select_related('UID')

    table_data = []; votes_timestamps = []

    for vote in votes:
        table_data.append({
            'uid': vote.UID_id,                        
            'name': vote.UID.name,              
            'surname': vote.UID.surname,
            'value': vote.value,
            'vote_timestamp': vote.vote_timestamp      
        })
        votes_timestamps.append(vote.vote_timestamp)

    # Columns headers
    table_data_for_pdf = [["UID", "Name", "Surname", "Value", "Vote Timestamp"]]

    # Adding data to pdf table
    for row in table_data:
        table_data_for_pdf.append([row['uid'], row['name'], row['surname'], row['value'], row['vote_timestamp'].strftime("%Y-%m-%d %H:%M")])

    # Creating pdf table
    table = Table(table_data_for_pdf)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    

    start_date = Project.objects.get(PID=pid).date_start
    end_date = Project.objects.get(PID=pid).date_end
    title = 'Voters histogram in time spaces'

    img_buffer = create_histogram(votes_timestamps, start_date, end_date, 5, title, 500, 400)

    img = Image(img_buffer)
    elements.append(img)
    
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=A4) # Creating pdf document
    pdf.build(elements)
    pdf_buffer.seek(0)
    filename = f"report_pid-{pid}.pdf"

    return FileResponse(pdf_buffer, as_attachment=False, filename=filename)
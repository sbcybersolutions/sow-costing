from django.shortcuts import render, redirect
from .forms import (
    CourseForm, LiveVideoForm, TalentForm,
    AnimatedVideoForm, StudioForm, TechnicalStaffForm
)
from .models import Course, LiveVideo, Talent, AnimatedVideo, Studio, TechnicalStaff

def index(request):
    """
    The front page to enter Client Name, Project Name, and Date.
    """
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        project_name = request.POST.get('project_name')
        date = request.POST.get('date')

        request.session['client_name'] = client_name
        request.session['project_name'] = project_name
        request.session['date'] = date

        return redirect('builder')

    return render(request, 'quotes/index.html')


def builder(request):
    """
    The SOW builder page: add Courses, Videos, Talent, Studio, Technical Staff.
    """
    # Load saved client info
    client_name = request.session.get('client_name')
    project_name = request.session.get('project_name')
    date = request.session.get('date')

    # Forms
    course_form = CourseForm()
    live_video_form = LiveVideoForm()
    talent_form = TalentForm()
    animated_video_form = AnimatedVideoForm()
    studio_form = StudioForm()
    technical_form = TechnicalStaffForm()

    if request.method == 'POST':
        if 'add_course' in request.POST:
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect('builder')

        elif 'add_live_video' in request.POST:
            live_video_form = LiveVideoForm(request.POST)
            if live_video_form.is_valid():
                live_video_form.save()
                return redirect('builder')

        elif 'add_talent' in request.POST:
            talent_form = TalentForm(request.POST)
            if talent_form.is_valid():
                talent_form.save()
                return redirect('builder')

        elif 'add_animated_video' in request.POST:
            animated_video_form = AnimatedVideoForm(request.POST)
            if animated_video_form.is_valid():
                animated_video_form.save()
                return redirect('builder')

        elif 'add_studio' in request.POST:
            studio_form = StudioForm(request.POST)
            if studio_form.is_valid():
                studio_form.save()
                return redirect('builder')

        elif 'add_technical' in request.POST:
            technical_form = TechnicalStaffForm(request.POST)
            if technical_form.is_valid():
                technical_form.save()
                return redirect('builder')

    # Show all added items
    courses = Course.objects.all()
    live_videos = LiveVideo.objects.all()
    talents = Talent.objects.all()
    animated_videos = AnimatedVideo.objects.all()
    studios = Studio.objects.all()
    technical_staff = TechnicalStaff.objects.all()

    return render(request, 'quotes/builder.html', {
        'client_name': client_name,
        'project_name': project_name,
        'date': date,
        'course_form': course_form,
        'live_video_form': live_video_form,
        'talent_form': talent_form,
        'animated_video_form': animated_video_form,
        'studio_form': studio_form,
        'technical_form': technical_form,
        'courses': courses,
        'live_videos': live_videos,
        'talents': talents,
        'animated_videos': animated_videos,
        'studios': studios,
        'technical_staff': technical_staff,
    })

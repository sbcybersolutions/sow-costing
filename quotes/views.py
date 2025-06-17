from django.shortcuts import render, redirect
from .forms import (
    CourseForm, LiveVideoForm, TalentForm,
    AnimatedVideoForm, StudioForm, TechnicalStaffForm
)
from .models import Course, LiveVideo, Talent, AnimatedVideo, Studio, TechnicalStaff

import openpyxl
from openpyxl.utils import get_column_letter
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


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

from django.urls import reverse

from django.shortcuts import get_object_or_404

# ✅ Delete a single asset
def delete_item(request, model_name, pk):
    MODEL_MAP = {
        'course': Course,
        'livevideo': LiveVideo,
        'talent': Talent,
        'animatedvideo': AnimatedVideo,
        'studio': Studio,
        'technical': TechnicalStaff,
    }

    Model = MODEL_MAP.get(model_name)
    if Model is None:
        return redirect('builder')

    obj = get_object_or_404(Model, pk=pk)
    obj.delete()
    return redirect('builder')


# ✅ Clear ALL quote items
def clear_all(request):
    Course.objects.all().delete()
    LiveVideo.objects.all().delete()
    Talent.objects.all().delete()
    AnimatedVideo.objects.all().delete()
    Studio.objects.all().delete()
    TechnicalStaff.objects.all().delete()

    # Optional: also clear session
    request.session.flush()

    return redirect('index')

# Dynamic totals
from django.http import JsonResponse

def get_totals(request):
    total_internal = 0

    # Sum up all internal costs
    for course in Course.objects.all():
        total_internal += course.get_total_internal_cost()

    for lv in LiveVideo.objects.all():
        total_internal += lv.get_total_internal_cost()

    for av in AnimatedVideo.objects.all():
        total_internal += av.get_total_internal_cost()

    for studio in Studio.objects.all():
        total_internal += studio.get_total_internal_cost()

    for tech in TechnicalStaff.objects.all():
        total_internal += tech.get_total_internal_cost()

    # Retail is always 2x internal by your rule
    total_retail = total_internal * 2

    return JsonResponse({
        'total_internal': total_internal,
        'total_retail': total_retail
    })



import openpyxl
from openpyxl.utils import get_column_letter
from io import BytesIO
from django.http import HttpResponse

def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SoW Internal Costs" #type: ignore

    ws.append(["Asset Type", "Description", "Internal Cost"]) #type: ignore

    for course in Course.objects.all():
        ws.append(["Course", course.description, course.get_total_internal_cost()]) #type: ignore

    for lv in LiveVideo.objects.all():
        ws.append(["Live Video", lv.description, lv.get_total_internal_cost()]) #type: ignore
        for talent in lv.talents.all(): #type: ignore
            ws.append(["  └ Talent", talent.name, talent.get_internal_cost()]) #type: ignore

    for av in AnimatedVideo.objects.all():
        ws.append(["Animated Video", av.description, av.get_total_internal_cost()]) #type: ignore

    for studio in Studio.objects.all():
        ws.append(["Studio", studio.studio_name, studio.get_total_internal_cost()]) #type: ignore

    for tech in TechnicalStaff.objects.all():
        ws.append([ #type: ignore
            "Technical Staff",
            f"{tech.filming_days} filming, {tech.editing_days} editing",
            tech.get_total_internal_cost()
        ])

    # Auto-fit columns
    for col in ws.columns: #type: ignore
        max_length = 0
        col_letter = get_column_letter(col[0].column if col[0].column else 1)
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 2 #type: ignore

    # ✅ Save to in-memory buffer instead of save_virtual_workbook
    file_buffer = BytesIO()
    wb.save(file_buffer)
    file_buffer.seek(0)

    response = HttpResponse(
        file_buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="SoW_Internal.xlsx"'
    return response



from django.template.loader import render_to_string
from xhtml2pdf import pisa

def export_pdf(request):
    # Calculate total retail
    total_internal = 0
    for course in Course.objects.all():
        total_internal += course.get_total_internal_cost()
    for lv in LiveVideo.objects.all():
        total_internal += lv.get_total_internal_cost()
    for av in AnimatedVideo.objects.all():
        total_internal += av.get_total_internal_cost()
    for studio in Studio.objects.all():
        total_internal += studio.get_total_internal_cost()
    for tech in TechnicalStaff.objects.all():
        total_internal += tech.get_total_internal_cost()
    total_retail = total_internal * 2

    context = {
        "client_name": request.session.get('client_name'),
        "project_name": request.session.get('project_name'),
        "date": request.session.get('date'),
        "courses": Course.objects.all(),
        "live_videos": LiveVideo.objects.all(),
        "animated_videos": AnimatedVideo.objects.all(),
        "studios": Studio.objects.all(),
        "technical_staff": TechnicalStaff.objects.all(),
        "total_retail": total_retail,
    }

    html = render_to_string('quotes/quote_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SoW_Client.pdf"'

    # pisa.CreatePDF returns True/False
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err: #type: ignore
        return HttpResponse('Error generating PDF', status=500)
    return response

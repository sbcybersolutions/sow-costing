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
from openpyxl.styles import numbers
from quotes.models import (
    Course, CourseResource, LiveVideo, Talent, AnimatedVideo,
    Studio, TechnicalStaff, TechnicalRate, VideoTypeRate, FixedCost, StudioRate, Quote
)


from quotes.models import Quote

def index(request):
    if request.method == 'POST':
        client_name = request.POST['client_name']
        project_name = request.POST['project_name']
        date = request.POST['date']

        # ✅ CREATE THE QUOTE FIRST:
        quote = Quote.objects.create(
            client_name=client_name,
            project_name=project_name,
            date=date,
            created_by=request.user if request.user.is_authenticated else None
        )

        # ✅ Now you can store its ID:
        request.session['quote_id'] = quote.id #type: ignore

        return redirect('builder')

    return render(request, 'quotes/index.html')


def builder(request):
    # ✅ 1) Get active Quote ID safely
    quote_id = request.session.get('quote_id')
    if not quote_id:
        return redirect('index')

    quote = Quote.objects.get(pk=quote_id)

    # ✅ 2) Blank forms for GET
    course_form = CourseForm()
    live_video_form = LiveVideoForm()
    talent_form = TalentForm()
    animated_video_form = AnimatedVideoForm()
    studio_form = StudioForm()
    technical_form = TechnicalStaffForm()

    # ✅ 3) Handle POST for each form
    if request.method == 'POST':
        # One helper to reduce repetition:
        def handle_form(form_class, button_name):
            if button_name in request.POST:
                form = form_class(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.quote = quote
                    obj.save()
                    return True
            return False

        if handle_form(CourseForm, 'add_course'):
            return redirect('builder')
        if handle_form(LiveVideoForm, 'add_live_video'):
            return redirect('builder')
        if handle_form(TalentForm, 'add_talent'):
            return redirect('builder')
        if handle_form(AnimatedVideoForm, 'add_animated_video'):
            return redirect('builder')
        if handle_form(StudioForm, 'add_studio'):
            return redirect('builder')
        if handle_form(TechnicalStaffForm, 'add_technical'):
            return redirect('builder')

    # ✅ 4) Only assets linked to this Quote
    context = {
        'quote': quote,
        'courses': quote.courses.all(), # type: ignore
        'live_videos': quote.live_videos.all(), # type: ignore
        'talents': quote.talents.all(), # type: ignore
        'animated_videos': quote.animated_videos.all(), # type: ignore
        'studios': quote.studios.all(), # type: ignore
        'technical_staff': quote.technical_staff.all(), # type: ignore
        'course_form': course_form,
        'live_video_form': live_video_form,
        'talent_form': talent_form,
        'animated_video_form': animated_video_form,
        'studio_form': studio_form,
        'technical_form': technical_form,
    }
    return render(request, 'quotes/builder.html', context)

def new_quote(request):
    request.session.pop('quote_id', None)
    return redirect('index')

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
    quote_id = request.session.get('quote_id')
    if not quote_id:
        return redirect('index')

    quote = Quote.objects.get(pk=quote_id)
    quote.courses.all().delete() # type: ignore
    quote.live_videos.all().delete() # type: ignore
    quote.animated_videos.all().delete() # type: ignore
    quote.studios.all().delete() # type: ignore
    quote.technical_staff.all().delete() # type: ignore
    quote.talents.all().delete() # type: ignore

    return redirect('builder')


# Dynamic totals
from django.http import JsonResponse

from django.http import JsonResponse
from quotes.models import Quote

def get_totals(request):
    quote_id = request.session.get('quote_id')
    if not quote_id:
        return JsonResponse({'total_internal': 0, 'total_retail': 0})

    quote = Quote.objects.get(pk=quote_id)

    total_internal = sum([
        sum(c.get_total_internal_cost() for c in quote.courses.all()), # type: ignore
        sum(lv.get_total_internal_cost() for lv in quote.live_videos.all()), # type: ignore
        sum(av.get_total_internal_cost() for av in quote.animated_videos.all()), # type: ignore
        sum(s.get_total_internal_cost() for s in quote.studios.all()), # type: ignore
        sum(t.get_total_internal_cost() for t in quote.technical_staff.all()), # type: ignore
    ])

    total_retail = total_internal * 2  # or your custom rule

    return JsonResponse({
        'total_internal': total_internal,
        'total_retail': total_retail
    })


# Export to Excel

def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SoW Detailed Costs" #type: ignore

    row = 1

    # Header
    ws.append(["Asset Type", "Detail", "Quantity/Hours/Seconds", "Rate", "Cost"]) #type: ignore
    row += 1

    # COURSES
    for course in Course.objects.all():
        ws.append([f"Course: {course.description} ({course.complexity})", "", "", "", ""]) #type: ignore
        row += 1

        resources = CourseResource.objects.filter(complexity=course.complexity)
        for r in resources:
            cost = r.fixed_hours * r.hourly_rate
            ws.append([ #type: ignore
                "  └ Resource",
                r.role_name,
                r.fixed_hours,
                f"${r.hourly_rate:.2f}",
                f"${cost:.2f}"
            ])
            row += 1

        # Translation
        if course.num_languages > 0:
            translation_cost = course.get_translation_cost()
            ws.append([ #type: ignore
                "  └ Translation",
                f"{course.num_languages} language(s)",
                "",
                "$500.00",
                f"${translation_cost:.2f}"
            ])
            row += 1

        ws.append([ #type: ignore
            "  → Total Internal",
            "",
            "",
            "",
            f"${course.get_total_internal_cost():.2f}"
        ])
        row += 2

    # LIVE VIDEOS
    for lv in LiveVideo.objects.all():
        ws.append([f"Live Video: {lv.description} ({lv.video_type}, {lv.num_seconds}s)", "", "", "", ""]) #type: ignore
        row += 1

        # Fixed costs
        for fc in FixedCost.objects.all():
            ws.append([ #type: ignore
                "  └ Fixed Cost",
                fc.name,
                "",
                "",
                f"${fc.amount:.2f}"
            ])
            row += 1

        # Variable cost
        rate = VideoTypeRate.objects.get(category="Live", type_name=lv.video_type).rate_per_second
        variable_cost = lv.num_seconds * rate
        ws.append([ #type: ignore
            "  └ Variable",
            f"{lv.num_seconds} sec",
            "",
            f"${rate:.2f}/sec",
            f"${variable_cost:.2f}"
        ])
        row += 1

        # Talents
        for t in lv.talents.all(): #type: ignore
            ws.append([ #type: ignore
                "  └ Talent",
                f"{t.name} ({t.role_type})",
                "",
                "",
                f"${t.get_internal_cost():.2f}"
            ])
            row += 1

        ws.append([ #type: ignore
            "  → Total Internal",
            "",
            "",
            "",
            f"${lv.get_total_internal_cost():.2f}"
        ])
        row += 2

    # ANIMATED VIDEOS
    for av in AnimatedVideo.objects.all():
        ws.append([f"Animated Video: {av.description} ({av.video_type}, {av.num_seconds}s)", "", "", "", ""]) #type: ignore
        row += 1

        for fc in FixedCost.objects.all():
            ws.append([ #type: ignore
                "  └ Fixed Cost",
                fc.name,
                "",
                "",
                f"${fc.amount:.2f}"
            ])
            row += 1

        rate = VideoTypeRate.objects.get(category="Animated", type_name=av.video_type).rate_per_second
        variable_cost = av.num_seconds * rate
        ws.append([ #type: ignore
            "  └ Variable", 
            f"{av.num_seconds} sec",
            "",
            f"${rate:.2f}/sec",
            f"${variable_cost:.2f}"
        ])
        row += 1

        ws.append([ #type: ignore
            "  → Total Internal",
            "",
            "",
            "",
            f"${av.get_total_internal_cost():.2f}"
        ])
        row += 2

    # STUDIOS
    for studio in Studio.objects.all():
        ws.append([f"Studio: {studio.studio_name} ({studio.filming_days} day(s))", "", "", "", ""]) #type: ignore
        row += 1

        s_rate = StudioRate.objects.get(studio_name=studio.studio_name)
        for label, value in [
            ("Hire Rate", s_rate.hire_rate),
            ("Studio Staff", s_rate.studio_staff),
            ("Equipment", s_rate.equipment)
        ]:
            ws.append([ #type: ignore
                "  └ Cost",
                label,
                "",
                "",
                f"${value:.2f} per day"
            ])
            row += 1

        daily_total = s_rate.hire_rate + s_rate.studio_staff + s_rate.equipment
        ws.append([ #type: ignore
            "  → Total Internal",
            f"{studio.filming_days} day(s) × ${daily_total:.2f}",
            "",
            "",
            f"${studio.get_total_internal_cost():.2f}"
        ])
        row += 2

    # TECHNICAL STAFF
    for tech in TechnicalStaff.objects.all():
        ws.append([f"Technical Staff ({tech.filming_days} filming day(s), {tech.editing_days} editing day(s))", "", "", "", ""])    #type: ignore
        row += 1

        for tr in TechnicalRate.objects.all():
            ws.append([ #type: ignore
                "  └ Daily Rate",
                tr.role_name,
                "",
                "",
                f"${tr.daily_rate:.2f} per day"
            ])
            row += 1

        ws.append([ #type: ignore
            "  → Total Internal",
            "",
            "",
            "",
            f"${tech.get_total_internal_cost():.2f}"
        ])
        row += 2

    # Adjust column widths
    for col in ws.columns: #type: ignore
        max_length = 0
        col_letter = get_column_letter(col[0].column)   #type: ignore
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 2 #type: ignore

    # Save to buffer
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="SoW_Detailed.xlsx"'
    return response

# Export to PDF
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

from quotes.models import Quote

def quote_review(request):
    quote_id = request.session.get('quote_id')
    if not quote_id:
        return redirect('index')

    quote = Quote.objects.get(pk=quote_id)

    total_internal = sum([
        sum(c.get_total_internal_cost() for c in quote.courses.all()), # type: ignore
        sum(lv.get_total_internal_cost() for lv in quote.live_videos.all()), # type: ignore
        sum(av.get_total_internal_cost() for av in quote.animated_videos.all()), # type: ignore
        sum(s.get_total_internal_cost() for s in quote.studios.all()), # type: ignore
        sum(t.get_total_internal_cost() for t in quote.technical_staff.all()), # type: ignore
    ])

    total_retail = total_internal * 2

    return render(request, 'quotes/quote_review.html', {
        "quote": quote,
        "courses": quote.courses.all(), # type: ignore
        "live_videos": quote.live_videos.all(), # type: ignore
        "animated_videos": quote.animated_videos.all(), # type: ignore
        "studios": quote.studios.all(), # type: ignore
        "technical_staff": quote.technical_staff.all(), # type: ignore
        "total_internal": total_internal,
        "total_retail": total_retail,
    })


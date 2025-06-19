from django.shortcuts import render, redirect, get_object_or_404
from quotes.models import Quote, Talent
from quotes.forms import (
    CourseForm, LiveVideoForm, TalentForm,
    AnimatedVideoForm, StudioForm, TechnicalStaffForm
)

def index(request):
    if request.method == 'POST':
        client_name = request.POST['client_name']
        project_name = request.POST['project_name']
        date = request.POST['date']

        quote = Quote.objects.create(
            client_name=client_name,
            project_name=project_name,
            date=date,
            created_by=request.user if request.user.is_authenticated else None
        )

        request.session['quote_id'] = quote.id # type: ignore
        return redirect('builder')

    return render(request, 'quotes/index.html')


def builder(request):
    quote_id = request.session.get('quote_id')
    if not quote_id:
        return redirect('index')

    quote = Quote.objects.get(pk=quote_id)

    course_form = CourseForm()
    live_video_form = LiveVideoForm()
    talent_form = TalentForm(quote=quote)
    animated_video_form = AnimatedVideoForm()
    studio_form = StudioForm()
    technical_form = TechnicalStaffForm()

    if request.method == 'POST':
        def handle_form(form_class, button_name):
            if button_name in request.POST:
                if button_name == 'add_talent':
                    form = form_class(request.POST, quote=quote)
                else:
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

    context = {
        'quote': quote,
        'courses': quote.courses.all(), #type: ignore
        'live_videos': quote.live_videos.all(), #type: ignore
        'talents': quote.talents.all(), #type: ignore
        'animated_videos': quote.animated_videos.all(), #type: ignore
        'studios': quote.studios.all(), #type: ignore
        'technical_staff': quote.technical_staff.all(), #type: ignore
        'course_form': course_form,
        'live_video_form': live_video_form,
        'talent_form': talent_form,
        'animated_video_form': animated_video_form,
        'studio_form': studio_form,
        'technical_form': technical_form,
    }
    return render(request, 'quotes/builder.html', context)


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

# Review old quotes

def quote_list(request):
    # If you have auth, filter by user:
    # quotes = Quote.objects.filter(created_by=request.user)
    quotes = Quote.objects.all().order_by('-created_at')
    return render(request, 'quotes/quote_list.html', {'quotes': quotes})

def resume_quote(request, quote_id):
    # ✅ Set this quote as active
    quote = get_object_or_404(Quote, pk=quote_id)
    request.session['quote_id'] = quote.id # type: ignore
    return redirect('builder')


def review_specific_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)

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
        "talents": Talent.objects.filter(live_video__quote=quote), # type: ignore
        "animated_videos": quote.animated_videos.all(), # type: ignore
        "studios": quote.studios.all(), # type: ignore
        "technical_staff": quote.technical_staff.all(), # type: ignore
        "total_internal": total_internal,
        "total_retail": total_retail,
    })
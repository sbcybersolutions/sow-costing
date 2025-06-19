from django.shortcuts import redirect, get_object_or_404
from quotes.models import (
    Course, LiveVideo, Talent, AnimatedVideo,
    Studio, TechnicalStaff, Quote
)

def clear_all(request):
    quote_id = request.session.get('quote_id')
    if not quote_id:
        return redirect('index')

    quote = Quote.objects.get(pk=quote_id)
    quote.courses.all().delete() # type: ignore
    quote.live_videos.all().delete() # type: ignore
    quote.animated_videos.all().delete() # type: ignore
    quote.studios.all().delete() # type: ignore
    quote.technical_staff.all().delete()    # type: ignore
    quote.talents.all().delete() # type: ignore

    return redirect('builder')


def new_quote(request):
    request.session.pop('quote_id', None)
    return redirect('index')


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

def clone_quote(request, quote_id):
    original = get_object_or_404(Quote, pk=quote_id)

    # ✅ 1) Create a new Quote with same data but Draft + not archived
    clone = Quote.objects.create(
        client_name=original.client_name + " (Copy)",
        project_name=original.project_name,
        date=original.date,
        status='Draft',
        is_archived=False,
        created_by=original.created_by,
    )

    # ✅ 2) Clone Courses
    for c in original.courses.all(): # type: ignore
        c.pk = None  # so Django treats it as new
        c.quote = clone
        c.save()

    # ✅ 3) Clone Live Videos + Talents
    for lv in original.live_videos.all(): # type: ignore
        original_lv_id = lv.id
        lv.pk = None
        lv.quote = clone
        lv.save()

        for t in Talent.objects.filter(live_video_id=original_lv_id):
            t.pk = None
            t.live_video = lv  # link to new LV
            t.save()

    # ✅ 4) Clone Animated Videos
    for av in original.animated_videos.all(): # type: ignore
        av.pk = None
        av.quote = clone
        av.save()

    # ✅ 5) Clone Studios
    for s in original.studios.all(): # type: ignore
        s.pk = None
        s.quote = clone
        s.save()

    # ✅ 6) Clone Technical Staff
    for tech in original.technical_staff.all(): # type: ignore
        tech.pk = None
        tech.quote = clone
        tech.save()

    # ✅ 7) Redirect to builder for new Quote
    request.session['quote_id'] = clone.id  # type: ignore
    return redirect('builder')


def toggle_archive(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.is_archived = not quote.is_archived
    quote.save()
    return redirect('quote_list')
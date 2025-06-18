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

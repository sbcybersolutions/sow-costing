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
        sum(s.get_total_internal_cost() for s in quote.studios.all()),  # type: ignore
        sum(t.get_total_internal_cost() for t in quote.technical_staff.all()), # type: ignore
    ])

    total_retail = total_internal * 2

    return JsonResponse({
        'total_internal': total_internal,
        'total_retail': total_retail
    })

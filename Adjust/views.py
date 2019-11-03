from Adjust.models import Dataset
from django.http import JsonResponse
from django.db.models import Sum, Q, F, ExpressionWrapper, FloatField


def dataset_show(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    channels = request.GET.getlist('channels')
    countries = request.GET.getlist('countries')
    os = request.GET.getlist('os')

    aggregation_list = request.GET.getlist('aggregation_list')
    group_by = request.GET.getlist('group_by')
    order_by = request.GET.get('order_by')

    dataset = Dataset.objects
    filter = list()

    if date_from and date_to:
        filter.append(Q(date__range=[date_from, date_to]))
    elif date_from and not date_to:
        filter.append(Q(date__gte=date_from))
    elif not date_from and date_to:
        filter.append(Q(date__lte=date_to))

    if channels:
        filter.append(Q(channel__in=channels))
    if countries:
        filter.append(Q(country__in=countries))
    if os:
        filter.append(Q(os__in=os))

    if len(filter) > 0:
        dataset = dataset.filter(*filter)

    if group_by:
        dataset = dataset.values(*group_by)

    if aggregation_list:
        for aggregator in aggregation_list:
            if aggregator == 'impressions':
                dataset = dataset.annotate(impressions=Sum('impressions'))
            if aggregator == 'clicks':
                dataset = dataset.annotate(clicks=Sum('clicks'))
            if aggregator == 'installs':
                dataset = dataset.annotate(installs=Sum('installs'))
            if aggregator == 'spend':
                dataset = dataset.annotate(spend=Sum('spend'))
            if aggregator == 'revenue':
                dataset = dataset.annotate(revenue=Sum('revenue'))
            if aggregator == 'cpi':
                dataset = dataset.annotate(cpi=ExpressionWrapper(
                Sum('spend')/Sum('installs'), output_field=FloatField()))

    if order_by:
        dataset = dataset.order_by(order_by)

    response = list(dataset)
    return JsonResponse({
        "count": len(response),
        "data": response
    }, safe=False)


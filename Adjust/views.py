from Adjust.models import Dataset
from Adjust.modules.support.response.helper import create_json_response_for_dataset
from Adjust.modules.dataset.operations import Operations


def dataset_show(request):
    """
    view for the only dataset exposing api
    :param request: the request object coming from Django and containing the necessary info for the method to work
    :return: a json response with the requested dataset info
    """
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    channels = request.GET.getlist('channels')
    countries = request.GET.getlist('countries')
    os = request.GET.getlist('os')
    aggregation_list = request.GET.getlist('aggregation_list')
    group_by = request.GET.getlist('group_by')
    order_by = request.GET.get('order_by')

    operations = Operations(date_from, date_to, channels, countries, os, aggregation_list, group_by, order_by)
    dataset = Dataset.objects
    if operations.is_empty_query():
        return create_json_response_for_dataset(list(dataset.values()))
    filters = operations.get_filters()
    dataset = operations.apply_filters(dataset, filters)
    dataset = operations.apply_group_by(dataset)
    dataset = operations.apply_aggregation(dataset)
    dataset = operations.apply_order_by(dataset)

    return create_json_response_for_dataset(list(dataset))


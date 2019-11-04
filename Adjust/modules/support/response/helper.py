from django.http import JsonResponse


def create_json_response_for_dataset(dataset):
    """
    creates a json response out of a dataset object
    :param dataset: the dataset to create the json response for
    :return: a json response object :django.http.JsonResponse
    """
    return JsonResponse({
        "count": len(dataset),
        "data": dataset
    }, safe=False)

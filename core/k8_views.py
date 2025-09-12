import json

from django.http import HttpResponse, JsonResponse


def healthz(request):
    return JsonResponse({"status": "ok"})


def dapr_subscribe(request):
    # Dapr calls this to learn topics (optional approach)
    subs = [{"pubsubname": "kafka-pubsub", "topic": "orders", "route": "orders"}]
    return JsonResponse(subs, safe=False)


def orders_handler(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    try:
        json.loads(request.body)
        # process payload...
        return JsonResponse({"status": "processed"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.shortcuts import render


# Create your views here.


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value123123123",
    })

    return context

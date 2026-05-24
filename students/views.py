from django.shortcuts import render

def home(request):
    context = {
        "name": "Ali",
        "students": ["Mona", "Sara", "Laila"]
    }
    return render(request, "students/home.html", context)
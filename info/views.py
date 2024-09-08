import requests, json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . forms import PersonForm, LoginForm
from . models import Person 

# Create your views here.
def home(request):
    return render(request, "index.html", {})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            context = {
                "form": form.cleaned_data
            }
            request.session["username"] = form.cleaned_data["username"] 
            for person in Person.objects.all():
                if person.username == form.cleaned_data["username"] and person.password == form.cleaned_data["password"]:
                    return HttpResponseRedirect("/tracker/") 
            context = {
                "form": LoginForm(),
                "message": "You do not have an account. Please sign-up"
            }
            return render(request, "login.html", context) 
    else:
        context = {
            "form": LoginForm() 
        }
    return render(request, "login.html", context)

def signup(request):
    if request.method == "POST":
        form = PersonForm(request.POST) 
        if form.is_valid():
            context = {
                "form": form
            }
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            for person in Person.objects.all():
                if person.username == username:
                    context = {
                        "form": PersonForm(), 
                        "message": "Username already exists. Please try again"
                    }
                    return render(request, "signup.html", context) 
            user = Person(username = username, password = password)
            user.save() 
            return HttpResponseRedirect("/login/")  
    else:
        context = {
            "form": PersonForm()
        }
    return render(request, "signup.html", context)

def tracker(request):    
    context = {} 
    if request.method == "POST" and "food-submit" in request.POST:
        food = request.POST["food"] 
        for person in Person.objects.all():
            if person.username == request.session["username"]:
                match request.POST["day"]:
                    case "monday":
                        try:
                            person.monday += food + " " 
                        except:
                            person.monday = food + " "
                    case "tuesday":
                        try:
                            person.tuesday += food + " " 
                        except:
                            person.tuesday = food + " "
                    case "wednesday":
                        try:
                            person.wednesday += food + " "  
                        except:
                            person.wednesday = food + " "
                    case "thursday":
                        try:
                            person.thursday += food + " " 
                        except:
                            person.thursday = food + " "
                    case "friday":
                        try:
                            person.friday += food + " " 
                        except:
                            person.friday = food + " " 
                    case _:
                        print("error") 
                person.save() 
                query = request.POST["food"] 
                api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
                response = requests.get(api_url, headers={'X-Api-Key': '{api_key}'})
                if response.status_code == requests.codes.ok:
                    api = json.loads(response.content)
                    print(api)     
                    person.fat = api[0]["fat_total_g"]
                    person.sodium = api[0]["sodium_mg"] 
                    person.potassium = api[0]["potassium_mg"]
                    person.cholesterol = api[0]["cholesterol_mg"]
                    person.carbohydrates = api[0]["carbohydrates_total_g"]
                    person.fiber = api[0]["fiber_g"]
                    person.sugar = api[0]["sugar_g"] 
                    person.save() 
                else:
                    print("Error:", response.status_code, response.text) 
 
    for person in Person.objects.all():
        if person.username == request.session["username"]:
            if person.monday:
                context["monday"] = person.monday.split()
            if person.tuesday:
                context["tuesday"] = person.tuesday.split()
            if person.wednesday:
                context["wednesday"] = person.wednesday.split()
            if person.thursday:
                context["thursday"] = person.thursday.split()
            if person.friday:
                context["friday"] = person.friday.split()
            context["fat"] = person.fat 
            context["sodium"] = person.sodium
            context["potassium"] = person.potassium
            context["cholesterol"] = person.cholesterol
            context["carbohydrates"] = person.carbohydrates
            context["fiber"] = person.fiber
            context["sugar"] = person.sugar 
    if request.method == "POST" and "clear-submit" in request.POST: # user has pressed the clear button 
        for person in Person.objects.all():
            if person.username == request.session["username"]:
                person.monday = "" # reset all values
                person.tuesday = ""
                person.wednesday = ""
                person.thursday = ""
                person.friday = ""
                person.fat = 0
                person.sodium = 0
                person.potassium = 0
                person.cholesterol = 0
                person.carbohydrates = 0
                person.fiber = 0
                person.sugar = 0 
                person.save() 
                return render(request, "tracker.html", {
                    "fat": person.fat, 
                    "sodium": person.sodium, 
                    "potassium": person.potassium,
                    "cholesterol": person.cholesterol,
                    "carbohydrates": person.carbohydrates,
                    "fiber": person.fiber,
                    "sugar": person.sugar,
                }) 
    return render(request, "tracker.html", context) 
    
        
import datetime
from io import BytesIO
from tkinter import Image
from django.shortcuts import render,HttpResponse
import requests

def home(request):
    message=None
    description = icon = temp = image_url=day = None 
    if request.method=="POST":
        city=request.POST.get('city')
    else:
        city="Agra"
    api_key = 'e901fe0a192196fa64c042cb40c48acb'  #  my API key
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}' #this is my api url
    api_id = 'ThLTAm4b4yu0TlkDkLRsdopbP8ms9g4inoq27dUCrIw' #for image id
    url = f"https://api.unsplash.com/photos/random?query={city}&client_id={api_id}"
    # response = requests.get(url)   #image url get 
    # data=response.json()
    # image_url = data['urls']['full']
    try:
         response = requests.get(url)
         data = response.json()
            
        #  if 'urls' in data:  # Check if the 'urls' key exists
        #     image_url = data['urls']['full']
        #  else:
        #     image_url = None  # Set default image or None if not found
         image_url = data['urls']['full']

    except Exception:
            image_url = None  # Set to None if request fails

    data={'units':'metric'}
    # print('mu unit',data)
    total = requests.get(api_url,data).json()
    if total.get("cod")!=200:
               message = "City not found. Please enter a valid city name."
  
    else:
        description=total['weather'][0]['description']
        icon=total['weather'][0]['icon']
        day=datetime.date.today()
        temp = total['main']['temp']
        print(description,icon,day)
            
    return render(request,"index.html",{'description':description,'icon':icon,'day':day,'city':city,'temp':temp,'image_url': image_url,"message":message})


def fetch_image(request):
    if request.method == "POST":
        city = request.POST.get('city')
        image_url = None
        api_id = 'ThLTAm4b4yu0TlkDkLRsdopbP8ms9g4inoq27dUCrIw'
        
        if city:
            # Unsplash API URL with search term (city name)
            url = f"https://api.unsplash.com/photos/random?query={city}&client_id={api_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    print(data)
                    image_url = data['urls']['regular']  # Get the regular size image URL
                    print('hi',image_url)
            return render(request, 'city.html', {'image_url': image_url, 'city': city})
    else:
        return render(request, 'city.html')


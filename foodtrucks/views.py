import datetime, tasks
from django.http import HttpResponse
from django.template import Context, loader
from foodtrucks.models import FacebookEvent
from constance import config

def index(request):
  upcoming_food_truck = FacebookEvent.getUpcomingFoodtruck(datetime.date.today(), config.LOCATION)
  template = loader.get_template('index.html')
  context = Context({
      'upcoming_food_truck': upcoming_food_truck,
  })
  return HttpResponse(template.render(context))

def send_hipchat_notification(request):
  res = tasks.sendHipChatUpdate()
  return HttpResponse(res[1])

def poll_food_trucks(request):
  if tasks.updateFoodTrucks():
    message = "Polled Facebook successfully"
  else:
    message = "Failed to poll Facebook"
  return HttpResponse(message)
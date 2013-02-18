import facebook, hipchat, datetime
from foodtrucks.models import FacebookEvent
from constance import config

def getFacebookEvents():
  graph = facebook.GraphAPI(config.FACEBOOK_TOKEN)
  # Assume desired events will be on the first page, pagination could be added if needed
  res = graph.request("/OffTheGridSF", {"fields" : "events.fields(description,start_time,end_time,id,location,venue,name)"})
  if res and 'events' in res and 'data' in res['events']:
    return res['events']['data']
  else:
    return None

def updateFoodTrucks():
  events = getFacebookEvents()
  if events:
    # This will not create duplicates, will update existing
    FacebookEvent.saveFromFacebookData(events)
    return True
  else:
    return False

def sendHipChatUpdate():
  token = config.HIPCHAT_TOKEN
  room_id = config.HIPCHAT_ROOMID
  location = config.LOCATION

  todays_date = datetime.date.today()
  event = FacebookEvent.getUpcomingFoodtruck(todays_date, location)

  if event:
    hipster = hipchat.HipChat(token=token)
    message = event.generateHipChatMessage(todays_date)
    res = hipster.message_room(room_id, 'NomNomNom', message)

    if res and 'status' in res and res['status'] == 'sent':
      return (True, "Sent Successfully")
    else:
      return (False, res['status'])

  return (False, "No upcoming food trucks found")

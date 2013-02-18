from django.db import models  
from dateutil import parser
import datetime

class FacebookEvent(models.Model):
  id = models.BigIntegerField(primary_key=True)
  name = models.CharField(max_length=200, null=True)
  location = models.CharField(max_length=200, null=True)
  description = models.TextField(null=True)
  start_time = models.DateTimeField(null=True)
  end_time = models.DateTimeField(null=True)

  def mapFromFacebookObject(self, event):
    self.id = int(event['id'])
    if "name" in event: self.name = event['name'].strip()
    if "location" in event: self.location = event['location'].strip()
    if "description" in event: self.description = event['description'].strip()
    if "start_time" in event: self.start_time = parser.parse(event['start_time'])
    if "end_time" in event: self.end_time = parser.parse(event['end_time'])

  def getVendors(self):
    vendors = []
    in_list = False
    for s in self.description.split("\n"):
      if s == "Vendors:": in_list = True
      elif in_list:
        if s == "": in_list = False
        else: vendors.append(s)
    return vendors

  def generateHipChatMessage(self, todays_date=datetime.date.today()):
    # Assuming all events have a start date
    if self.start_time.date() == todays_date:
      date_str = "today"
    else:
      date_str = self.start_time.strftime("%A %B %d")

    vendors = self.getVendors()

    if vendors and len(vendors):
      vendors_str = ', '.join(vendors)
    else:
      vendors_str = "No vendors found"

    message = 'Foodtrucks for ' + date_str + ': ' +  vendors_str
    return message

  @classmethod
  def getUpcomingFoodtruck(cls, date, location_str):
    res = cls.objects.filter(location__icontains=location_str, start_time__gte=date).order_by("start_time")[:1]
    return res[0] if len(res) else None

  @classmethod
  def saveFromFacebookData(cls, events):
    for event in events:
      db_event = cls()
      db_event.mapFromFacebookObject(event)
      db_event.save()
from django.core.management.base import NoArgsCommand, make_option
from foodtrucks import tasks

class Command(NoArgsCommand):

  help = "Whatever you want to print here"

  option_list = NoArgsCommand.option_list + (
    make_option('--verbose', action='store_true'),
  )

  def handle_noargs(self, **options):
    tasks.updateFoodTrucks()
    tasks.sendHipChatUpdate()
# store/context_processors.py
from .models import Announcement

def current_announcement(request):
    announcement = Announcement.get_current() # Use the class method we defined
    return {'current_announcement': announcement}
from django.test import TestCase
from .views import getData
from .models import Hotspot
import datetime

# Create your tests here.

class HotspotTest(TestCase):

    def setUp(self):
        Hotspot.objects.create(id=1, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=12)
        Hotspot.objects.create(id=2, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=13)
        Hotspot.objects.create(id=3, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=14)
        Hotspot.objects.create(id=4, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=15)
        Hotspot.objects.create(id=5, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=16)
        Hotspot.objects.create(id=6, date=(datetime.datetime.now()-datetime.timedelta(days=3)).strftime("%y-%m-%d %H:%M"), visitor=12234234)
        Hotspot.objects.create(id=7, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=17)
        Hotspot.objects.create(id=8, date=datetime.datetime.now().strftime("%y-%m-%d %H:%M"), visitor=18)
        Hotspot.objects.create(id=9, date=(datetime.datetime.now()-datetime.timedelta(days=3)).strftime("%y-%m-%d %H:%M"), visitor=1242333234)


    def test_get_date(self):
        print(getData(30))
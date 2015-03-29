from django.core.management.base import BaseCommand
from uptimerobot.uptimerobot import UptimeRobot
from status.models import Component

class Command(BaseCommand):
    help = "Import Components from Uptime Robot"

    def handle(self, *args, **options):
        robot = UptimeRobot()
        monitors = robot.getMonitors()
        for itm in monitors:
            component, created = Component.objects.get_or_create(name=monitors[itm], uptime_robot_id=itm)
            if created:
                component.save()

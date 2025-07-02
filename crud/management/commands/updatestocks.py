# myapp/management/commands/updatestocks.py

from django.core.management.base import BaseCommand

from ...views import updateStock


class Command(BaseCommand):
    help = "Fetches and updates stock prices from Tiingo API"

    def handle(self, *args, **kwargs):
        updateStock()
        self.stdout.write(self.style.SUCCESS("Stock prices updated successfully."))
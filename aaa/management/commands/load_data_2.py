import csv

from django.core.management.base import BaseCommand

from aaa.models import Category, Location, User, Ads

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('aaa/csv_files/datasets/location.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                location = Location()
                location.name = row['name']
                location.lat = row['lat']
                location.lng = row['lng']
                location.save()
        print("Command load_data location.csv")

        with open('aaa/csv_files/datasets/user.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                user = User()
                user.first_name = row['first_name']
                user.last_name = row['last_name']
                user.username = row['username']
                user.password = row['password']
                user.role = row['role']
                user.age = row['age']
                # user.location_id = Location.objects.get(id=row['location_id'])
                user.save()
                user.locations.add(Location.objects.get(id=row['location_id']))
        print("Command load_data user.csv")

        with open('aaa/csv_files/datasets/categories.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                categories = Category()
                categories.name = row['name']
                categories.save()
        print("Command load_data categories.csv")

        with open('aaa/csv_files/datasets/ads.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                ad = Ads()
                ad.name = row['name']
                # ad.author_id = row['author_id']
                ad.author = User.objects.get(id=row['author_id'])
                ad.price = row['price']
                ad.description = row['description']
                if row['is_published'] == 'TRUE':
                    ad.is_published = True
                else:
                    ad.is_published = False
                ad.image = row['image']
                # ad.category_id = row['category_id']
                ad.category = Category.objects.get(id=row['category_id'])
                ad.save()
        print("Command load_data ads.csv")
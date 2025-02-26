import csv
from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = "Import categories and products from CSV files"

    def handle(self, *args, **kwargs):
        self.import_categories()
        self.import_products()

    def import_categories(self):
        file_path = "data/categories.csv"
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.get_or_create(
                    id=row["id"],
                    defaults={
                        "name": row["name"],
                        "slug": row["slug"],
                        "description": row["description"]
                        }
                )
        self.stdout.write(self.style.SUCCESS("✅ Categories imported successfully!"))

    def import_products(self):
        file_path = "data/products.csv"
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(id=row["category_id"])  # Ensure category exists
                Product.objects.get_or_create(
                    id=row["id"],
                    defaults={
                        "name": row["name"],
                        "slug": row["slug"],
                        "image": row["image"],
                        "description": row["description"],
                        "price": row["price"],
                        "quantity_available": row["quantity_available"],
                        "category": category
                    }
                )
        self.stdout.write(self.style.SUCCESS("✅ Products imported successfully!"))

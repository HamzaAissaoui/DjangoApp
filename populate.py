from provider.models import Provider
import django
import os
import dotenv
dotenv.load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techChallenge.settings')
django.setup()


def populate_provider():
    providers = [
        {
            "name": "Hamza Aissaoui",
            "email": "test1@gmail.com",
            "phone_number": "4084132222"
        },
        {
            "name": "Jeremiah",
            "email": "testing2@gmail.com",
            "phone_number": "4084130000"
        },

    ]

    for p in providers:
        add_provider(p["name"], p["email"], p["phone_number"])

    # Print out the providers we have added.
    for p in Provider.objects.all():
        print(f"- {p}")


def add_provider(name, email, phone_number):
    p = Provider.objects.get_or_create(email=email)[0]
    p.name = name
    p.email = email
    p.phone_number = phone_number
    p.save()
    return p


# Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate_provider()
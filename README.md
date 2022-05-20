# DjangoApp
All API Documentation can be found here: https://postman.com/galactic-moon-353783/workspace/my-workspace 

This is a REST API that has API endpoints to create, update, delete, and retrieve information about providers. A provider contains the following information:
- Name
- Email
- Phone Number
- Language
- Currency


Once a provider is created they are be able to start defining service areas. These service areas are geojson polygons. There are endpoints to create, update, delete, and get a polygon. A polygon contains:
- Name 
- Price 
- Geojson information.

There is also an API endpoint that takes a lat/lng pair as arguments and returns a list of all polygons that include the given lat/lng. 
    
All of this was built with Django and PostgreSQL with Postgis extension.
There also Basic Authentication (Using provider name in headers) to be able to manipulate Polygons.
The code Follows standard pep8 style.

Currently workin on unit and integration tests.
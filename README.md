<h1>Pizzami</h1>

# Introduction
<img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/banner.jpg" >
A DRF web appliction of a restaurent with customers' custom foods.

This application provides both customer and management APIs.


# Tools
<div style ="display: flex;">
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/python-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/django-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/rest-api-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/postgresql-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/jwt-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/docker-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/cookiecutter-icon.png" >
  <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/swagger-icon.png" >
</div>
- I have used this cookiecutter for my project structure:

https://github.com/AdelNoroozi/Personal-Cookiecutter

- In this structure the main configuration and setting files are inside the config directory and the django apps are inside the pizzami (project_slug) directory. Requirements and Docker related files are seperated for developement and production processes. (for example The main django app is not included in docker developement services to avoid rebuilding project after every modification in code.)

- This project uses Django & Django REST framework for handling APIs.

- The architecure used in this project is the Service Oriented Architecture. All of the queries are wrotten through selector functions which can be found inside the selectors directory in each app. The main business logic of the project is defined as services which are the python fuctions inside services directories. Serializers are also used for validating data or defining data structures. No Generic API View was used in this project because of the SOA architecture and all of the API classes (in apis.py file inside the apps) inherit from APIViews. 

- The rest_framework_simplejwt package is used for authentication. The API classes inherit from two custom mixins for authentication & authorization called ApiAuthMixin and BasePermissionsMixin (pizzami/api/mixins.py). The ApiAuthMixin class is used to access the user requesting when it is needed through business logic. The BasePermissionsMixin defines the logic of API permissions by the HTTP method. There is a dictionary which by default states that HTTP requests with GET methods can be sent by any user, but staff privileges is needed for other methods. This dictionary can be overwritten in any API class if needed.

- PostgreSQL is used as the database for this project. The PostgreSQL's full-text-search tools are used in this project for better search results. To do so, a PostgreSQL extension called pg_trgm is needed. The process of its installation is handled through a migration file inside the core app (pizzami/core/migrations/0001_install_pg_trgm.py). The package will be installed when running the django migrate command and there is no need for manual installation of this extension inside the database.

- The drf_spectacular package is used for documentation of this project. It generates a great UI for working with APIs and also provides the whole authentication functionalities. This UI is accessible inside the base url of the project after running it. Defining these docmentations is done inside the files found in the documentations directory of each app. Request body structure for POST requests, possible respones, parameters & query parameters are described inside the swagger UI for most of the APIs.

# Setup
For running the project, follow the steps bellow.

1-Create a virtual environment:
```bash
virtualenv Venv
```
2-Activate virtual environment:
```bash
source Venv/bin/activate
```
3-Install the requirements:
```bash
pip install -r requirements_dev.txt
```
4-run the developement docker services. The main django app is not included in docker developement services to avoid rebuilding project after every modification in code.
```bash
docker compose -f docker-compose.dev.yml up
```
5-Add your .env file in the root directory. There are some default values to avoid any impropeerly configured exceptions, but for better functionality it's for best to include the environment variables using a .env file. The only part of the app that won't work without these configurations are the email sending services which the required settings could be find in "config/settings/email_sending.py". The app will still work without those settings but no emails would be sent. 

Database settings can also be configured in the .env file, otherwise the app will use the database inside the docker services.

IMPORTANT: The database for this project MUST BE a Postgresql database, because the food search engine uses some functionalities which are only provided by Postgresql databases. For more information go to the part about "searching foods" in the description part.

6- Migrate.
```bash
python manage.py migrate
```

7- Run the project:
```bash
python manage.py runserver
```
8- Create a superuser for using the APIs that need staff privileges or accessing the admin pannel (optional):
```bash
python manage.py createsuperuser
```
# Description
## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/core-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> Core App

The core app is defined for data and functions which belong to the whole project, not a specific part of it.

### constants
Inside the constants.py file, there are three constan values which can be provided by environment variables (.env file).
- WORK_HOUR_START_TIME (default value is 10:00:00): this is used for checking if a process is happening during the work hours and if it causes any conflicts, avoid it to happen.
- WORK_HOUR_END_TIME (default value is 23:00:00): this is used for checking if a process is happening during the work hours and if it causes any conflicts, avoid it to happen.
- BASE_URL (default is the local host): this is used for generating the password reset URL and sending that to users' emails.
### helpers
Inside the helpers.py there is a function that checks current server times and tells if it is during the work hours or not. function is used in multiple places inside the project.
### scheduler
The start function inside scheduler.py file handles periodic tasks. The tasks should be started in related app's apps.py file. This function uses the aspcheduler package. It was first implemented with Celery but then refactored using apscheduler so it works both on windows and linux. (Celery has too many issues on windows)
## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/common-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> common app
This app contains some abstract classes that can be inheritted by other classes inside other apps. This reduces duplicated codes and makes it cleaner.
### models
The common models are:
- BaseModel

  This is the first base abstract model that contains is_active and position field. the position field is used as the default ordering field for data sets of multiple models. The positions are automatically evaluated for each object of the inherited models. This process happens inside the save method. The position of each object equals to first next empty position to its siblings. Siblings are objects that have the same object for their main foreign key field. This logic is defined in a reusable way so by writing the main foreign key field's name in each inherited model as a string inside a "main_fk_field" variable, we can determine how to sort the positions of that model's objects. For example the main_fk_field for Food is category, so foods with the same category are considered siblings and the positioning is done automatically according to them.

- TimeStampedBaseModel

  This abstract model is inherited from the first BaseModel to keep first two fields. It has two time related fields called created_at and updated_at which refer to each object's creation and last modification dates. They are also automatically evaluated.

- ImageIncludedBaseModel

  This model inherits from the TimeStampedBaseModel and is used for models that need an image. It has two nullable fields called image_url and image_alt_text.
### managers
There is a base manager which the abstract BaseModel uses it as its manager class. It has a custom manager called active for accessing only the activated objects of inherited models.
### admin
The admin.py file contains an abstract model admin class called BaseModelAdmin. This model is defined based on the TimeStampedBaseModel and can be inherited for any by any model's admin class that inherits from TimeStampedBaseModel or ImageIncludedBaseModel. 

These items form the common base options for admin panels:
- list_display: position, is_active, created_at & updated_at fields are shown in the list of objects.
- list_editable: activation status of objects can be modified in the list of objects
- list_filter: objects in the list can be filtered by thier activation status or creation & modification dates
- date_hierarchy: the creation date is used for the hierarchical filter of objects
- ordering: objects can be ordered by their position or creation or modification dates
### serializers
There is a PaginatedOutputSerializer inside the serializers.py file. This serializer is used for documentation of APIs that their reponse has pagianted structure. The main object structure must later be determined using a serializer in the child classes.
### services
The change_activation_status service can be used for activating or deactivating objects of any model that inherit from the BaseModel. It takes the id of the object that needs to be deactivated and also the model it belongs to.
### validators
- The string_ending_validator function, checks if an input string ends with a particular string. If not, it will raise a propper exception that transforms to a valid HTTP 400 response.
- The and string_included_validator checks if an input string contains a particular string. If not, it will raise a propper exception that transforms to a valid HTTP 400 response.
## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/api-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> api app
The api app contains the common basic requirements for APIs.
- mixins

The API classes inherit from two custom mixins for authentication & authorization called ApiAuthMixin and BasePermissionsMixin (pizzami/api/mixins.py). The ApiAuthMixin class is used to access the user requesting when it is needed through business logic. The BasePermissionsMixin defines the logic of API permissions by the HTTP method. There is a dictionary which by default states that HTTP requests with GET methods can be sent by any user, but staff privileges is needed for other methods. This dictionary can be overwritten in any API class if needed.
- pagination

  The FullPagination class is the custom class based on rest framework's PageNumberPagination that is used for list APIs in this project. There is a default page_size variable in this custom class so htere won't be an issue if none specified in the request.
- urls

  The urls.py file contains url patterns of other apps' APIs.
## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/authentication-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> authentication app
This app contains the necessary urls and permissions for authenticatin and authorizing users that send requests.
- permissions

  This app contains two custom permissions inherited from BasePermission class that don't exist in rest framework's built-in permissions.
  - IsAuthenticatedAndNotAdmin

    Only non-staff authenticated users can send requests.
  - IsSuperUser

    Only superusers can send requests.
- urls

  urls.py file contains three REST API urls from rest_framework_simplejwt package.
    - login
 
      Takes authentication credentials in request (email & password in this project) and if any active users found with those credentials, returns access and refresh tokens in response.

    - refresh

      Takes a refresh token in request and returns a new access token in response.

    - verify
 
      Takes a token and verifies it.
## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/users-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> users app
Stores the user related data and manages its APIs.

! The description for each module in this app  is made up of two parts, data structure and APIs. Other important components such as selectors, services, serializers, model admins, documentations will be described through the related items inside those two main components.

### ----------user and profile modules----------

#### data structure
- BaseUser

this is the base user model for storing users' data and handling their authentication.

| Field        | Type           | Description                           |
|--------------|----------------|---------------------------------------|
| email        | EmailField     | Email address of the user. This is considered the username field and users use it to login             |
| is_active    | BooleanField   | Indicates if the user account is active (default: True). Deactivated users can't login|
| is_admin     | BooleanField   | Indicates if the user is an admin (default: False)     |
| password     | CharField      | User's password. Hashes before storing                      |
| last_login   | DateTimeField  | Date and time of the last login       |
| created_at   | DateTimeField  | Date and time when the user account was created |
| updated_at   | DateTimeField  | Date and time when the user account was last updated |
| position     | PositiveIntegerField | Position of the user         |


The BaseUserManager is considered BaseUser model's manager. It contains three custom managers for creating normal users, admin users and superusers.

The BaseUserAdmin is this model's admin class. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents user's emails and staff and superuser statuses. It allows editing staff and superuser statuses and filtering by them in the list view. It also allows searching users by their emails or their profiles' public name.

- Profile

profile model holds non-staff users' extended data.

| Field        | Type           | Description                           |
|--------------|----------------|---------------------------------------|
| user         | OneToOneField(BaseUser) | The user associated with this profile |
| bio          | CharField      | Biography of the user|
| public_name  | CharField      | Public name of the user. must be unique |

#### APIs

<details>
  <summary>POST /api/users/register/</summary>

##### method: POST

##### request:
```json
{
  "email": "user@example.com",
  "bio": "string",
  "public_name": "string",
  "password": "stringstri@123",
  "confirm_password": "stringstri@123"
}
```
##### responses:
- 200: user registered successfully

```json
{
  "email": "user@example.com",
  "token": "string",
  "created_at": "2024-03-15T08:51:38.534Z",
  "updated_at": "2024-03-15T08:51:38.534Z"
}
```
- 400: bad request. possible issues:
  - password & confirm password don't match
  - email or public name already exists
  - password is short
  - password does not contain numbers or special characters
</details>

This API is used for registering new non-staff users. If no problem occurs, user will be registered and a new access token will be returned in response for instant login.

<details>
  <summary>/api/users/profile/</summary>

##### method: GET
##### permission: authenticated non staff users
##### responses:
- 200: 

```json
{
  "email": "string",
  "bio": "string",
  "public_name": "string"
}
```
</details>

This API is used for retrieving authenticated non staff user's data.

<details>
  <summary>GET /api/users/</summary>

##### method: GET
##### permission: staff users
##### parameters:
- **is_active**: must be true or false
- **is_admin**: must be true or false
- **is_superuser**: must be true or false
- **order_by**: can be created_at or updated_at. a - symbol can be added before the param for descending order.
- **page**: must be a valid int
- **page_size**: must be a valid int
- **search**: can be any str. this will be done on users' 'email' & 'public name'.

##### responses:
- 200: 

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": {
    "ok": true,
    "data": [
      {
        "id": 0,
        "public_name": "string",
        "bio": "string",
        "last_login": "2024-03-15T09:15:07.711Z",
        "is_superuser": true,
        "position": 0,
        "created_at": "2024-03-15T09:15:07.711Z",
        "updated_at": "2024-03-15T09:15:07.711Z",
        "email": "user@example.com",
        "is_active": true,
        "is_admin": true
      }
    ]
  }
}
```
- 400: bad request. possible issues:
  - invalid page number
- 401: user is not autenticated
- 403: user doesn't have the permission (is not staff user)

</details>

Returns a paginated list of users. Only for staff users. Superusers can access all users but non superuser staff users (admins) can only access non-staff users. staff users can filter the outputs by their activation, staff or superuser statuses. They can also search among them by their email or profile's public name.

<details>
 <summary>PATCH /api/users/{id}/activate</summary>

##### method: PATCH
##### permission: staff users
##### parameters:
- id (path, required, string)

##### responses:
- 200: user acount activated/deactivated successfully
- 401: user is not autenticated
- 403: user doesn't have the permission (is not staff user)
- 404: no user with that id found in requesting users access zone

</details>

changes user's activation status. only for staff users.
### ----------admin module----------
#### APIs
<details>
  <summary>POST /api/users/add-admin/</summary>

##### method: POST
##### permission: superuser
##### request:
```json
{
  "email": "user@example.com",
  "password": "stringstri",
  "confirm_password": "string"
}
```

##### responses:
- 200: admin successfully created
```json
{
  "email": "user@example.com"
}
```
- 400: bad request. possible issues:
  - password & confirm password don't match
  - email or public name already exists
  - password is short
  - password does not contain numbers or special characters
- 401: user is not autenticated
- 403: user doesn't have the permission (is not superuser)
</details>

### ----------address module----------

#### data structure

- Address

| Field | Type | Description |
|-------|------|--------------|
| id | UUIDField | Unique identifier for the address (primary key) |
| user | ForeignKey | User profile associated with the address |
| title | CharField | Title of the address (home for example) |
| address_str | TextField | Full address string |
| phone_number | PhoneNumberField | Phone number associated with the address. phonenumber_field package is used for this  |

The AddressAdmin is this model's admin class. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents user's str value and addresses title & phone number. It allows filtering addresses by their user in the list view. It also allows searching addresses by their title or full string.

#### APIs

<details>
<summary>POST /api/users/my-addresses/</summary>

##### method: POST
##### permission: authenticated non staff users
##### request:
```json
{
  "title": "string",
  "address_str": "string",
  "phone_number": "string"
}
```

##### responses:
- 201: address successfully created
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-15T12:40:38.629Z",
  "updated_at": "2024-03-15T12:40:38.629Z",
  "title": "string",
  "address_str": "string",
  "phone_number": "string"
}
```
- 400: bad request. possible issues:
  - phone number is invalid.
- 401: user is not autenticated
- 403: user doesn't have the permission (is staff user)
</details>

users can add new addresses specified to themselves using this API. 

<details>
<summary>GET /api/users/my-addresses/</summary>

##### method: GET
##### permission: authenticated non staff users

##### responses:
- 200: Represents a list of user's addresses.
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "is_active": true,
    "position": 0,
    "created_at": "2024-03-15T12:54:28.423Z",
    "updated_at": "2024-03-15T12:54:28.423Z",
    "title": "string",
    "address_str": "string",
    "phone_number": "string"
  }
]
```
- 401: user is not autenticated
- 403: user doesn't have the permission (is staff user)
</details>

users can access their own addresses using this API. they can also search among their addresses by their title or the full string.

<details>
<summary>PUT /api/users/my-addresses/{id}/</summary>

##### method: PUT
##### permission: authenticated non staff users (addresses that belong to other users will return a 404 response so those scenarios will not be a permission issue)
##### parameters:
- **id**: id of the address
##### request:
```json
{
  "title": "string",
  "address_str": "string",
  "phone_number": "string"
}
```

##### responses:
- 200: address updated successfully
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-15T12:58:31.719Z",
  "updated_at": "2024-03-15T12:58:31.719Z",
  "title": "string",
  "address_str": "string",
  "phone_number": "string"
}
```
- 400: bad request. possible issues:
  - phone number is invalid.
- 401: user is not autenticated
- 403: user doesn't have the permission (is staff)
- 404: no address with that id found in requesting users access zone
</details>

users can update their own addresses using this API. this APi has only access to addresses that belong to requesting users. 

! anytime an order is created with an address object, the address data will be stored in the order object as plain text. so later modification on address objects won't cause any invalid data in order app.

<details>
<summary>DELETE /api/users/my-addresses/{id}/</summary>

##### method: DELETE
##### permission: authenticated non staff users (addresses that belong to other users will return a 404 response so those scenarios will not be a permission issue)
##### parameters:
- **id**: id of the address

##### responses:
- 204: address deleted successfully
- 401: user is not autenticated
- 403: user doesn't have the permission (is staff)
- 404: no address with that id found in requesting users access zone
</details>

users can delete their own addresses using this API. this APi has only access to addresses that belong to requesting users. 

! anytime an order is created with an address object, the address data will be stored in the order object as plain text. so later address deletion objects won't cause any invalid data in order app.

### ----------password module----------
#### APIs

<details>
  <summary>POST /api/users/change-password/</summary>

##### method: POST
##### permission: authenticated users
##### request:

```json
{
  "old_password": "string",
  "password": "stringstri@123",
  "confirm_password": "stringstri@123"
}
```
##### responses:
- 200: password changed successfully.
- 400: input values are invalid or don't match the expected format. possible issues:
  - password & confirm password don't match
  - email or public name already exists
  - password is short
  - password does not contain numbers or special characters
- 401: user is not authenticated.

this API is used to change an athenticated users password

</details>

<details>
  <summary>POST /api/users/request-password-reset/</summary>

##### method: POST
##### permission: anyone
##### request body:

```json
{
  "email": "user@example.com"
}
```
##### responses:
- 200: reset password email sent successfully.

- 400: input values are invalid or don't match the expected format. e.g: email is invalid or does not exist.

- 408: something went wrong.

</details>

this APIs is used for requesting authenticated users' password to reset. it takes user's email and sends a reset password url to that.

<details>
  <summary>POST /api/users/reset-password/{uid}/{token}/</summary>

##### method: POST
##### permissions: anyone
##### parameters:

- token: string
- uid: string

##### request:
```json
{
  "password": "stringstri@123",
  "confirm_password": "stringstri@123"
}
```
##### responses:

- 200: password reset successfully.
- 400: input values are invalid or don't match the expected format. possible issues:
  - password & confirm password don't match
  - email or public name already exists
  - password is short
  - password does not contain numbers or special characters
- 403: Invalid or expired token.

</details>

this is the API url which is sent to user's email after requesting a password reset. it contains user's encoded id and a token with an access to reset password.

## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/ingredients-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> ingredients app
Stores the food ingredient related data and manages its APIs.

! The description for each module in this app is made up of two parts, data structure and APIs. Other important components such as selectors, services, serializers, model admins, documentations will be described through the related items inside those two main components.

### ----------ingredient category module----------
#### data structure

- Ingredient Category

| Field            | Type           | Description                            |
|------------------|----------------|----------------------------------------|
| id               | UUIDField      | Unique identifier for the category     |
| name             | CharField      | Name of the ingredient category  |
| is_active        | BooleanField   | Indicates if the category is active |
| position         | PositiveIntegerField | Position of the category |
| image_url        | CharField      | URL of the category's image |
| image_alt_text   | CharField      | Alt text for the category's image |
| created_at       | DateTimeField  | Date and time when the category was created |
| updated_at       | DateTimeField  | Date and time when the category was last updated |

This model holds information about food ingredients' categories. By categorizing ingredients (for example categorizing pesto cheese and mozarella cheese as cheese) we can have a clear defenition of different food structures so users can create their custom foods easier. This will be explained more in the food app. Ingredient categories inherit from image included base model so each ingredient category can have a specific image.

The IngredientCategoryAdmin is Ingredient Category models' admin class. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents ingredient category's name in the list view. This admin panel also allows searching ingredient categories by their name.

#### APIs
<details>
  <summary>GET /api/ingredients/categories/</summary>

##### method: GET
##### permissions: anyone, but only staff users have access to deactivated objects.
##### responses:

- 200: created_at, updated_at & is_active fields are only visible to users with staff privileges.

```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "is_active": true,
    "position": 0,
    "created_at": "2024-03-16T16:55:08.070Z",
    "updated_at": "2024-03-16T16:55:08.070Z",
    "image_url": "string",
    "image_alt_text": "string",
    "name": "string"
  }
]
```

</details>

returns a list of ingredient categories (all of them for staff users and only activated ones for non staff users). created_at, updated_at & is_active fields are only visible to users with staff privileges.

<details>
  <summary>POST /api/ingredients/categories/</summary>

#### method: POST
#### permission: staff users
#### Request:

```json
{
  "name": "string",
  "image_url": "string",
  "image_alt_text": "string",
  "is_active": true
}
```

#### Responses:

- 201: an ingredient category created successfully

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-16T17:02:28.267Z",
  "updated_at": "2024-03-16T17:02:28.267Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string"
}
```

- 400: input values are invalid or don't match the expected format. e.g: image alt text does not contain /ingredient category's name.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a new ingredient category

</details>

adds a new ingredient category. only for staff users.

<details>
  <summary>PUT /api/ingredients/categories/{id}/</summary>

#### method: PUT
#### Pernission: staff users
#### parameters:
- id: ingredient category's id

#### Request body:
```json
{
  "name": "string",
  "image_url": "string",
  "image_alt_text": "string",
  "is_active": true
}
```
#### Responses:

- 200: ingredient category updated successfully
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-16T17:06:50.504Z",
  "updated_at": "2024-03-16T17:06:50.504Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string"
}
```
- 400: input values are invalid or don't match the expected format. e.g: image alt text does not contain /ingredient category's name.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient category

- 404: ingredient category with specified id does not exist

</details>

updates an ingredient category. only for staff users.

<details>
  <summary>DELETE /api/ingredients/categories/{id}/</summary>

#### method: DELETE
#### Pernission: staff users
#### parameters:
- id: ingredient category's id

#### Responses:

- 204: ingredient category deleted successfully.

- 400: can't delete this category as long as it has ingredients or some food category is using it as one of its compounds.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient category

- 404: ingredient category with specified id does not exist

</details>

deletes an ingredient category. only for staff users. if that category contains any ingredients or some food compound object (explained later) refers to that category as a foreign key, this won't happen.

<details>
  <summary>PATCH /api/ingredients/categories/{id}/activate</summary>

#### method: PATCH
#### Pernission: staff users
#### Parameters:
- id: ingredient category's id

#### Responses:

- 200: status changed successfully

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient category

- 404: ingredient category with specified id does not exist

</details>

changes ingredient category's activation status. only for staff users. if the ingredient category is active, it will be deactivated and if it is deactivated it will be activated.

### ----------ingredient module----------
#### data structure

- Ingredient

| Field                  | Type           | Description                                 |
|------------------------|----------------|---------------------------------------------|
| id                     | UUIDField      | Unique identifier for the ingredient        |
| category               | ForeignKey(IngredientCategory) | Category to which the ingredient belongs, main_fk_field |
| name                   | CharField      | Name of the ingredient     |
| png_file_url           | CharField      | URL of the PNG file for the ingredient, this is the graphical representation of the ingredient when the user is trying to create a custom food with the GUI |
| png_file_alt_text      | CharField      | Alt text for the PNG file |
| price                  | FloatField     | Per unit of the ingredien's price                     |
| unit                   | CharField      | Unit of measurement for the ingredient |
| remaining_units        | PositiveIntegerField | Remaining units of the ingredient in the stock |
| stock_limit            | PositiveIntegerField | Stock limit for the ingredient, this is the limit which if the remaining amount of ingredient is above that, the restaurent can make sure that it can handle enough orders containing foods with that ingredient  |
| is_available           | BooleanField   | Indicates if the ingredient is available |
| auto_check_availability | BooleanField   | If true, the system automatically makes the ingredient unavailable when the remaining units reach stock limit and the foods with that ingredient will become unavailable too (default: False) |
| is_active              | BooleanField   | Indicates if the ingredient is active (default: True) |
| position               | PositiveIntegerField | Position of the ingredient |
| created_at             | DateTimeField  | Date and time when the ingredient was created |
| updated_at             | DateTimeField  | Date and time when the ingredient was last updated |
| image_url              | CharField      | URL of the ingredient's image (max length: 512) |
| image_alt_text         | CharField      | Alt text for the ingredient's image (max length: 50) |

holds information of the ingredients. this model's save method is overriden in a way so that if the object's auto_check_availability is true, check its rmaining units and compare it with the stock limit and determine the ingredient's availability. then checks if the availability statud of any food using that ingredient needs to be modified or not. more explanation in foods model.

The IngredientAdmin is the Ingredient models' admin class. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents ingredient's name, category, is_available, auto_check_availability, remaining_units, unit & price fields in the list view. It allows editing ingredient's remaining units, auto_check_availabilty field & availabilty status in the list view and filtering them by their category, availability and price. Price & remaining units filters in the admin panel are implemented with SliderNumericFilter from admin_numeric_filter package to filter these values in a spectrum with a slider. This admin panel also allows searching ingredients by their name or category's name. Finally ingredients can be ordered by their price or remaining units in the admin panel.

#### APIs
<details>
  <summary>GET /api/ingredients/</summary>

##### method: GET
##### permissions: anyone, but only staff users have access to deactivated objects.
##### parameters:
- **category**: must be the id of an ingredient category
- **page**: must be a valid int
- **page_size**: must be a valid int
##### responses:

- 200: created_at, updated_at & is_active fields are only visible to users with staff privileges.

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": {
    "ok": true,
    "data": [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "category": {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "position": 0,
          "image_url": "string",
          "image_alt_text": "string",
          "name": "string"
        },
        "is_active": true,
        "position": 0,
        "created_at": "2024-03-16T17:51:26.441Z",
        "updated_at": "2024-03-16T17:51:26.441Z",
        "image_url": "string",
        "image_alt_text": "string",
        "name": "string",
        "png_file_url": "string",
        "png_file_alt_text": "string",
        "price": 0,
        "unit": "string",
        "remaining_units": 2147483647,
        "stock_limit": 2147483647,
        "is_available": true,
        "auto_check_availability": true
      }
    ]
  }
}
```

</details>

Returns a paginated list of ingredients(all of them for staff users and only activated ones for non staff users). created_at, updated_at & is_active fields are only visible to users with staff privileges. users can filter the output ingredients by their category.

<details>
  <summary>POST /api/ingredients/categories/</summary>

#### method: POST
#### permission: staff users
#### Request:

```json
{
  "name": "string",
  "image_url": "string",
  "image_alt_text": "string",
  "is_active": true
}
```

#### Responses:

- 201: an ingredient category created successfully

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-16T17:02:28.267Z",
  "updated_at": "2024-03-16T17:02:28.267Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string"
}
```

- 400: input values are invalid or don't match the expected format. e.g: image alt text does not contain /ingredient category's name.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient

</details>

adds a new ingredient. only for staff users. after creating an ingredient, the system checks if its auto_check_availabilty field is true or not, if so it will determine if its available or not based on its remaining units and stock limits.

<details>
  <summary>PUT /api/ingredients/{id}/</summary>

#### method: PUT
#### Pernission: staff users
#### parameters:
- id: ingredient's id

#### Request body:
```json
{
  "is_active": true,
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "png_file_url": "string",
  "png_file_alt_text": "string",
  "price": 0,
  "unit": "string",
  "remaining_units": 2147483647,
  "stock_limit": 2147483647,
  "is_available": true,
  "auto_check_availability": true,
  "category": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
#### Responses:

- 200: ingredient updated successfully
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "category": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "position": 0,
    "image_url": "string",
    "image_alt_text": "string",
    "name": "string"
  },
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-17T06:25:49.792Z",
  "updated_at": "2024-03-17T06:25:49.792Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "png_file_url": "string",
  "png_file_alt_text": "string",
  "price": 0,
  "unit": "string",
  "remaining_units": 2147483647,
  "stock_limit": 2147483647,
  "is_available": true,
  "auto_check_availability": true
}
```
- 400: input values are invalid or don't match the expected format. e.g: image alt text does not contain /ingredient category's name.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient

- 404: ingredien with specified id does not exist

</details>

updates an ingredient category. only for staff users. after updating an ingredient, the system checks if its auto_check_availabilty field is true or not, if so it will determine if its available or not based on its remaining units and stock limits.

<details>
  <summary>DELETE /api/ingredients/{id}/</summary>

#### method: DELETE
#### Pernission: staff users
#### parameters:
- id: ingredient's id

#### Responses:

- 204: ingredient deleted successfully.

- 400: can't delete this ingredient as long as it is used in a food.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient

- 404: ingredient with specified id does not exist

</details>

deletes an ingredient category. only for staff users. if that ingredient is used in a food this won't happen.

<details>
  <summary>PATCH /api/ingredients/{id}/activate</summary>

#### method: PATCH
#### Pernission: staff users
#### Parameters:
- id: ingredient's id

#### Responses:

- 200: status changed successfully

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete an ingredient

- 404: ingredient with specified id does not exist

</details>

changes ingredient's activation status. only for staff users. if the ingredient is active, it will be deactivated and if it is deactivated it will be activated.

## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/foods-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> foods app
Stores the food related data and manages its APIs.

! The description for each module in this app is made up of two parts, data structure and APIs. Other important components such as selectors, services, serializers, model admins, documentations will be described through the related items inside those two main components.

### ----------food category module----------
#### data structure

- Food Category

| Field          | Type           | Description                                 |
|----------------|----------------|---------------------------------------------|
| id             | UUIDField      | Unique identifier for the food category     |
| name           | CharField      | Name of the food category |
| icon_url       | CharField      | URL of the category's icon |
| icon_alt_text  | CharField      | Alt text for the category's icon |
| is_customizable| BooleanField   | Indicates if the category is customizable. Normal customers can only create foods from customizable categories.  |
| image_url      | CharField      | URL of the category's image |
| image_alt_text | CharField      | Alt text for the category's image |
| is_active      | BooleanField   | Indicates if the food category is active |
| position       | PositiveIntegerField | Position of the food category |
| created_at     | DateTimeField  | Date and time when the food category was created |
| updated_at     | DateTimeField  | Date and time when the food category was last updated |

This model is used to categorize foods. It is an ImageIncludedBaseModel which means that each food can have its own image.

- Food Category Compound

| Field                | Type                     | Description                                     |
|----------------------|--------------------------|-------------------------------------------------|
| id                   | UUIDField                | Unique identifier for the food category compound |
| food_category        | ForeignKey(FoodCategory) | Food category which the compound object belongs to. main_fk_field    |
| ingredient_category  | ForeignKey(IngredientCategory) | Ingredient category that exists in the structure of that food category that current compound object is refering to |
| min                  | PositiveIntegerField     | Minimum quantity of ingredients from current catrgory in the compound (default: 1) |
| max                  | PositiveIntegerField     | Maximum quantity of ingredients from current catrgory in the compound |
| is_active            | BooleanField             | Indicates if the food category compound is active (default: True) |
| position             | PositiveIntegerField     | Position of the food category compound |

This model is used to define each food category's structure, so the GUI can represent the custom food creation process according to that and also created foods have a valid rational structure. For example the compounds for burger category would be something like this:
- min:1 and max:1 ingredient from the buns ingredient category
- min:1 and max:3 ingredient(s) from the meat ingredient category
- min:0 and max:4 ingredient(s) from the cheese ingredient category
- min:0 and max:5 ingreedient(s) from the toppping ingredient category
- min:0 and max:3 ingredient(s) from the sauce ingredient category

The FoodCategoryAdmin is the Food Category & Food Category Compound models' admin class. It contains the FoodCategoryCompoundInlineAdmin tabular inline admin as an inline adminstration component for the compounds so a food category with its compounds can be adminstrated in a single page. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents food category's name in the list view. It allows filtering food categories by their customizability in the list view. It also allows searching food categories by their name. The image_alt_text and icon_alt_text fields are prepopulated by the food category's name while creating or updating.

#### APIs
<details>
  <summary>GET /api/foods/categories/</summary>

##### method: GET
##### permissions: anyone, but only staff users have access to deactivated objects.
#### parameters:
- is_customizable: can be true or false
##### responses:

- 200: a list of food categories

```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string",
    "icon_url": "string",
    "icon_alt_text": "string"
  }
]
```

</details>

returns a list of food categories (all of them for staff users and only activated ones for non staff users). this API only contains general information for representing in the menu or when user is trying to create a new custom food. the outputs can be filtered by customizablity (so when users are trying to create a new custom foods they can see the customizable categories to choose.)

<details>
  <summary>POST /api/foods/categories/</summary>

#### method: POST
#### permission: staff users
#### Request:

```json
{
  "compounds": [
    {
      "min": 2147483647,
      "max": 2147483647,
      "ingredient_category": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
  ],
  "is_active": true,
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "icon_url": "string",
  "icon_alt_text": "string",
  "is_customizable": true
}
```

#### Responses:

- 201: a food category created successfully

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "compounds": [
    {
      "ingredient_category": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "position": 0,
        "image_url": "string",
        "image_alt_text": "string",
        "name": "string"
      },
      "min": 2147483647,
      "max": 2147483647
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-17T20:08:15.279Z",
  "updated_at": "2024-03-17T20:08:15.279Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "icon_url": "string",
  "icon_alt_text": "string",
  "is_customizable": true
}
```

- 400: 	input values are invalid or don't match the expected format. possible issues:
  - a compound's min value is larger than its max value.
  - customizable category does not have compunds
  - not customizable category has compounds
  - image alt text or icon alt text does not contain category's name
  - image alt text or icon alt text does not end with the word 'food category'

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a food category

</details>

adds a new food category. only for staff users. created food category's compounds must be involved in the body if the category is customizable.

<details>
  <summary>GET /api/foods/categories/{id}/</summary>

#### method: GET
#### Pernission: anyone, but only staff users have access to deactivated objects.
#### parameters:
- id: food category's id

#### Responses:

- 200: information of the requested food category retrieved
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "icon_url": "string",
  "icon_alt_text": "string",
  "compounds": [
    {
      "ingredient_category": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "position": 0,
        "image_url": "string",
        "image_alt_text": "string",
        "name": "string"
      },
      "min": 2147483647,
      "max": 2147483647
    }
  ]
}
```

- 404: food category with specified id does not exist in requesting user's access zone

</details>

retrieves information of a single food category. staff purposes: admins see complete details of a food category. non-staff purposes: customers want to create a new food and need specific details containing information about that category's compounds. is customizable, is_active, position & all timestamped fields are only included for staff purposes.

<details>
  <summary>PUT /api/foods/categories/{id}/</summary>

#### method: PUT
#### Pernission: staff users
#### parameters:
- id: food category's id

#### Request body:
```json
{
  "compounds": [
    {
      "min": 2147483647,
      "max": 2147483647,
      "ingredient_category": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
  ],
  "is_active": true,
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "icon_url": "string",
  "icon_alt_text": "string",
  "is_customizable": true
}
```
#### Responses:

- 200: food category updated successfully
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "compounds": [
    {
      "ingredient_category": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "position": 0,
        "image_url": "string",
        "image_alt_text": "string",
        "name": "string"
      },
      "min": 2147483647,
      "max": 2147483647
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-17T20:29:58.375Z",
  "updated_at": "2024-03-17T20:29:58.375Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "icon_url": "string",
  "icon_alt_text": "string",
  "is_customizable": true
}
```
- 400: 	input values are invalid or don't match the expected format. possible issues:
  - a compound's min value is larger than its max value.
  - customizable category does not have compunds
  - not customizable category has compounds
  - image alt text or icon alt text does not contain category's name
  - image alt text or icon alt text does not end with the word 'food category'

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a food category

- 404: food category with specified id does not exist

</details>

updates a food category. only for staff users. if compounds exist in the body, previous compounds will be deleted first and new ones will be replaced.

<details>
  <summary>DELETE /api/foods/categories/{id}/</summary>

#### method: DELETE
#### Pernission: staff users
#### parameters:
- id: food category's id

#### Responses:

- 204: food category deleted successfully.

- 400: can't delete this category as long as it has foods.

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a food category

- 404: food category with specified id does not exist

</details>

deletes a food category. only for staff users. if that category contains food(s) this won't happen.

<details>
  <summary>PATCH /api/foods/categories/{id}/activate</summary>

#### method: PATCH
#### Pernission: staff users
#### Parameters:
- id: food category's id

#### Responses:

- 200: status changed successfully

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a food category

- 404: food category with specified id does not exist

</details>

changes food category's activation status. only for staff users. if the food category is active, it will be deactivated and if it is deactivated it will be activated.

### ----------food module----------
#### data structure

- Food

| Field                  | Type                     | Description                                            |
|------------------------|--------------------------|--------------------------------------------------------|
| id                     | UUIDField                | Unique identifier for the food                         |
| name                   | CharField                | Name of the food                    |
| category               | ForeignKey(FoodCategory) | Category to which the food belongs, main_fk_field                    |
| created_by             | ForeignKey(Profile)      | Profile of the user who created the food (nullable, because original foods are created by the management, not any customer)     |
| description            | TextField                | Description of the food                                 |
| rate                   | FloatField               | Rate of the food (range: 0-5)               |
| is_original            | BooleanField             | Indicates if the food is original, foods created by the management are considered original food and foods created by customer users are not original       |
| price                  | FloatField               | Price of the food                                      |
| views                  | PositiveIntegerField     | Number of views of the food (default: 0)                |
| ordered_count          | PositiveIntegerField     | Number of times the food has been ordered (default: 0) |
| is_public           | BooleanField             | Indicates if user wants the food to be published or not (default: False), this doesn't necessarily mean that the food is public and exists in the menu, it just determines if the creator wants the food to be in the public menu or just wants to order the food for himself/herself, if the user wants to publish the food (and this field becomes true) it must be confirmed by the management before becoming available in the menu             |
| is_confirmed              | BooleanField             | Indicates if the food is confirmed by management or not (nullable, default: null), if the value is null it means that it is suspended and no decision has been made about its confirmation yet, if the value is true it means that the food is confirmed and will be in the public meny, if it is false it means the food is rejected by the management, users can still access their rejected foods so they can modify its issue and try republishing it again       |
| is_available           | BooleanField             | Indicates if the food is available (default: True), it depends on the availability of its ingredients      |
| auto_check_availability| BooleanField             | If true, the system automatically makes the food unavailable when any of its ingredients is not available (default: False)  |
| is_active              | BooleanField             | Indicates if the food is active (default: True)         |
| position               | PositiveIntegerField     | Position of the food                       |
| created_at             | DateTimeField            | Date and time when the food was created                |
| updated_at             | DateTimeField            | Date and time when the food was last updated            |
| image_url              | CharField                | URL of the food's image              |
| image_alt_text         | CharField                | Alt text for the food's image        |

This model holds information of the foods. It is an ImageIncludedBaseModel which means that each food can have its own image. This model has two custom methods:
- check_availability: this is the method called by Ingredient model's overriden save method after updating availability of one of its object, while trying to also check if the foods using it need to be modified or not.
- update_rate: after a user rates a food, this function is called to update the food's rate value by calculating the its average ratings. even though this is a violation of database normalization, but since getting ratings happens way much more than submitting ratings, this aproach will be better for performance

This model has a secendary manager called "tags" which is an object of TaggableManager from django_taggit package. This package is a great tool for tagging objects of a model. The taggit package doesn't support models with UUID primary key by default and UUIDTaggedItem is a custom inherited class to make tagging this model with a UUID avilable.

- Food Ingredient

| Field         | Type                     | Description                                     |
|---------------|--------------------------|-------------------------------------------------|
| id            | UUIDField                | Unique identifier for the food ingredient      |
| food          | ForeignKey(Food)         | Food associated with the ingredient, (main_fk_field)             |
| ingredient    | ForeignKey(Ingredient)   | Ingredient associated with the food             |
| amount        | PositiveIntegerField     | Amount of the ingredient required for the food  |
| is_active     | BooleanField             | Indicates if the food ingredient is active (default: True) |
| position      | PositiveIntegerField     | Position of the food ingredient   |

This model defines the many to many relationship between the Food and Ingredient models to store ingredients of each food and the amount of them.

The FoodManager is considered Food model's manager. It contains two custom managers for accessing public and confirmed foods.

The FoodAdmin is the Food & Food Ingredient models' admin class. It contains the FoodIngredientInlineAdmin tabular inline admin as an inline adminstration component for each food's ingredient so a food with its ingredients can be adminstrated in a single page. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents food's name, rate, is_confirmed, is_public, is_available, auto_check_availability, views, ordered_count and is_original fields in the list view. It allows editing foods' confirmation, publicity, availabilty & auto_check_availability statuses in the list view and filtering them by those four editable fields mentioned and also is_original field, tags, category, price and ordered_count. Price and ordered count filters in the admin panel are implemented with SliderNumericFilter from admin_numeric_filter package to filter these values in a spectrum with a slider. This admin panel also allows searching foods by their name, category's name, description and tags. The image_alt_text and icon_alt_text fields are prepopulated by the food's name while creating or updating. Finally foods can be ordered by their rate, views, created_at, updated_at, price & ordered_count in the admin panel.

#### APIs
<details>
  <summary>GET /api/foods/</summary>

##### method: GET
##### permissions: anyone, but only staff users have access to deactivated objects and only creators have access to non public or unconfirmed objects
##### parameters:
- **category**: Must be the id of a food category.
- **created_by**: Must be the id of a user profile.
- **is_confirmed**: Must be true or false.
- **is_original**: Must be true or false.
- **is_public**: Must be true or false.
- **order_by**: Can be rate, price, ordered_count, position, created_at, or updated_at. A - symbol can be added before the param for descending order.
- **page**: Must be a valid int.
- **page_size**: Must be a valid int.
- **price__gt**: Must be a float.
- **price__lt**: Must be a float.
- **search**: Can be any string.
- **set**: Can be null or 'mine'.
- **tags__name**: Must be a tag.

##### responses:

- 200: the output format for staff users or users who request their own set of foods is different

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": {
    "ok": true,
    "data": [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "category": "string",
        "created_by": {
          "id": 0,
          "public_name": "string"
        },
        "ingredients_str": "string",
        "discounted_price": 0,
        "tags": "string",
        "is_active": true,
        "position": 0,
        "created_at": "2024-03-18T11:29:42.314Z",
        "updated_at": "2024-03-18T11:29:42.314Z",
        "image_url": "string",
        "image_alt_text": "string",
        "name": "string",
        "rate": 0,
        "is_original": true,
        "price": 0,
        "views": 0,
        "ordered_count": 0,
        "is_confirmed": true,
        "is_public": true,
        "is_available": true,
        "auto_check_availability": true
      }
    ]
  }
}
```
- 403: requesting user is a staff user but the set parameter value is "mine"
- 
</details>

Returns a paginated list of foods(all of them for staff users, activated, public and confirmed ones for non staff users and activated ones for creators). If the set parameter has the value 'mine' it will show foods created by requesting user (staff users don't have the privelege to do so). created_at, updated_at & is_active, is_public, is_confirmed & auto_check_availabilty fields are only visible to users with staff privileges or the foods' owners. Explanation about some of the output fields:
- category: returns category's icon url
- created_by: returns creators public name
- inredients_str: returns a string representation of ingredients with this format :

  "<ingredient's amount in the food> <ingredient's unit>(s) of <ingredient's name>, ..." e.g: 1 loaf of bugget, 2 pats of ground beef burger, 2 layers of goda cheese
- discounted_price: returns food's price after discount if it has any
- tags: returns a list of the foods tags' names

The output can be filtered these parameters: category, creator, being original, price range, confirmation, publicity and tags.

Searching is available on this API. PostgreSQL's full text search tools have been used for this API. It performs stemming (using roots of the strings to search), stopping (ignoring words like of, in and ...) and trigram similarity (specifies a similariy rate between users input and values inside database) to return the best possible result for user's search input. Foods' name, category's name, tags, and description are used as fields that searching happens on. Each field has a weight while searching which is: A for name, B for category's name and tags, C for description. After performing search only results with a trigram similarity above 0.3 and similarity rank above 0.1 will be returned and sorted in a descending order by those two items.

Results can also be ordered by rate, price, ordered_count, position, created_at, updated_at ascending & descending.

<details>
  <summary>POST /api/foods/</summary>

#### method: POST
#### permission: authenticated users
#### Request:

```json
{
  "name": "string",
  "category": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "description": "string",
  "ingredients": [
    {
      "ingredient": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "amount": 2147483647
    }
  ],
  "image_url": "string",
  "image_alt_text": "string",
  "is_public": true,
  "is_available": true,
  "price": 0,
  "auto_check_availability",
  "tags": [
    "string"
  ]
}
```

#### Responses:

- 201: a food created successfully

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "category": "string",
  "created_by": {
    "id": 0,
    "public_name": "string"
  },
  "ingredients_str": "string",
  "discounted_price": 0,
  "tags": "string",
  "ingredients": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "is_active": true,
      "position": 0,
      "amount": 2147483647,
      "ingredient": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-18T14:20:54.836Z",
  "updated_at": "2024-03-18T14:20:54.836Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "description": "string",
  "rate": 0,
  "is_original": true,
  "price": 0,
  "views": 0,
  "ordered_count": 0,
  "is_confirmed": true,
  "is_public": true,
  "is_available": true,
  "auto_check_availability": true
}
```

- 400: 	input values are invalid or don't match the expected format. possible issues:
  - there is some ingredient that should not be inside foods from this category
  - there is an invalid amount of some ingredient
  - non staff user is trying to create a food inside an inactive category (the error would be the same as non existent id for category to protect management level data)
  - non staff user is trying to create a food inside a non customizable category
  - image alt text or icon alt text does not contain food's name

- 401: user is not authenticated

</details>

adds a new food. both staff and non staff users can create new foods. food ingredients (a list of dicts as above) and tags (a list of strings) must be involved in the body. Explanation about some of the fields:
- the price field is only needed when requesting user is a staff user, otherwise the food price will be calculated by sum of its ingredients' price plus 20% added value.
- only staff users can set a value for auto_check_availability field, for non staff users it would be automatically false
- if the requesting user is a staff user, the is_confirmed field would be true on creation
- if the requesting user is not a staff user, the is_original field would be false

<details>
  <summary>GET /api/foods/{id}/</summary>

#### method: GET
#### Pernission: anyone, but only staff users have access to deactivated objects and only creators have access to non public or unconfirmed objects
#### parameters:
- id: food's id

#### Responses:

- 200: information of the requested food retrieved
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "category": "string",
  "created_by": {
    "id": 0,
    "public_name": "string"
  },
  "ingredients_str": "string",
  "discounted_price": 0,
  "tags": "string",
  "ingredients": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "is_active": true,
      "position": 0,
      "amount": 2147483647,
      "ingredient": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-18T16:32:13.882Z",
  "updated_at": "2024-03-18T16:32:13.882Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "description": "string",
  "rate": 0,
  "is_original": true,
  "price": 0,
  "views": 0,
  "ordered_count": 0,
  "is_confirmed": true,
  "is_public": true,
  "is_available": true,
  "auto_check_availability": true,
  "comments": [
    {
      "user": "ali",
      "children": [
        {
          "user": "jalilam",
          "children": [],
          "is_active": true,
          "position": 1,
          "created_at": "2024-03-19T08:28:46.555152Z",
          "updated_at": "2024-03-19T08:28:46.555152Z",
          "text": "sdfasfsa",
          "by_staff": false,
          "lft": 2,
          "rght": 3,
          "tree_id": 3,
          "level": 1
        }
      ],
      "is_active": true,
      "position": 3,
      "created_at": "2024-03-09T20:11:24.814966Z",
      "updated_at": "2024-03-09T20:11:24.814966Z",
      "text": "dsaasdasfd",
      "by_staff": false,
      "lft": 1,
      "rght": 4,
      "tree_id": 3,
      "level": 0
    }
  ],
}
```

- 404: food with specified id does not exist in requesting user's access zone

</details>

retrieves information of a single food. Explanation about some of the fields:
- ingredients: instead of a string, ingredients are represented as a list of FoodIngredient objects here.
- created_by: an object of cretor user's profile containing profile id and its public name, the name is for representing in the UI and th id is for getting foods of that creator by the filters inside foods list API
- comments: is a hierarchical list of confirmed comments submitted for that food


<details>
  <summary>PUT /api/foods/{id}/</summary>

#### method: PUT
#### Pernission: staff users or creator of the food
#### parameters:
- id: food's id

#### Request body:
```json
{
  "name": "string",
  "category": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "description": "string",
  "ingredients": [
    {
      "ingredient": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "amount": 2147483647
    }
  ],
  "image_url": "string",
  "image_alt_text": "string",
  "is_public": true,
  "is_available": true,
  "price": 0,
  "tags": [
    "string"
  ]
}
```
#### Responses:

- 200: food category updated successfully
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "category": "string",
  "created_by": {
    "id": 0,
    "public_name": "string"
  },
  "ingredients_str": "string",
  "discounted_price": 0,
  "tags": "string",
  "ingredients": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "is_active": true,
      "position": 0,
      "amount": 2147483647,
      "ingredient": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-18T16:35:10.206Z",
  "updated_at": "2024-03-18T16:35:10.206Z",
  "image_url": "string",
  "image_alt_text": "string",
  "name": "string",
  "description": "string",
  "rate": 0,
  "is_original": true,
  "price": 0,
  "views": 0,
  "ordered_count": 0,
  "is_confirmed": true,
  "is_public": true,
  "is_available": true,
  "auto_check_availability": true
}
```
- 400: 	input values are invalid or don't match the expected format. possible issues:
  - a compound's min value is larger than its max value.
  - customizable category does not have compunds
  - not customizable category has compounds
  - image alt text or icon alt text does not contain category's name
  - image alt text or icon alt text does not end with the word 'food category'

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a food

- 404: food with specified id does not exist in requesting user's access zone
- 503: user is trying to update a public confirmed food (a food inside the menu) during work hours

</details>

updates a food. staff users have full access but normal users can only update name, description and publicity of their own foods and afterwards, the food's confirmation status will be changed to null value (suspended and waiting for confirmation). if ingredients exist in the body, previous ingredients will be deleted first and new ones will be replaced. the same logic applies for the tags. this API only works during work hours for public confirmed foods (the foods inside the menu) to avoid conflicts while customers are trying to order.

<details>
  <summary>DELETE /api/foods/{id}/</summary>

#### method: DELETE
#### Pernission: staff users or creator of the food
#### parameters:
- id: food's id

#### Responses:

- 204: food category deleted (or deactivated) successfully.

- 401: user is not authenticated

- 404: food with specified id does not exist in requesting user's access zone
- 503: user is trying to update a public confirmed food (a food inside the menu) during work hours

</details>

deletes a food. staff users have full access but normal users can only delete their own foods. if that any order is submitted for that food or the food exists in a cart, it will be deactivated instead of getting deleted so no order records would miss after deletion. this API only works during work hours for public confirmed foods (the foods inside the menu) to avoid conflicts while customers are trying to order.

<details>
  <summary>PATCH /api/foods/{id}/{action}</summary>

#### method: PATCH
#### Pernission: staff users
#### Parameters:
- id: food's id
- action: must be confirm, reject or suspend

#### Responses:

- 200: food's confirmation status changed successfully
- 400: invalid request, probably due to invalid action or trying to change foods status to an status which the food is already in.

- 401: user is not authenticated

- 403: non-staff user is trying to change confirmation status of a food

- 404: food with specified id does not exist

</details>

changes food's confirmation status to confirmed, rejected or suspended. only for staff users.


<details>
  <summary>PATCH /api/foods/{id}/activate</summary>

#### method: PATCH
#### Pernission: staff users
#### Parameters:
- id: food's id

#### Responses:

- 200: status changed successfully

- 401: user is not authenticated

- 403: non-staff user is trying to change activation status of a food

- 404: food with specified id does not exist

</details>

changes food's activation status. only for staff users. if the food is active, it will be deactivated and if it is deactivated it will be activated.

## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/feedback-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> feedback app
Stores users' feedback related data to foods and manages its APIs.

! The description for each module in this app is made up of two parts, data structure and APIs. Other important components such as selectors, services, serializers, model admins, documentations will be described through the related items inside those two main components.

### ----------rating module----------
#### data structure

- Rating

| Field         | Type                    | Description                                    |
|---------------|-------------------------|------------------------------------------------|
| id            | UUIDField               | Unique identifier for the rating               |
| food          | ForeignKey(Food)        | Food associated with the rating                |
| user          | ForeignKey(Profile)     | User who submitted the rating                  |
| rate          | PositiveIntegerField    | Rating given to the food (range: 1-5)         |

stores users' ratings to foods

#### APIs
<details>
  <summary>PUT /api/feedback/rate-food/</summary>

#### method: PUT
#### Pernission: authenticated non staff users

#### Request body:
```json
{
  "food": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "rate": 5
}
```
#### Responses:

- 200: food's rating by current user created/updated/deleted successfully.

- 400: 	input values are invalid or don't match the expected format. possible issues:
  - the rate is not a valid integer
  - the food is not a valid UUID

- 401: user is not authenticated

- 403: user doesn't have the permission (is staff user)
- 
- 404: no food with specified id found in user's access zone

</details>

this API is used for rating foods. if user has not rated the specified food before, it will rate it by the specified rating in the body. else it will update the previous rating. also it will remove user's rating for a food if the rate value equals to 0.

### ----------comment module----------

#### data structure

- Comment

| Field         | Type                    | Description                                    |
|---------------|-------------------------|------------------------------------------------|
| id            | UUIDField               | Unique identifier for the comment              |
| food          | ForeignKey(Food)        | Food associated with the comment               |
| user          | ForeignKey(Profile)     | User who submitted the comment, nullable for staff users' comments                 |
| parent        | TreeForeignKey(Comment) | Parent comment, if any, main_fk_field                          |
| text          | TextField               | Content of the comment                          |
| is_confirmed  | BooleanField            | Indicates if the comment is confirmed by management (nullable)|
| by_staff      | BooleanField            | Indicates if the comment was made by staff so that it can be shown in a different format in the UI      |
| created_at    | DateTimeField           | Date and time when the comment was created     |
| updated_at    | DateTimeField           | Date and time when the comment was last updated|

This model is a mptt model using django-mptt package. mptt models define a tree relationship between objects of the same model. This feature is used for the comment model to provide the comment reply system functionality, so that each reply is a comment object with a parent foreign key to the comment it's replying to.

The comment model's clean function is overriden to avoid invalid data. Two important contraints are checked befor saving a comment:
- a comment's parent must be for the same food as itself
- a comment's must be confirmed

The CommentModelAdmin is the coment models' admin class. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents comment's str value (user's public name or if it is submitted by admins "staff", food's name and comment creation date), is_confirmed, field and its parent str value in the list view. It allows editing comments' confirmation status in the list view and filtering them by their food, user, parent, confirmation status or by_staff field. This admin panel also allows searching comments by their text.

#### APIs
<details>
<summary>GET /api/feedback/comments/</summary>

##### method: GET
##### permission: authenticated users, but non staff users can only access their own comments with setting the set patameter's value to "mine"
##### parameters:
- **food**: Must be the id of a food.
- **user**: Must be the id of a user profile. (only for staff users, cause non staff users only access to their own orders)
- **is_confirmed**: Must be true or false.
- **order_by**: can be position, created_at, updated_at. a - symbol can be added before the param for descending order..
- **page**: Must be a valid int.
- **page_size**: Must be a valid int.
- **search**: Can be any string.
- **set**: Can be null or 'mine'.
- **tags__name**: Must be a tag.

##### responses:
- 200: Represents a list of comments.
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": {
    "ok": true,
    "data": [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "food": {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "name": "string",
          "price": 0,
          "discounted_price": 0,
          "category": "string",
          "created_by": "string",
          "rate": 0,
          "ordered_count": 0,
          "is_original": true,
          "is_available": true,
          "ingredients_str": "string",
          "image_url": "string",
          "image_alt_text": "string",
          "tags": "string"
        },
        "parent": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "text": "string",
        "created_at": "2024-03-19T08:45:24.158Z",
        "updated_at": "2024-03-19T08:45:24.158Z",
        "is_confirmed": true,
        "user": {
          "id": 0,
          "public_name": "string"
        },
        "by_staff": true
      }
    ]
  }
}
```
- 401: user is not autenticated
- 403: user doesn't have the permission (is staff user with value "mine" for set parameters or a non staff user withou value "mine" for set parameter)
</details>

returns a paginated list of comments (all of them for staff users, but for normal users only the ones created by them). API's staff purposes: admins can see comments to confirm or reject them. API's non-staff purposes: customers can see their own comments.

The output can be filtered by these parameters: food, user & confirmation.

Searching is available on this API. It will be done on comments' text or food.

Results can also be ordered by position, created_at or updated_at ascending & descending.

<details>
<summary>POST /api/feedback/comments/</summary>

##### method: POST
##### permission: authenticated users
##### request:
```json
{
  "food": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "parent": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "text": "string"
}
```

##### responses:
- 201: comment successfully created
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "food": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string",
    "price": 0,
    "discounted_price": 0,
    "category": "string",
    "created_by": "string",
    "rate": 0,
    "ordered_count": 0,
    "is_original": true,
    "is_available": true,
    "ingredients_str": "string",
    "image_url": "string",
    "image_alt_text": "string",
    "tags": "string"
  },
  "parent": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "text": "string",
  "created_at": "2024-03-19T11:44:55.367Z",
  "updated_at": "2024-03-19T11:44:55.367Z",
  "is_confirmed": true
}
```
- 400: bad request. possible issues:
  - active food with that id does not exist in public access zone
  - parent does not exist
  - food is not the same as its parent
  - parent is not confirmed
- 401: user is not autenticated
</details>

creates a new comment. if requesting user is a staff user, the is confirmed and by staff fields will be automatically set to true, otherwise they will be null and false.

<details>
<summary>DELETE /api/feedback/comments/{id}/</summary>

##### method: DELETE
##### permission: staff users or creator of the comment
##### parameters:
- **id**: id of the comment

##### responses:
- 204: comment deleted successfully
- 401: user is not autenticated
- 404: no comment with that id found in requesting user's access zone
</details>

this API deletes comments. staff users can delete any comment and non staff users only their own comments.

<details>
  <summary>PATCH /api/feedback/comments/{id}/{action}/</summary>

#### method: PATCH
#### Pernission: staff users
#### Parameters:
- id: comment's id
- action: must be confirm, reject or suspend

#### Responses:

- 200: comment's confirmation status changed successfully
- 400: invalid request, probably due to invalid action or trying to change comment's status to an status which the comment is already in.

- 401: user is not authenticated

- 403: non-staff user is trying to change confirmation status of a comment

- 404: comment with specified id does not exist

</details>

changes comment's confirmation status to confirmed, rejected or suspended. only for staff users.

## <img src="https://github.com/AdelNoroozi/Pizzami/blob/master/resources/orders-app-icon.png?raw=true" style="vertical-align:middle;margin-right:10px;"> orders app
Stores order related data (discounts, carts, orders and discounts) and manages its APIs.

! The description for each module in this app is made up of three parts, data structure, APIs, tasks. Other important components such as selectors, services, serializers, model admins, documentations will be described through the related items inside those two main components.

### ----------discount module----------
#### data structure

- Discount

| Field              | Type                  | Description                                                |
|--------------------|-----------------------|------------------------------------------------------------|
| id                 | UUIDField             | Unique identifier for the discount                          |
| name               | CharField             | Name of the discount                    |
| description        | TextField             | Description of the discount (nullable)                      |
| is_public          | BooleanField          | Indicates if the discount is public (can be accessed by anyone)         |
| code               | CharField             | Discount code (unique, nullable), it is nullable because discounts specified to foods or food categories are represented inside the menu and shouldn't have a code           |
| has_time_limit     | BooleanField          | Indicates if the discount has a time limit (default: False)|
| type               | CharField(choices=TYPE_CHOICES) | Type of the discount (choices: absolute or ratio)         |
| start_date         | DateTimeField         | Start date of the discount (nullable)                      |
| expiration_date    | DateTimeField         | Expiration date of the discount (nullable)                 |
| specified_to_type  | CharField(choices=SPECIFIED_TO_CHOICES) | Specified to type (choices: user, food, category), discounts can be specified to different things such as users, foods or food categories, it can also be none for broad discounts that will apply to orders (so they must have a code) |
| specified_type     | ForeignKey(ContentType)| Since discounts can be specified to different things, type of the specified object should be determined (nullable)                  |
| object_id          | CharField             | Since discounts can be specified to different things, id of the specified object should be determined                     |
| specified_object   | GenericForeignKey     | Specified object which is an object of "specified_type" with "object_id"                                           |
| percentage_value   | FloatField            | Percentage value of the discount (nullable, range: 1-100)  |
| absolute_value     | FloatField            | Absolute value of the discount (nullable)                   |
| created_at         | DateTimeField         | Date and time when the discount was created                |
| updated_at         | DateTimeField         | Date and time when the discount was last updated           |

Holds information of the discounts. discounts can be specified to different things such as users, foods or food categories, so a django generic foreign key is used to determine what is it specified to. discounts can be time limited and have a start date and expiration date. some discounts may be public. some discounts may have a code. some discounts have an absolute value, for example a 5$ discount, but some of them (ratio type) have a percentage value, like 20%.

The discount model's clean function is overriden to avoid invalid data. Six important contraints are checked befor saving a comment:
- a time limited discount must have a start date and an end date
- discounts with absolute type must have an absolute value
- discounts with ratio type must have a percentage value
- user-specified or public broad discounts (specified_to_type is null) must have a code.
- food or food category specified discounts must not have a code
- user specified discounts can not be public

The DiscountAdmin is the Discount model's admin class. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents discounts' name, type, is_public, specified_to_type, absolute_value and percentage_value fields in the list view. It allows editing discounts' publicity status and absolute and percentage value in the list view and filtering them by their publicity status, type, specified to type, absolute value & percentage value. Absolute value & percentage value filters in the admin panel are implemented with SliderNumericFilter from admin_numeric_filter package to filter these values in a spectrum with a slider. This admin panel also allows searching discounts by their names and descriptions. Finally discounts can be ordered by their absolute_value, percentage_value, created_at, updated_at, price & ordered_count in the admin panel.

#### APIs
<details>
  <summary>GET /api/orders/discounts/</summary>

##### method: GET
##### permissions: authenticated users, but non staff users can only access their own discounts with setting the set patameter's value to "mine"
##### parameters:
- **has_time_limit**: Must be true or false.
- **is_active**: Must be true or false.
- **is_public**: Must be true or false.
- **order_by**: Can be start_date, expiration_date, position, created_at, updated_at, absolute_value, percentage_value. a - symbol can be added before the param for descending order..
- **page**: Must be a valid int.
- **page_size**: Must be a valid int.
- **search**: Can be any string.
- **specified_to_type**: Must be USR (user), FOD (food) or CAT (food category).
- **type**: must be ABS (absolute) or RAT (ratio).

##### responses:

- 200: the output format for staff users and non staff users is different, for normal users it only contains the id, name, description, code, exp dat and value (if it's abs it will be a string with absolute value and $ and otherwise percentage value and %) of the discount, but for staff users it contains every single field, specified_to field would also differ based on what the discount is specified to
 
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": {
    "ok": true,
    "data": [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "specified_to": {
                "id": "4aa85f64-5717-4562-b3fc-2c963f66afa6"
          },
        "is_active": true,
        "position": 0,
        "created_at": "2024-03-20T09:50:05.217Z",
        "updated_at": "2024-03-20T09:50:05.217Z",
        "name": "string",
        "description": "string",
        "is_public": false,
        "code": "string",
        "has_time_limit": true,
        "type": "ABS",
        "start_date": "2024-03-20T09:50:05.217Z",
        "expiration_date": "2024-03-20T09:50:05.217Z",
        "specified_to_type": "USR",
        "percentage_value": 10,
        "absolute_value": null
      }
    ]
  }
}
```
- 401: user is not authenticated
 
</details>

Returns a paginated list of discounts(all of them for staff users, user specified for non staff users). The output format for staff users and non staff users is different, for normal users it only contains the id, name, description, code, exp dat and value (if it's abs it will be a string with absolute value and $ and otherwise percentage value and %) of the discount, but for staff users it contains every single field. The specified_to field will represent a dictionary containing general information about the refered object. This happens using RelatedField and by checking the "specified_to" object's type, returns a proper serializer for representation.

The output can be filtered by these parameters: has_time_limit, is_active, is_public, specified_to_type & type.

Searching is available on this API. It will be done on discounts' names & descriptions.

Results can also be ordered by start_date, expiration_date, position, created_at, updated_at, absolute_value, percentage_value ascending & descending.

<details>
  <summary>POST /api/orders/discounts/</summary>

#### method: POST
#### permission: staff users
#### Request:

```json
{
  "is_active": true,
  "name": "string",
  "description": "string",
  "is_public": false,
  "code": "string",
  "has_time_limit": true,
  "type": "ABS",
  "start_date": "2024-03-20T11:29:23.904Z",
  "expiration_date": "2024-03-20T11:29:23.904Z",
  "specified_to_type": "USR",
  "object_id": "string",
  "percentage_value": 10,
  "absolute_value": null
}
```

#### Responses:

- 201: a new discount created successfully

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "specified_to": "string",
  "is_active": true,
  "position": 2,
  "created_at": "2024-03-20T11:29:23.905Z",
  "updated_at": "2024-03-20T11:29:23.905Z",
  "name": "string",
  "description": "string",
  "is_public": false,
  "code": "string",
  "has_time_limit": true,
  "type": "ABS",
  "start_date": "2024-03-20T11:29:23.905Z",
  "expiration_date": "2024-03-20T11:29:23.905Z",
  "specified_to_type": "USR",
  "percentage_value": 10,
  "absolute_value": null
}
```

- 400: input values are invalid or don't match the expected format. possible issues:
  - a time limited discount must have a start date and an end date
  - discounts with absolute type must have an absolute value
  - discounts with ratio type must have a percentage value
  - user-specified or public broad discounts (specified_to_type is null) must have a code.
  - food or food category specified discounts must not have a code
  - user specified discounts can not be public

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a discount

- 404: no specified object found for this specified id for the specified type

</details>

creates a new discount. only for staff users. by using the specified_to_type and object_id fields, the system will find the exact specified object to specify the new discount to it. each food or food category can have only one specified activated discount at a time. so for avoiding any issues, all the previous discounts wolud be deactivated before adding a new acitve discount.


<details>
  <summary>PUT /api/orders/discounts/{id}/</summary>

#### method: PUT
#### Pernission: staff users
#### parameters:
- id: discount's id

#### Request body:
```json
{
  "is_active": true,
  "name": "string",
  "description": "string",
  "is_public": false,
  "code": "string",
  "has_time_limit": true,
  "type": "ABS",
  "start_date": "2024-03-20T11:29:23.904Z",
  "expiration_date": "2024-03-20T11:29:23.904Z",
  "specified_to_type": "USR",
  "object_id": "string",
  "percentage_value": 10,
  "absolute_value": null
}
```
#### Responses:

- 200: discount updated successfully
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "specified_to": "string",
  "is_active": true,
  "position": 2,
  "created_at": "2024-03-20T11:29:23.905Z",
  "updated_at": "2024-03-20T11:29:23.905Z",
  "name": "string",
  "description": "string",
  "is_public": false,
  "code": "string",
  "has_time_limit": true,
  "type": "ABS",
  "start_date": "2024-03-20T11:29:23.905Z",
  "expiration_date": "2024-03-20T11:29:23.905Z",
  "specified_to_type": "USR",
  "percentage_value": 10,
  "absolute_value": null
}
```
- 400: input values are invalid or don't match the expected format. possible issues:
  - a time limited discount must have a start date and an end date
  - discounts with absolute type must have an absolute value
  - discounts with ratio type must have a percentage value
  - user-specified or public broad discounts (specified_to_type is null) must have a code.
  - food or food category specified discounts must not have a code
  - user specified discounts can not be public

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a discount

- 404: possible issues:
  - discount object with this id does not exist
  - no specified object found for this specified id for the specified type

</details>

updates a discount. only for staff users. each food or food category can have only one specified activated discount at a time. so for avoiding any issues, all the previous discounts wolud be deactivated before editting a discount and its new status is active.

<details>
  <summary>DELETE /api/orders/discounts/{id}/</summary>

#### method: DELETE
#### Pernission: staff users
#### parameters:
- id: discount's id

#### Responses:

- 204: discount deleted successfully.

- 400: can't delete this discount because one or multiple orders exist with it

- 401: user is not authenticated

- 403: non-staff user is trying to create, update or delete a discount

- 404: discount with specified id does not exist

</details>

deletes a discount. only for staff users. if that discount is used in an order this won't happen.

<details>
  <summary>POST /api/orders/discounts/inquiry/</summary>

#### method: POST
#### Pernission: non staff authenticated users

#### Request body:
```json
{
  "code": "string"
}
```

#### Responses:

- 200: discount is acceptable
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "string",
  "description": "string",
  "code": "string",
  "expiration_date": "2024-03-21T06:01:29.232Z",
  "value": "string"
}
```

- 400: code missed or is not string

- 401: user is not authenticated

- 403: user is not allowed to perform this action on discounts (is staff user)

- 406: discount code is not acceptable. maybe it is invalid, expired, deactivated or belongs to another user (the reason is not represented)

</details>

this API recieves a discount code and checks if it is acceptable for requesting user. if an activated public discount exists with that code, a dictionary containing informations about that discount is returned so the id can be used for an order. if an activated private user specified disount exists with that code, the system checks if it belongs to the requesting user. if so the dicount data dictionary is returned, otherwise an error response will be returned. since discounts deactivate automatically after their expiration_date (explained later), discount codes that are invalid, expired, deactivated or belong to another user will all return the same error and status code (406-not acceptable).

#### tasks

- update discount status: checks if discounts with time limit have reached their start or expiration date every 30 seconds. if so the task changes their activation status according to them. if they have reached their start date they will be activated and if they have reached their expiration date they will be deactivated.

### ----------cart module----------
#### data structure

- Cart

| Field        | Type                 | Description                                  |
|--------------|----------------------|----------------------------------------------|
| id           | UUIDField            | Unique identifier for the cart               |
| is_alive     | BooleanField         | Indicates if the cart is user's curreent cart |
| user         | ForeignKey(Profile)  | User associated with the cart, main_fk_field                |
| is_active    | BooleanField         | Indicates if the cart is active              |
| position     | PositiveIntegerField| Position of the cart           |
| created_at   | DateTimeField        | Date and time when the cart was created     |
| updated_at   | DateTimeField        | Date and time when the cart was last updated |

holds information of users' carts. this model has a custom method called total_value which calculates the total value of the cart using its items. this model's save method has been overriden in a way that only one alive cart can exist for each user at a time.

- Cart Item

| Field        | Type                  | Description                                    |
|--------------|-----------------------|------------------------------------------------|
| id           | UUIDField             | Unique identifier for the cart item            |
| food         | ForeignKey(Food)      | Food in the cart            |
| count        | PositiveIntegerField  | Quantity of the food item in the cart (min value: 1) |
| cart         | ForeignKey(Cart)      | Cart associated with the cart item, main_fk_field             |
| is_active    | BooleanField          | Indicates if the cart item is active           |
| position     | PositiveIntegerField | Position of the cart item         |
| created_at   | DateTimeField         | Date and time when the cart item was created   |
| updated_at   | DateTimeField         | Date and time when the cart item was last updated |

stores ids and number of items in each cart

The CartAdmin is the Cart & Cart Item models' admin class. This model admin is just for observing carts (specially for the purpose of managing orders) and carts can not be added or editted inside the admin pannel. It contains the CartItemInlineAdmin tabular inline admin as an inline adminstration component for observing carts and their items in a single page. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents carts' str value (user's public name - creation date), is_alive field and total value in the list view. 

#### APIs
<details>
  <summary>PUT /api/orders/add-to-cart/</summary>

#### method: PUT
#### Pernission: non staff authenticated users

#### Request body:
```json
{
  "food_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "count": 2
}
```
#### Responses:

- 200: 	
item added/removed to/from cart successfully.
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2024-03-21T07:01:58.207Z",
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "food": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "price": 12,
        "discounted_price": 10,
        "category": "string",
        "created_by": "string",
        "rate": 4,
        "ordered_count": 2,
        "is_original": true,
        "is_available": true,
        "ingredients_str": "string",
        "image_url": "string",
        "image_alt_text": "string",
        "tags": "string"
      },
      "count": 3
    }
  ],
  "total_value": 30
}
```
- 400: 	input values are invalid or don't match the expected format. possible issues:
  - count is not an int
  - food_id is not a valid uuid.

- 401: user is not authenticated

- 403: user is not allowed to perform this action on carts (is staff user)

- 404: food with specified id does not exist in requesting user's access zone
- 406: food is unavailable or too many foods of the same kind.

</details>

adds/removes an item to/from user's cart. if the user doesn't have an alive cart, the system creates one for it and then adds the items to that cart. otherwise the items will be added/removed to/from user's existing alive cart. if there is an order object refering to that cart, its status will be changed to CREATED to avoid invalid values for orders that are ready to pay (orders & their statuses will be explained more later). the food must either be in the menu (public and confirmed) or created by the requesting user. otherwise a 404 response will be returned. the food must also be available or a 406 response will be returned. if there was no problem with the food, service will try to check if a cart item refering to that food exists or not. if so the specified number of that item will be added to or removed from that cart item's count, otherwise a new cart item with that food and count will be created for user's alive cart. if the new total count is 0 or less the cart item will be deleted from the database. if the new total count is 8 or more an error will be returned because of too many items of the same kind. 

<details>
  <summary>GET /api/orders/my-cart/</summary>

#### method: PUT
#### Pernission: non staff authenticated users

#### Responses:

- 200: 	
retrieves user's alive cart
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2024-03-21T07:01:58.207Z",
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "food": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "price": 12,
        "discounted_price": 10,
        "category": "string",
        "created_by": "string",
        "rate": 4,
        "ordered_count": 2,
        "is_original": true,
        "is_available": true,
        "ingredients_str": "string",
        "image_url": "string",
        "image_alt_text": "string",
        "tags": "string"
      },
      "count": 3
    }
  ],
  "total_value": 30
}
```

- 401: user is not authenticated

- 403: user is not allowed to perform this action on carts (is staff user)

</details>

retrieves user's current alive cart. if user doesn't already have an alive cart, a new empty cart will be created for it and that will be returned as the response.


### ----------order module----------
#### data structure

- Order

| Field         | Type                    | Description                                             |
|---------------|-------------------------|---------------------------------------------------------|
| id            | UUIDField               | Unique identifier for the order                          |
| cart          | OneToOneField(Cart)     | Cart associated with the order (not editable)           |
| discount      | ForeignKey(Discount)    | Discount applied to the order (nullable)                |
| has_delivery  | BooleanField            | Indicates if the order has delivery or the user is going to receive it by going to the restaurent         |
| address       | ForeignKey(Address)     | Address associated with the order (nullable because of orders without a delivery don't need an address), on addresses deletion orders address values for refering objects will be set null            |
| address_str   | CharField               | String representation of the address, addresses' data is stored as strings inside the order objects so that if users delete ir update their addresses later, they are recorded somwhere (nullable) |
| status        | CharField(choices=STATUS_CHOICES) | Status of the order (choices: created, ready to pay, paid, rejected, in progress, delivered, default: created) |
| final_value   | FloatField              | Final value of the order after discount                                |
| is_active     | BooleanField            | Indicates if the order is active                        |
| position      | PositiveIntegerField   | Position of the order                      |
| created_at    | DateTimeField           | Date and time when the order was created                |
| updated_at    | DateTimeField           | Date and time when the order was last updated           |

holds information of the orders.

The OrderAdmin is the Order model's admin class. This model admin is just for observing orders and they can not be added or editted inside the admin pannel. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents orders' str value (cart's str value + "order"), a link to their carts' admin page, status & value in the list view. It allows filtering them by status, carts' user & final value. final value filter in the admin panel is implemented with SliderNumericFilter from admin_numeric_filter package to filter the values in a spectrum with a slider. This admin panel also allows searching orders by their str value. Finally orders can be ordered by their final value in the admin panel.

#### APIs
<details>
<summary>GET /api/orders/</summary>

##### method: GET
##### permission: authenticated users, but non staff users can only access their own orders with setting the set patameter's value to "mine"
##### parameters:
- **cart__items__food**: Must be the id of a food.
- **cart__items__food__category**: Must be the id of a food category.
- **final_value__gt**: Must be a float
- **final_value__lt**: Must be a float
- **cart__user**: Must be the id of a user profile. (only for staff users, cause non staff users only access to their own orders)
- **has_delivery**: Must be true or false.
- **is_active**: Must be true or false.
- **order_by**: Van be final_value, position, created_at, updated_at. a - symbol can be added before the param for descending order.
- **page**: Must be a valid int.
- **page_size**: Must be a valid int.
- **search**: Can be any string.
- **set**: Can be null or 'mine'.

##### responses:
- 200: Represents a list of orders.
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": {
    "ok": true,
    "data": [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "cart_user": "string",
        "has_delivery": true,
        "address": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "status": "CRT",
        "final_value": 12,
        "payments": [
          {
            "id": 2,
            "tracking_code": "string",
            "payment_data": "string"
          }
        ]
      }
    ]
  }
}
```
- 401: user is not autenticated
- 403: user doesn't have the permission (is staff user with value "mine" for set parameters or a non staff user withou value "mine" for set parameter)
</details>

returns a paginated list of orders (all of them for staff users, but for normal users only the ones created by them). API's staff purposes: recording orders, admins can see orders to manage them or change their status. API's non-staff purposes: customers can see their own orders.

The output can be filtered by these parameters: items' food, items' food category, cart user, final value (lt, gt), having delivery & activation status

Searching is available on this API. It will be done on orders' addresses, users' public names, foods' names, food categories' names

Results can also be ordered by final_value, position, created_at or updated_at ascending & descending.

<details>
  <summary>PUT /api/orders/</summary>

#### method: PUT
#### Pernission: non staff authenticated users

#### Request body:
```json
{
  "discount": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "address": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "has_delivery": true
}
```
#### Responses:

- 200: 	
order object created/updated successfully.
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "cart": {
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2024-03-21T07:01:58.207Z",
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "food": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "price": 12,
        "discounted_price": 10,
        "category": "string",
        "created_by": "string",
        "rate": 4,
        "ordered_count": 2,
        "is_original": true,
        "is_available": true,
        "ingredients_str": "string",
        "image_url": "string",
        "image_alt_text": "string",
        "tags": "string"
      },
      "count": 3
    }
  ],
    "total_value": 30
    "is_active": true,
    "position": 1,
    "created_at": "2024-03-21T07:50:30.566Z",
    "updated_at": "2024-03-21T07:50:30.566Z",
    "is_alive": true
  },
  "discount": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string",
    "description": "string",
    "code": "string",
    "expiration_date": "2024-03-21T07:50:30.566Z",
    "value": "15%"
  },
  "payments": [
    {
      "id": 0,
      "tracking_code": "string",
      "payment_data": "string"
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-21T07:50:30.566Z",
  "updated_at": "2024-03-21T07:50:30.566Z",
  "has_delivery": true,
  "address_str": "string",
  "status": "CRT",
  "final_value": 33,
  "address": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
- 400: input values are invalid or don't match the expected format. possible issues:
  - address doesn't exist or doesn't belong to user
  - invalid, expired, deactivated or belongs to another user
  - delivery order has no address

- 401: user is not authenticated

- 403: user is not allowed to perform this action on carts (is staff user)
- 406:user's current cart is empty

</details>

this API creates or updates an order object for user's current cart. takes has_delivery, discount id (result of the discount inquiry) & address id. returns information of the created/updated order. the final value is calculated with cart's total value wnd dicount (if any). if discount is larger than the total value, the final value would be 0. before saving the system automatically extracts all of the information from address object and stores them in the address_str field.

<details>
  <summary>GET /api/orders/{id}/</summary>

#### method: GET
#### Pernission: authenticated users, but non staff users can only access their own orders
- id: orders's id

#### Responses:

- 200: information of the requested order retrieved
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "cart": {
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2024-03-21T07:01:58.207Z",
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "food": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "price": 12,
        "discounted_price": 10,
        "category": "string",
        "created_by": "string",
        "rate": 4,
        "ordered_count": 2,
        "is_original": true,
        "is_available": true,
        "ingredients_str": "string",
        "image_url": "string",
        "image_alt_text": "string",
        "tags": "string"
      },
      "count": 3
    }
  ],
    "total_value": 30
    "is_active": true,
    "position": 1,
    "created_at": "2024-03-21T07:50:30.566Z",
    "updated_at": "2024-03-21T07:50:30.566Z",
    "is_alive": true
  },
  "discount": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string",
    "description": "string",
    "code": "string",
    "expiration_date": "2024-03-21T07:50:30.566Z",
    "value": "15%"
  },
  "payments": [
    {
      "id": 0,
      "tracking_code": "string",
      "payment_data": "string"
    }
  ],
  "is_active": true,
  "position": 0,
  "created_at": "2024-03-21T07:50:30.566Z",
  "updated_at": "2024-03-21T07:50:30.566Z",
  "has_delivery": true,
  "address_str": "string",
  "status": "CRT",
  "final_value": 33,
  "address": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

- 401: user is not authenticated

- 404: order with specified id does not exist in requesting user's access zone

</details>

retrieves information of a single order. staff users can access all data but normal users can only access their own orders.

<details>
  <summary>PATCH /api/orders/{id}/</summary>

#### method: PATCH
#### Permission: staff users
#### Parameters:
- id: orders's id
#### Request body:
```json
{
  "status": "RJC"
}
```
#### Responses:

- 200: order status updated successfully.

- 400: input values are invalid or don't match the expected format. e.g: input status is neither 'IPR', 'RJC', nor 'DLV'.

- 401: user is not authenticated

- 403: user is not allowed to perform this action on carts (is not staff user)

- 404: order with specified id does not exist

- 406: something about this order makes it impossible to change its status. possible issues:
  - maybe it has not been paid for yet
  -  it is delivered/rejected before
  -  it is already in that status.

</details>

this API is used by staff users to changes status of an order. the target status must be either delivered, rejected or in progress, cause other statuses should be handled automatically by system:
- created: order status automatically changes to created after creation of an order object or any modification on its cart items
- paid: order status automatically changes to paid after a payment is done by the user
- ready to pay: order status automatically changes to ready to pay after the user submits its order (explaind in the submit order API)

the order that the staff user is trying to change its status must be paid first by the user. otherwise its just a temporary object just for better the user itself (explained more in the delete dead orders task). that order's current status should not be delivered or rejected, cause their process is compeleted and changing their statuses will cause issues. obviously the targetted status should not be the same as its current status

if the staff user changes the order status to rejected, a withdrawal payment object will be created to return the money. (no payment is done its just fake data)

<details>
  <summary>PATCH /api/orders/submit-my-order/</summary>

#### method: PATCH
#### Permission: non staff authenticated users
#### Responses:

- 200: order submitted successfully.

- 401: user is not authenticated

- 403: user is not allowed to perform this action on carts (is staff user)

- 404: user doesn't have an order in 'created' status

- 406: something is wrong with user's order. e.g: order's delivery status not determined.

</details>

submits user's order. changes order's status from created to ready to pay so the order gets finalized and user can start hte payment process.

#### tasks
- delete dead orders: deletes all the orders that have been in created status for more than three hours.

### ----------payment module----------
! everything about payment module is fake, they are defined for having an integrated structure.
#### data structure

- Payment
 
| Field          | Type                  | Description                                    |
|----------------|-----------------------|------------------------------------------------|
| id             | UUIDField             | Unique identifier for the payment              |
| order          | ForeignKey(Order)     | Order associated with the payment, this is a one to mny relationship  because an order can have more than one payment object (one income payment and one withdrawal payment), main_fk_field             |
| is_income      | BooleanField          | Indicates if the payment is income or withdrawal             |
| tracking_code  | CharField             | Tracking code for the payment |
| payment_data   | TextField             | Additional payment data             |
| is_active      | BooleanField          | Indicates if the payment is active             |
| position       | PositiveIntegerField | Position of the payment           |
| created_at     | DateTimeField         | Date and time when the payment was created    |
| updated_at     | DateTimeField         | Date and time when the payment was last updated |

holds information of the payments.

The PaymentAdmin is the Payment model's admin class. This model admin is just for observing payments and they can not be added or editted inside the admin pannel. Besides the custom BaseModelAdmin functionalities inside the common app, this admin model represents payments' str value (order's str value + payment type (income or withdrawal) + "payment") & order's final value in the list view. It allows filtering them by payments' type (income or withdrawal). This admin panel also allows searching payments by their str value. Finally payments can be ordered by their order's final value, creation time & last update time in the admin panel.

#### APIs
<details>
  <summary>POST /api/orders/payments/</summary>

#### method: POST
#### Pernission: non staff authenticated users

#### Request body:
```json
{
  "order": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "tracking_code": "string",
  "payment_data": "string"
}
```
#### Responses:

- 201: 	
payment object created.
```json
{
  "order": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "tracking_code": "string",
  "payment_data": "string"
}
```
- 400: input values are invalid or don't match the expected format

- 401: user is not authenticated

- 403: user is not allowed to perform this action on payments (is staff user)

</details>

! as mentioned before this API is fake and is defined for having an integrated structure.

creates payment objects. after payment creation four things happen:
- associated order's status will change to PAID
- associated cart's is_alive value will change to false
- for each item in the cart, proper amount of its ingredients will be substracted from remaining_amount value (and then ingredients and foods that their auto_check_availability is true will be unavailable if there is no enough amount left)
- for each item in the cart, its ordered_count will be increased by th number of items existing of that food in the cart

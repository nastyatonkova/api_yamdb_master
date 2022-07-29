
## YamDB Service

The YaMDb project collects user reviews of works. 
The works are divided into categories: "Books", "Films", "Music". 
The list of categories can be expanded by the administrator.


## Technologies

- Django rest_framework
- Django rest_framework_simplejwt
- Django django_filters
- Git

## How to launch a project:

Clone the repository and go to it on the command line:
```sh
git clone git@github.com:Ivan-Maksimov/api_yamdb.git
cd api_yamdb
```


Create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/Scripts/activate
```

Install dependencies from a file requirements.txt:

```sh
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Perform migrations:

```sh
python3 manage.py migrate
```

Launch a project:

```sh
python3 manage.py runserver
```

After starting the server, you can get acquainted with the project documentation, which describes the main logic of the application, the documentation is available at the link: http://127.0.0.1:8000/redoc/


## How to upload data to a project

To load the data received with the project, we use the management command to add the data to the database via Django ORM.

The CSV files are located in the static folder. After you have done all the migrations, you can add the data from the CSV to the database by running the command in the terminal


```sh
python manage.py load-data *filename*.csv
```

### User roles
 - Anonymous — can view descriptions of works, read reviews and comments.
 - Authenticated user (user) — can read everything, as well as Anonymous, can publish reviews and rate works (films / books / songs), can comment on reviews; can edit and delete their reviews and comments, edit their ratings of works. This role is assigned by default to each new user.
 - Moderator — the same rights as an Authenticated User, plus the right to delete and edit any reviews and comments.
 - Admin — full rights to manage all the content of the project. Can create and delete works, categories and genres. Can assign roles to users.
 - The Django superuser must always have administrator rights, a user with admin rights. Even if you change the user role of the superuser, it will not deprive him of administrator rights. A superuser is always an administrator, but an administrator is not necessarily a superuser.

### User registration algorithm
 - The user sends a POST request with the email and username parameters to the endpoint /api/v1/auth/signup/.
 -The YaMDB service sends an email with a confirmation code (confirmation_code) to the specified email address.
 - The user sends a POST request with the username and confirmation_code parameters to the endpoint /api/v1/auth/token/, in response to the request he receives a token (JWT token).
 - As a result, the user receives a token and can work with the project API by sending this token with each request.
 - After registering and receiving the token, the user can send a PATCH request to the endpoint /api/v1/users/me/ and fill in the fields in his profile (the description of the fields is in the documentation at the link: http://127.0.0.1:8000/redoc/).
 
### Creating a user by an administrator
 - The user can be created by an administrator — through the site's admin zone or through a POST request to a special api endpoint/v1/users/ (the description of the request fields for this case is in the documentation).
 - - At this point, the user does not need to send an email with a confirmation code.
After that, the user must independently send his email and username to the endpoint /api/v1/auth/signup/, in response he should receive an email with a confirmation code.
 - Next, the user sends a POST request with the username and confirmation_code parameters to the endpoint /api/v1/auth/token/, in response to the request, he receives a token (JWT token), as with self-registration.

 ## Resources of the YaMDb API service
- auth: authentication.
- users: users.
- titles: works that are reviewed (a certain movie, book or song).
- categories: categories (types) of works ("Movies", "Books", "Music").
- genres: genres of works. One work can be linked to several genres.
- reviews: reviews of works. The review is tied to a specific work.
- comments: comments on reviews. The comment is linked to a specific review.

 ## Examples of requests:
> The full list of possible requests and responses can be seen after installing and running the API on the local server by `http://127.0.0.1:8000/redoc/#tag/api`

 ### 1.`POST` Adding a new category, endpoint `api/v1/categories/`:
>Permissions class: Administrator.
```sh
{
    "name": "string",
    "slug": "string"
}
```
Example of a successful response:
```sh
{
    "name": "string",
    "slug": "string"
}
```
 ### 2.`GET` Getting a list of all genres, endpoint `api/v1/genre/`:
>Permissions class: Available without token.
Example of a successful response:
```sh
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": []
    }
]
```
 ### 3. `POST` Adding a masterpiece, endpoint `api/v1/titles/`:
>Permissions class: Administrator.
```sh
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
Example of a successful response:
```sh
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
 ### 4. `POST` Adding a new review, endpoint `api/v1/titles/{title_id}/reviews/`:
>Permissions class: Authenticated users.
```sh
{
    "text": "string",
    "score": 1
}
```
Example of a successful response:
```sh
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```
 ### 5. `POST` Adding a comment to the review, endpoint `api/v1/titles/{title_id}/reviews/{review_id}/comments/`:
>Permissions class: Authenticated users.
```sh
{
    "text": "string"
}
```
Example of a successful response:
```sh
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```
 ### 6. `GET` Getting a list of all users, endpoint `api/v1/users/`:
>Permissions class: Administrator.
Example of a successful response:
```sh
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "username": "string",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "bio": "string",
                "role": "user"
            }
        ]
    }
]
```
 ### 7. `POST` New user registration, endpoint `api/v1/auth/signup/`:
>Permissions class: Available without token.
```sh
{
    "email": "string",
    "username": "string"
}
```
Example of a successful response:
```sh
{
    "email": "string",
    "username": "string"
}
```
 
## License
**Prepared by the development team: 

Ivan Maksimov [GitHub Profile](https://github.com/Ivan-Maksimov),
Petr Buikin [GitHub Profile](https://github.com/nikpup),
Anastasiia Tonkova [GitHub Profile](https://github.com/nastyatonkova)
**

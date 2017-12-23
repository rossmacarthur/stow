# stow

A simple flask app to securely PUT and GET data.

### Register a new user

**POST** to /user with payload

```
{
    "name": "Firstname Surname",
    "password": "xxxxxxxxxxxxxxxxxxx"
}
```

You will receive a token:

```
{
    "message": "User 'Firstname Surname' registered",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1MTM5NzEwNzksImV4cCI6MTUxNjU2MzA3OSwic3ViIjoxfQ.Gf4fmSowcehVGJwnw6mJW1GZC4CYUZ2FG5UfggBkrjxbtt9qtxU7hZWaAt0CnVGOkjxUcNYkFQ-66GlbXgFY7g"
}
```

Which must then be used in the `Authorization` HTTP for other endpoints.

### Store and retrieve data

**PUT** to /stow to store data
```
{
    "key": "test",
    "value": "some interesting secret data"
}
```

**GET** from /stow?key=test to retrieve data in the form
```
{
    "key": "test",
    "value": "some interesting secret data",
    "modified": "Fri, 22 Dec 2017 21:37:47 GMT"
}
```

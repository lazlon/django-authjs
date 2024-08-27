# django-authjs

django-authjs is a Django app that provides a database adapter for Auth.js

## Quick start

1. Add "authjs" to your INSTALLED_APPS setting

```python
# settings.py

INSTALLED_APPS = [
    "authjs"
]
```

2. Add authjs middleware after builtin auth middleware

```python
MIDDLEWARE = [
    ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "authjs.middleware.AuthenticationMiddleware",
    ...
]
```

3. Include the polls URLconf in your project urls.py

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("auth/", include("authjs.urls"))
]
```

3. Run `python manage.py migrate` to create the models

## Usage in Next.js

```javascript
import NextAuth from "next-auth"
import { DjangoAdapter } from "django-authjs"

export const { handlers, signIn, signOut, auth } = NextAuth({
    adapter: DjangoAdapter("http://127.0.0.1:8000/auth/"),
    providers: [],
})
```

---
layout: default
title: User Authentication
nav_order: 8
---

# User Authentication

Add the following to the bottom of the main urls.py file:

``` python
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
```

The URLs (and implicitly, views) that we just added expect to find their associated templates in a directory /registration/ somewhere in the templates search path.

Put your HTML pages in the __templates/registration/__ directory. This directory should be in your project root directory.

Create login.html (in the templates/registration directory) and fill it with:

{% raw %}
```python
{% extends "base.html" %}

{% block content %}

  {% if form.errors %}
    <p>Your username and password didn't match. Please try again.</p>
  {% endif %}

  {% if next %}
    {% if user.is_authenticated %}
      <p>Your account doesn't have access to this page. To proceed,
      please login with an account that has access.</p>
    {% else %}
      <p>Please login to see this page.</p>
    {% endif %}
  {% endif %}

  <form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <table>
      <tr>
        <td>{{ form.username.label_tag }}</td>
        <td>{{ form.username }}</td>
      </tr>
      <tr>
        <td>{{ form.password.label_tag }}</td>
        <td>{{ form.password }}</td>
      </tr>
    </table>
    <input type="submit" value="login">
    <input type="hidden" name="next" value="{{ next }}">
  </form>

  {# Assumes you setup the password_reset view in your URLconf #}
  <p><a href="{% url 'password_reset' %}">Lost password?</a></p>

{% endblock %}

```
{% endraw %}

Also, ensure that upon login the user is redirected to the home page. Add the following to the main settings.py file

```python
# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
```

Now visit [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) to make sure the tenplate works

---

Now add all the remaining auth templates:

_logged_out.html_

{% raw %}
```python
{% extends "base.html" %}

{% block content %}
  <p>Logged out!</p>
  <a href="{% url 'login'%}">Click here to login again.</a>
{% endblock %}
```
{% endraw %}

_password_reset_form.html_

{% raw %}
```python
{% extends "base.html" %}

{% block content %}
  <form action="" method="post">
  {% csrf_token %}
  {% if form.email.errors %}
    {{ form.email.errors }}
  {% endif %}
      <p>{{ form.email }}</p>
    <input type="submit" class="btn btn-default btn-lg" value="Reset password">
  </form>
{% endblock %}
```
{% endraw %}

_password_reset_done.html_

{% raw %}
```python
{% extends "base.html" %}

{% block content %}
  <p>We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder.</p>
{% endblock %}
```
{% endraw %}

_password_reset_email.html_

{% raw %}
```python
Someone asked for password reset for email {{ email }}. Follow the link below:
{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
```
{% endraw %}

_password_reset_confirm.html_

{% raw %}
```python
{% extends "base.html" %}

{% block content %}
    {% if validlink %}
        <p>Please enter (and confirm) your new password.</p>
        <form action="" method="post">
        {% csrf_token %}
            <table>
                <tr>
                    <td>{{ form.new_password1.errors }}
                        <label for="id_new_password1">New password:</label></td>
                    <td>{{ form.new_password1 }}</td>
                </tr>
                <tr>
                    <td>{{ form.new_password2.errors }}
                        <label for="id_new_password2">Confirm password:</label></td>
                    <td>{{ form.new_password2 }}</td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type="submit" value="Change my password"></td>
                </tr>
            </table>
        </form>
    {% else %}
        <h1>Password reset failed</h1>
        <p>The password reset link was invalid, possibly because it has already been used. Please request a new password reset.</p>
    {% endif %}
{% endblock %}
```
{% endraw %}

_password_reset_complete.html_

{% raw %}
```python
{% extends "base.html" %}

{% block content %}
  <h1>The password has been changed!</h1>
  <p><a href="{% url 'login' %}">log in again?</a></p>
{% endblock %}
```
{% endraw %}

Note: The password reset system requires that your website supports email. To allow testing, put the following line at the end of your __settings_dev.py__ file. This logs any emails sent to the console (so you can copy the password reset link from the console).

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

Update the base html to allow buttons for login and logout:

{% raw %}
```python
{% block sidebar %}
    <a href="{% url 'home' %}">Home</a>
    <ul class="sidebar-nav">
        {% if user.is_authenticated %}
        <li>User: {{ user.get_username }}</li>
        <li><a href="{% url 'logout' %}?next={{ request.path }}">Logout</a></li>
        {% else %}
        <li><a href="{% url 'login' %}?next={{ request.path }}">Login</a></li>
        {% endif %}
    </ul>
{% endblock %}
```
{% endraw %}

---

Now test out the different auth views to make sure everything works as expected.

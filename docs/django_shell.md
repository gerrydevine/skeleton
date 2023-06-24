---
layout: default
title: Django shell
nav_order: 10
---

# Django shell

Now that we have a model setup we are going to use the django shell to experiment with the new model.

Start up a new django shell:

```bash
$ python manage.py shell
```

First create a new User to own the record 

```python
>>> from users.models import User
```

Create a new user

```python
>>> user1 = User(email="user1@gmail.com", password="qzmpqzmp")
```

At this stage, the user has been created but not saved. To save the user (and create an id for it):

```python
>>> user1.save()
```

Check the user:

```python
>>> user1.id
1
>>> user1.email
'user1@gmail.com'
```

Now let's create a new record with the user we created

```python
>>> from records.models import Record
>>> r = Record(owner = user1, title = 'My new record', description = 'This is a description of this record', type='THES', rating=4, version=1.0)
>>> r.save()
>>> r.id
3
```

Create a few more records and users.

- Get all records (returns a queryset):

```python
>>> records = Record.object.all()
<QuerySet [<Record: This is Record 2>, <Record: This is Record 3>, <Record: This is Record 4>]>
```

- Get first record (returns an individual record instance):

```python
>>> record = Record.object.first()
<Record: This is Record 2>
```

- Get last record:

```python
>>> record = Record.object.last()
<Record: This is Record 4>
```

- Get record by id:

```python
>>> record = Record.objects.get(pk=2)
>>> record
<Record: This is Record 2>
```

- get all records belonging to user 1

```python
>>> u = User.objects.first()
>>> user_records = u.record_set.all()
<QuerySet [<Record: This is the record title>]>
```
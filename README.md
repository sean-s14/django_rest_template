# Django Skeleton

**What does this skeleton include?**
- Custom authentication with username/email login capablities
- `.env` file with variables set for sendgrid, stripe and more...
- Necessary files for Heroku (e.g. `runtime.txt`, `Procfile`, `Pipfile.lock`, etc.)

---
**Clone Repository**
```
git clone https://github.com/shaun-ps-04/django_rest_template.git .
```

Remember to uncomment `config/.env` in `.gitignore`

```bash
pipenv shell
pipenv install
py generate_sk.py  # Swap key in .env with key generated from this command
```

---
(Optional) **Include e-mails and payments**
```
pipenv install sendgrid stripe
```

---
Runserver shortcut (runs on port 9000):
```
./server.sh
```
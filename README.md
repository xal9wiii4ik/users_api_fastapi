# users_api_fastapi

### manipulations with user/authentication/permissions
1) CRUD user
2) custom jwt authentication
3) verification user using smtp
4) terminal commands

#### for create superuser:
python scripts/createsuperuser

### for create SECRET_KEY:
''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))

### main libraries: 
1) fastapi
2) alembic
3) smtplib
4) bcrypt
5) databases
6) psycopg2
7) uvicorn

### Database PostgreSQL

# date the code was written: 21.04.2021

# STARNAVI Test Task
##
List of Python libs in `requirements.txt`.

Copy `.env.example` and rename to `.env`

MySQL container was created with Docker `docker-compose.yml`

- Apply migrations `python manage.py migrate`
- Run server `python manage.py runserver 0.0.0.0:3000`
##
## Docker's command helpers
- Build\Rebuild of containers `docker-compose up --build` or `docker-compose up -d --build` add ahead `sudo` for ubuntu/linux
- Start of containers `docker-compose up` or `docker-compose up -d` add ahead `sudo` for ubuntu/linux
- Stop of containers `docker-compose down` add ahead `sudo` for ubuntu/linux
- Checking logs `docker-compose logs --tal 25`
###
## List of URLs actions
- Create User 
    - Method POST: `api/user/create`
    - DATA: `{
        'email': string,
        'password': string,
        'first_name': string,
        'last_name': string
    }`
- Login User 
    - Method POST: `api/user/login`
    - DATA: `{
        'email': string,
        'password': string
    }`
- Create Post 
    - Method POST: `api/posts`
    - DATA: `{
        'title': string,
        'description': string
    }`
- Like Post by id 
    - Method POST: `api/posts/<int:pk>/like`
- Unlike Post by id 
    - Method DELETE: `api/posts/<int:pk>/like`
##
## Command for Run AUTOMATED_BOT
- `python manage.py generate_users_and_posts`
##
## Command for Run tests
- `python manage.py generate_users_and_posts`
##

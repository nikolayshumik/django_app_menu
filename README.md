# menu_project (demo)
Minimal Django project with `tree_menu` app implementing a tree menu rendered with template tag.

## Setup
1. Clone:
   ```bash
   git clone https://github.com/nikolayshumik/django_app_menu.git
   ```
2. Cd:
   ```bash
   cd django_app_menu
   ```
3. Build a docker image:
   ```bash
    docker build -t menu_app .      
   ```
4. Run docker container:
   ```bash
    docker run -p 8000:8000 menu_app
   ```
5. Go and check:
   ```bash
   http://localhost:8000/
   ```
    Я не скрывал бд, данные и миграции уже будут созданы

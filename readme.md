# Development setup

- `python -m venv .project_env` run this first create the virtual environment for the app
- `.project_env/Scripts/activate` after creating virutal environment activate the virtual environment for the project

## Local Development Run

- `pip install -r requirements.txt`  run this to install the reuirements/dependencies for the app
- `python -m main` It will start the flask app in `development`. Suited for local development

- ### or

- `python main.py` It will start the flask app in `development`. Suited for local development

## Folder Structure

- `instance` has the sqlite DB. It can be anywhere on the machine. Configuration in  ``Main/config.py`
- `Main` is where all core requirements are gathered to run
- `.gitignore` - ignore file for repositories
- `static` - default `static` files folder. has img, css and js resources.
- `templates` - Default flask templates folder
- `templates/admin` - Templates related to the admin backend
- `templates/user` - Templates related to the User backend

```
    ├───app_admin
    │   └───__pycache__
    ├───app_show_manager
    │   └───__pycache__
    ├───app_user
    │   └───__pycache__
    ├───db_directory
    ├───instance
    ├───Main
    │   └───__pycache__
    ├───migrations
    │   └───versions
    ├───static
    │   ├───img
    │   │   ├───admin_src
    │   │   └───show_thumbnails
    │   └───js
    ├───templates
    │   ├───admin
    │   └───user
```

# Cash management system
[![Build Status](https://travis-ci.com/pulyaevskiy/test-coverage.svg?branch=master)](https://travis-ci.com/pulyaevskiy/test-coverage) [![Pub](https://img.shields.io/pub/v/test_coverage.svg?style=flat)](https://pub.dartlang.org/packages/test_coverage) ![Coverage](https://raw.githubusercontent.com/pulyaevskiy/test-coverage/master/coverage_badge.svg?sanitize=true)

Restful API for a cash management system using Django and Django Rest Framework. The system allow users to manage their cash flow by creating and updating transactions, tracking balances, and generating reports.

## Technologies

<a href="https://www.python.org/" title="python"><img src="https://logos-world.net/wp-content/uploads/2021/10/Python-Symbol.png" alt="python" height="60px"></a>
<a href="https://www.djangoproject.com/" title="django"><img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/django.svg" alt="django" height="60px"></a>
<a href="https://www.django-rest-framework.org/" title="DRF"><img style="margin-left: 10px;" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRS8k7IWwMrpA1r0AZBwKI56HBNOjpbhe6CQKip9wh0BS9H-aWX5XZt5IqR5bpFpakNthM&usqp=CAU" alt="DRF" height="60px"></a>
<a href="https://www.docker.com/" title="docker"><img style="margin-left: 10px;" src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/docker-icon.svg" alt="docker" height="60px"></a>
<a href="https://www.postgresql.org/" title="postgresql"><img style="margin-left: 10px;" src="https://www.postgresql.org/media/img/about/press/elephant.png" alt="postgresql" height="60px"></a>
<a href="https://docs.pytest.org/en/7.4.x/" title="github action"><img style="margin-left: 10px;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Pytest_logo.svg/2048px-Pytest_logo.svg.png" alt="github action" height="60px"></a>

## Setup project
1. Clone the project repository:

    ``` shell
    git clone https://github.com/MohammadMahdi-Akhondi/cash_management
    cd cash_management
    ```

2. Setup virtual environment

    ``` shell
    virtualenv .venv
    source .venv/bin/activate
    ```

3. Install dependencies

    - for development(recommended):

        ``` shell
        pip install -r requirements_dev.txt
        ```

    - for production:

        ``` shell
        pip install -r requirements.txt 
        ```

4. Build and launch the Docker environment

    - for development(recommended):

        ``` shell
        docker compose -f docker-compose.dev.yml up -d --build
        ```

    - for production:

        ``` shell
        docker compose up -d --build
        ```

5. Run project for development stage:

    ``` shell
    python manage.py runserver
    ```

## Test and coverage

``` shell
coverage run -m pytest
```

``` shell
coverage report 
```

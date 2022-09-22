FROM python:3.10

WORKDIR /code

# ENV LOCAL_LIB=/dist/python

ARG PIPENV_VER=2022.9.21
RUN pip install --root-user-action ignore "pipenv==$PIPENV_VER"

COPY src/Pipfile src/Pipfile.lock /code/
RUN pipenv install --system --deploy --ignore-pipfile --dev

# ENV PYTHONPATH=${LOCAL_LIB}

COPY ./src/ /code/

CMD ["uvicorn", "relief_worker.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

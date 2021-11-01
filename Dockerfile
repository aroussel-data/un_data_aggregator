FROM python:3.8

WORKDIR /src/

COPY . .

RUN pip install pipenv \
        && pipenv install

CMD pipenv run python -c "from acquire_data.fetcher import Fetcher; Fetcher().run()"

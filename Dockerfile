# Stage 1: Build stage
ARG PYTHON_VERSION="3.12"
FROM python:${PYTHON_VERSION}-alpine as build

WORKDIR /app

COPY . .
RUN python -m venv /opt
RUN pip install poetry==1.6.1
RUN . /opt/bin/activate &&  poetry install --no-dev --no-root

# Stage 2: Final stage
FROM python:${PYTHON_VERSION}-alpine
ENV APP_HOME /app

ENV PYTHONPATH /opt/lib/python${PYTHON_VERSION}/site-packages:${APP_HOME}
ENV PATH /opt/bin:${PATH}

COPY --from=build /opt /opt

WORKDIR $APP_HOME

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

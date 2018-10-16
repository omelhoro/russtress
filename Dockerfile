FROM clojure:lein-alpine AS frontend-builder

WORKDIR /app
COPY ./frontend/project.clj /app
RUN lein deps
COPY ./frontend /app
RUN lein uberjar

FROM python:alpine as backend-builder
WORKDIR /app
COPY ./backend /app
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
COPY --from=frontend-builder /app/resources/public ./static
CMD python webapi_blue.py;
EXPOSE 5001

FROM python:slim

LABEL "space.opengate.vendor"="SpaceRouter"
LABEL org.opencontainers.image.source https://github.com/SpaceRouter/isc-dhcp-api
LABEL space.opengate.image.authors="theo.lefevre@edu.esiee.fr"

RUN mkdir /usr/src/app/
COPY src /usr/src/app/

WORKDIR /usr/src/app/
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "isc-dhcp-api.py"]


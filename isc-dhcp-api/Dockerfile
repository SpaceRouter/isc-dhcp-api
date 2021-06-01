FROM python
MAINTAINER feloeht

RUN mkdir dhcp
RUN mkdir /usr/src/app/
COPY src /usr/src/app/

WORKDIR /usr/src/app/
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "isc-dhcp-api.py"]


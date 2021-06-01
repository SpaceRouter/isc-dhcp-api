FROM python
RUN mkdir /usr/src/app/
COPY src /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8080
RUN pip install -r requirements.txt
CMD ["python", "isc-dhcp-api.py"]


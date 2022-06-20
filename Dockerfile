FROM python:3.7-alpine
RUN pip install flask
RUN mkdir -p /home/email_service
WORKDIR /home/email_service
COPY ./send_email_service.py /home/email_service/send_email_service.py
EXPOSE 20000/tcp
ENTRYPOINT ["python", "send_email_service.py"]
#ENTRYPOINT ["tail"]
#CMD ["-f","/dev/null"]
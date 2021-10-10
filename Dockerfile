FROM python:3
WORKDIR /user/src/app
COPY . .
CMD ["call_vending_machine.py"]
ENTRYPOINT ["python3"]
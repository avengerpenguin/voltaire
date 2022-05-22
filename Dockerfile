FROM python:3

RUN pip install voltaire

CMD ["inv", "build"]

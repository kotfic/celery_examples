FROM python:2.7

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

ADD . /fib

RUN pip install -r /fib/requirements.txt

USER user
CMD ["celery", "-A", "fib", "worker", "-l", "info"]

FROM public.ecr.aws/docker/library/python:3.10.4

COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt
COPY domain ./domain
COPY main.py ./main.py

CMD [ "python", "main.py" ]
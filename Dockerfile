#
FROM muccg/python-base:ubuntu14.04-2.7
MAINTAINER https://github.com/muccg/mastr-ms

ENV DEBIAN_FRONTEND noninteractive

# Project specific deps
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpcre3 \
  libpcre3-dev \
  libpq-dev \
  libssl-dev \
  libxml2-dev \
  libxslt1-dev \
  libssl-dev \
  libsasl2-dev \
  postgresql-client-9.3 \
  python-wxgtk2.8 \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN env --unset=DEBIAN_FRONTEND

# install python deps
COPY mastrms/*requirements.txt /app/mastrms/
WORKDIR /app
RUN pip install -r mastrms/requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy code and install the app
COPY . /app
RUN pip install mdatasync_client/
RUN pip install -e mastrms

EXPOSE 8000 9000 9001 9100 9101
VOLUME ["/app", "/data"]

# stay as root user for dev
ENV HOME /data
WORKDIR /data

# entrypoint shell script that by default starts runserver
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["runserver"]

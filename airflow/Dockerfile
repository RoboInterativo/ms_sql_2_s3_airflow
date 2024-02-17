FROM apache/airflow:2.8.1
USER root
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

RUN echo """deb [arch=amd64,armhf,arm64] https://packages.microsoft.com/ubuntu/20.04/mssql-server-2022 focal main \n\
deb [arch=amd64,armhf,arm64] https://packages.microsoft.com/ubuntu/20.04/prod focal main"""  >/etc/apt/sources.list.d/mssql.list
RUN apt-get update

RUN apt-get upgrade -y
RUN apt-get -y install curl gnupg wget
# Install Kerberos
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install krb5-locales libkrb5-3 libapache2-mod-auth-gssapi

# Install config for Kerberos
RUN apt-get -y -qq install krb5-config krb5-user
RUN mkdir -p /var/run/httpd
COPY ./kerberos_conf/krb5.conf /etc/krb5.conf
RUN chmod -R 777 /var/run/httpd

#RUN apt-get -y install libodbc1 odbcinst1debian2

#RUN ACCEPT_EULA=Y apt-get install -y unixodbc-dev
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN ACCEPT_EULA=Y apt-get install -y sqlcmd

# RUN apt-get install -y netcat
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc



RUN apt-get update
# Verify the installed driver:
# RUN myodbc-installer -d -l
# If everything is ok you will see output like:
# ODBC Driver 17 for SQL Server
# MySQL ODBC 8.0 Driver
# MySQL ODBC 8.0


# # User init
# RUN mkdir -p /usr/src/home
# RUN groupadd -g 1005 hive
# RUN useradd --uid 1005 --gid 1005 --shell /bin/sh --create-home --home-dir /usr/src/home/cdc_user hive
# USER hive
# WORKDIR /usr/src/home/cdc_user
#clean
RUN apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
# Copy application and files
COPY ./requirements/common-data.txt ./requirements.txt
COPY ./test_connect.py ./

#ENV PATH=$PATH:/usr/src/home/cdc_user/.local/bin

RUN python3 -m pip install --root-user-action=ignore -r ./requirements.txt

FROM mysql:latest

# Set credentials according to your MySQL server (and .env)
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=padel
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=password

USER mysql
EXPOSE 3306

# Copy the SQL schema file
COPY schema.sql /docker-entrypoint-initdb.d/

# Use a volume to persist the database
VOLUME /var/lib/mysql

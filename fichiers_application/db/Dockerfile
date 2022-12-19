FROM mysql:8.0

# Auteur : CHAPRON Lucas

COPY ./init.sql/ /docker-entrypoint-initdb.d/
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/
EXPOSE 3306

CMD ["mysqld", "--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]

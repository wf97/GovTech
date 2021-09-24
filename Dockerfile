FROM postgres
ENV POSTGRES_PASSWORD root
ENV POSTGRES_DB test_db
WORKDIR '/'
COPY init.sql /docker-entrypoint-initdb.d/
RUN npm install
COPY . .
CMD ["npm", "run", "start", "docker", "psql"]
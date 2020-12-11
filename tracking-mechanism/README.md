## Prerequisite for the meta scheduler and placement service

* Setting up postgres docker container
~~~~
docker pull postgres:10
docker run --name metadata -e POSTGRES_PASSWORD=sealeapmetadata -p 5432:5432 -d postgres:10
sudo apt-get install postgresql-client
#load the initial metadata
psql -h localhost -U postgres < preload.sql 

#access postgres db 
psql -h localhost -U postgres

#check existing tables and inserted metadata
postgres=# \dt
postgres=# SELECT * FROM meta_db;
~~~~
* retrieving metadata from postgres - test
~~~~
python3 retrieveMetadata.py
~~~~

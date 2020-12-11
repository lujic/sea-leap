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
* retrieving metadata from postgres - TEST
~~~~
python3 retrieveMetadata.py
~~~~
* data movement tracking - TEST
~~~~
#run agent-m02.py from target node that will execute request for data management action
python3 agent-m02.py

#run migrate-data.py from meta-server (or other node) requesting data management action
python3 migrate-data.py

#check new location details in the metadata database
~~~~

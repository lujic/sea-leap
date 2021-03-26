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
#run agent-Ex_Ny.py from target edge site Ex and node Ny that will execute request for data management action
python3 agent-Ex_Ny.py

#run migrate-data.py from edge meta-server (or other nodes) requesting data management action
python3 migrate-data.py

#check new location details in the metadata database
~~~~

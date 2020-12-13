CREATE TABLE meta_db (
   ID serial PRIMARY KEY,
   datasetID VARCHAR (255) NOT NULL,
   nodeLocation VARCHAR (255) NOT NULL,
   clusterLocation VARCHAR (255) NOT NULL,
   edgeSite VARCHAR (255) NOT NULL,
   dataSize real NOT NULL,
   noFrames SMALLINT NOT NULL,
   dataPath VARCHAR (255) NOT NULL
);

INSERT INTO meta_db (datasetID, nodeLocation, clusterLocation, edgeSite, dataSize, noFrames, dataPath )
VALUES
 ('cam-intrasafed-31Dec20', 'rll-m01', 'rll-mozart', 'E1', '91.4', '600', '/data/samples/cam-intrasafed-31Dec20/'),
 ('cam-pennfudan-31Dec20', 'rll-m01', 'rll-mozart', 'E1', '25.2', '60', '/data/samples/cam-pennfudan-31Dec20/'),
 ('cam-sher-31Dec20', 'rll-m01', 'rll-mozart', 'E1', '154', '1800', '/data/samples/cam-sher-31Dec20/'), 
 ('cam-rene-31Dec20', 'rll-m01', 'rll-mozart', 'E1', '1011.8', '3600', '/data/samples/cam-rene-31Dec20/');

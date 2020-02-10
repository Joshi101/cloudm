# cloudm

This is a simple Python API service to simulate machine management in cloud. 

### Tech stack and Architecture

This service is written in Python using Flask framework. MongoDB is being used for database with flask mongoengine ODM.

The code is divided into application and domains. Domain consist of basic business units of the application. Here we only have one domain,but we can devide application into multiple domains if required. Inside Domain we define domain related models and operations. Repository layer is used to interact with the database.

 The Application layer consist of services which implement business logics which may concern one or more domains. 
  
 Flask Restful plugin is being used  to build REST APIs.
 
 The application is deployed in aws EC2. Nginx and Gunicorn are used as web server and wsgi server respectively.
 
 
 ### Making Request
 
The APIs are well documanted using swagger and can be found at http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/apidocs/ . The request can be directly made from swagger. Listing out curl syntax for the rquests.
 
##### get all regions

> curl -X GET http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/site-constants?constant=region

##### get code fot machine state and action

>curl -X GET http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/site-constants?constant=machine_state

>curl -X GET http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/site-constants?constant=machine_operation

##### get all clusters

> curl -X GET http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/clusters

##### create new cluster

> curl -X POST -H "Content-Type: application/json" --data '{"name":"cluster1","region_code":"A"}' http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/clusters

##### edit cluster name and region

> curl -X PATCH -H "Content-Type: application/json" --data '{"name":"cluster2","region_code":"B"}' http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/clusters/5e40b783fcc0917ca1b57137

##### create new machine

> curl -X POST -H "Content-Type: application/json" --data '{"name":"machine1","cluster_name":"cluster1","tags":["tag1"]}' http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/machines

##### list all machines

> curl -X GET http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/machines

##### get mahine details

> curl -X GET http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/machines/5e40b933fcc0917ca1b57138

##### edit machine name and tags

> curl -X PATCH -H "Content-Type: application/json" --data '{"name":"maxhinex"}' http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/machines/5e40b933fcc0917ca1b57138

##### run operations on machines

> curl -X POST  http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com/api/v1/machines/5e40b933fcc0917ca1b57138\?action\=STOP

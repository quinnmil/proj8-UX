# Project 8: User interface for uthenticated brevet time calculator service


Simple listing service from project 5 stored in MongoDB database. 

- Implemented by: Quinn Milionis
- Contact: qdm@uoregon.edu


#### About
- Project provides a basic user interface to create a login and access API resources.
- Main Application calculates control times for brevets. 
- This essentially replaces the calcuator at https://rusa.org/octime_acp.html with flask and ajax. 
- Subsequent updates create and maintain a database for storing these brevet times.
- Latest update allows you to create authenticated REST API-based services


- Controls are essentially "checkpoints" where a ride has to get proof of passage. The control times are the minimum and maximum times by which the rider has to arrive at the location. 
- The algorithm for calculating controle times is described at
https://rusa.org/octime_alg.html .  Additional background information
is in https://rusa.org/pages/rulesForRiders .
- Updated version in this project included two new buttons, Submit and Display. 'Submit' transmits the table data to a database, while 'Display' returns those database entires on a sepeate page.
- For this project, registering a new user and displaying tolkens can be done through cURL from a terminal window. 

## Instructions

- Navigate to the /DockerRestAPI directory in a Unix shell. 

- With docker running, use 'docker-compose build up' to build and run.

- New in Project 8: open localhost:5001 on broswer to show a basic user interface. Here create a user account can be created.

- After logging in, the user can access API resources through : <HOST>:<PORT>/[listAll] for example. 

The following was implemented for prevoious projects, but most should still work. 

- To register(use shell/terminal) :  'curl localhost:5001/api/register -d "user_name<USERNAME>&password=<PASSWORD>"'

- To get the token: curl localhost:5001/api/token -u <PASSWORD>:<USERNAME>	

- To access with auth: curl <host>:<port>/listAll?token=<token>

- To access the following RESTful services, navigae to 'localhost:5000' in a browswer with the docker-compose files running. 

- To view the Brevet calculator and add entries into the database, navigate to 'localhost:5005'

- To view a specific service, go to 'localhost:5001/SERVICE' with SERVICE replaced with any of the services described in the project description below.

- to display a set amnount of results, the url can be modified with '?top=NUM' where NUM is replaced by an integer. 

## Project Description:

 project has three parts: 

* You will design RESTful service to expose what is stored in MongoDB.
Specifically, you'll use the boilerplate given in DockerRestAPI folder, and
create the following:

   "http://<host:port>/listAll" should return all open and close times in the database
   
   "http://<host:port>/listOpenOnly" should return open times only
   
   "http://<host:port>/listCloseOnly" should return close times only

* You will also design two different representations: one in csv and one 
 in json. For the above, JSON should be your default representation. 

   "http://<host:port>/listAll/csv" should return all open and close times in CSV format
   
   "http://<host:port>/listOpenOnly/csv" should return open times only in CSV format
   
   "http://<host:port>/listCloseOnly/csv" should return close times only in CSV format

   "http://<host:port>/listAll/json" should return all open and close times in JSON format
   
   "http://<host:port>/listOpenOnly/json" should return open times only in JSON format
   
   "http://<host:port>/listCloseOnly/json" should return close times only in JSON format

* You will also add a query parameter to get top "k" open and close
times. For examples, see below.

   "http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format 
   
   "http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format

* You'll also design consumer programs (e.g., in jQuery) to use the service
  that you expose. "website" folder inside DockerRestAPI is an example of that. It is
  uses PHP. You're welcome to use either PHP or jQuery to consume your
  services. NOTE: your consumer program should be in a different container like
  example in DockerRestAPI.


# Covid Contact Tracing
> Implementation of a thesis paper which you can read from [here](https://github.com/nss10/covid-contact-tracing/blob/master/Docs/Thesis_document.pdf) which was written as a part of Master's degree program at Southern Illinois University, Carbondale. 

## About
* This is a tool which is a check-in based contact tracing system at an organizational level.
* Everytime a person enters or exits a room/public space, he is asked to scan the QR code that is placed at the entry/exit of the room. 
* Doing so would sent an event object to the backend and that event is stored in a certral database. 
* Whenever one of the user is tested positive, a medical professional is responsible to enter the user's id into the system. 
  * By making sure only a medical professional has access to insert this information we are maintaining both authenticity and confidentiality of the patient. 
* When a new user-id is inserted, the process of contact-tracing begins
* Detailed explanation of the contact tracing algorithm is mentioned in the Methodology section of the thesis dissertation document.


## Tech Stack
* Python
* MongoDB
* Flask
* Flutter

#### Back-end
* The backend of the application is the main crux of the functionality. 
* It is written in python. 
* There are different classes and methods involved in the process of contact tracing and each one of them are explained in detail in the thesis document. 
* A few of the key classes are _Agent, InfectedWindow, and Overlap._
* Flask server acts a gateway to for the front end to send "event" objects.


#### Front-end
* The front-end of this application is a mobile app built using Flutter. 
* It is a slightly customized version of a QR code scanner tool. 
* NFC scanning was a feature which was supposed to be integrated but later got pushed to the backlog. 


#### Databse
* As mentioned above, this aplication uses a NoSQL databse of Mongodb for storing and retrieving data. 
* Mongodb lets an easy way of storing and retrieving json objects which are manipulated easily by python. 

**Request analyzer**

This repo contains a tool for collecting data about requests that a website does when loaded.

By default, start.sh will create 20 processes that each make requests 
to 5000 of the domains found in top-100k.csv but the code can be configured 
to run on any list. 

Since the requests are VERY slow, as many processes as possible are desirable.
Each process needs to opperate on a different part of the list so to increase 
the number of processes, the code in start.sh needs to be changed to set number of processes and the code in main() 
needs to be changed to set the number of requests for each process.
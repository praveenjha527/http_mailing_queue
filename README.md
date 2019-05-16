# HTTP Mailing Queue
A python 3 native mailing queue with HTTP interface for job addition. A master process forks two processes, one to bind 
the http service for receiving jobs and the mailing service to pick up jobs and send them. Interprocess queues are used for
the purpose of queue maintenance.

### Setup:
* Set the following paramters in the environment
  * ALERT_EMAIL
  * ALERT_PASSWORD
  * ALERT_EMAIL_HOST
  * ALERT_EMAIL_PORT

### Running
The Service can be either run as a service using upstart, supervisor or there is a docker image attached.
```
python master.py [flags]
```
<strong>To Run Docker Image, Run the following commands:-  </strong>
```
* docker build -t mailer_app
* docker run -d mailer_app --name mailerdockerimage -p <docker_port><host_port>
```
### Flags
* -p, --port: Port for web server to bind to (default: 9999)
* -qd, ---queue-delay: Delay between subsequent job pickup by mailing worker (default: 3secs)
* -ld, --logs-directory: if logs directory is passed, logs are created in the logs directory (default: stdout)
* -fc  --file-conf: if file configuration location is passed, then the configuration precedence is given to file config over environment variables

### Web Service (Submitting jobs)
A post request to the webserver with the following json schema adds the job to the queue:-
```
{
  "sender": <sender email id>,
  "receivers": <[list of receiving mail ids]>,
  "content": <mail content>
}
```

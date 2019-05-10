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
```
python master.py [flags]
```

### Flags
* -p, --port: Port for web server to bind to (default: 9999)
* -qd, ---queue-delay: Delay between subsequent job pickup by mailing worker (default: 3secs)
* -ld, --logs-directory: if logs directory is passed, logs are created in the logs directory (default: stdout)

### Web Service (Submitting jobs)
A post request to the webserver with the following json schema adds the job to the queue:-
```
{
  "sender": <sender email id>,
  "receivers": <[list of receiving mail ids]>,
  "content": <mail content>
}
```

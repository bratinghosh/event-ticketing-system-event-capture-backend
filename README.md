# event-ticketing-system-event-capture-backend

Built using [FastAPI](https://fastapi.tiangolo.com/). 


### Purpose
- Log events for off-chain storage.
- Extract Analytics from logged events.

### Event Format - Basic
```
Event: {
  contract_id: STRING,
  wallet_id: STRING,
  ticket_id: STRING,
  timestamp: STRING,
  type: STRING,
  data: {...}
}
```

### TLDR

If you really don't want to read the [blog post](https://developer.mongodb.com/quickstart/python-quickstart-fastapi/) and want to get up and running,
activate your Python virtualenv, and then run the following from your terminal (edit the `MONGODB_URL` first!):

```bash
# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database directly or update the .env file:
export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"

# Start the service:
python3 app.py
```

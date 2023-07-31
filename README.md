# event-ticketing-system-event-capture-backend

Built using [FastAPI](https://fastapi.tiangolo.com/). 

### Purpose
- Log events for off-chain storage.
- Extract Analytics from logged events.

## MongoDB Database Pre-Setup
1. Login to MongoDB (https://account.mongodb.com/account/login).
2. Create a database and user.
3. Copy the url from the website to the `.env` file.

### Setup

If you don't want to read the [blog post](https://developer.mongodb.com/quickstart/python-quickstart-fastapi/) and want to get up and running,
activate your Python virtualenv, and then run the following from your terminal (edit the `MONGODB_URL` first!):

```bash
# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database in .env file:
DATABASE_URL=mongodb+srv://<user>:<password>@event-ticketing-system.aw7bjsx.mongodb.net/?retryWrites=true&w=majority

# Configure port in .env file:
PORT=3031

# Start the service on local machine:
python3 app.py
```

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

### <i>Name</i>: Mohammed Jakhir Hussain J
### <i>Email</i>: jakhirhussain13@gmail.com

To run the project:
* clone the project
* Fill the secrets as per .env.bak in .env file
* run docker compose up --build

### Technologies used
* Uses redis for task queue
* Celery for asynchronous task execution
* PostgreSQL for database
* Docker for containerisation
* AWS EC2 for hosting

API documentation:

Endpoint: http://18.61.61.112:8000/website/records/1/
Supported methods: Get, Post, Put, Delete
Body: {
    "site": 1,
    "name": "John Doe",
    "email": "johndoe@example.com",
    "phone": "1234567890",
    "address": "123 Main St, Sample City, Sample State",
    "country": "Country Name",
    "state": "Sample State",
    "city": "Sample City",
    "pincode": "123456",
    "dob": "1990-01-01",
    "is_active": true
}

To get records of a site: http://18.61.61.112:8000/website/records/?site_id=1&limit=3&offset=1

Endpoint: http://18.61.61.112:8000/website/sites/
Supported Methods: Get, Post, Put, Delete
Body: {
    "name": "jason",
    "domain": "https://sample.com/",
    "url": "https://sample.com/user",
    "description": "description"
}

Task initiation:
Endpoint: http://18.61.61.112:8000/website/records/1/initiate-task/
Body: {
    "task_name": "task_05"
}
Method: POST

Once this API is called the task will be executed asynchronously as per the priority.

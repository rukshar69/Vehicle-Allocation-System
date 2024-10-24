Here’s the README file with clear instructions on how to run, deploy, and maintain your project:

---

# Vehicle Allocation System - FastAPI with MongoDB

This project implements a **vehicle allocation system** using **FastAPI** and **MongoDB**. The application allows employees to allocate vehicles for a day, ensuring that no vehicle is double-booked on the same date. A **driver is pre-assigned** to each vehicle, and employees can **create, update, or delete allocations** before the allocation date. 

The project is fully **containerized with Docker**. 

## **Project Structure**
```
/app
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # Pydantic schema models
│   ├── crud.py            # CRUD operations for vehicle allocation
│   ├── database.py          # Establish MongoDB connection
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile                 # Docker configuration for FastAPI
/docker-compose.yml         # Docker Compose configuration
```

---

## **Prerequisites**
- Install **Docker Desktop** on your machine.
- Ensure that **ports 8000** (FastAPI) and **27017** (MongoDB) are available.

---

## **Running the Project**

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Build and Start the Containers**  
   Use Docker Compose to build the images and start the services:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**
   - API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)  


---



## **How to Stop the Application**
To stop the running containers:
```bash
docker-compose down
```

---


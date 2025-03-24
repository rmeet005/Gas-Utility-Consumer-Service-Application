Here is the clean **README** text without special characters:  

 Gas Utility Management System - Flask Application  

This is a simple Flask-based application for a gas utility company to manage customer service requests. The application allows users to submit service requests, track their status, and manage account information.  

 Features  

- Submit service requests with file attachments  
- Track the status of service requests  
- Basic user management  
- Rate limiting to prevent abuse  


 Tech Stack  

- Backend: Flask  
- Database: SQLite  
- ORM: SQLAlchemy  
- API Management: Flask-RESTful  
- Rate Limiting: Flask-Limiter  



 Installation Guide  

1. Clone the Repository  
    git clone https://github.com/your-repo/gas-utility-management.git  
    cd gas-utility-management  

2. Create and Activate Virtual Environment  
    python -m venv venv  
    source venv/bin/activate    (On Linux/Mac)  
    venv\Scripts\activate       (On Windows)  

3. Install Dependencies  
    pip install -r requirements.txt  

4. Run the Application  
    python app.py  

5. Database Creation  
    - A db.sqlite file will be automatically created in the project directory on the first run.  
    - It will store users and service request data.  


 API Endpoints  

1. Add User  
- URL: /add_user  
- Method: POST  
- Body (JSON)  
    {  
      "username": "testuser",  
      "password": "password123"  
    }  
- Response:  
    {  
      "message": "User added successfully",  
      "user_id": 1  
    }  


2. Submit Service Request  
- URL: /submit_request  
- Method: POST  
- Body (form-data)  
    - user_id: User ID (example: 1)  
    - request_type: Type of request (example: Gas Leakage)  
    - description: Details about the issue  
    - file: Optional file attachment  

- Response:  
    {  
      "message": "Service request submitted successfully"  
    }  


3. Track Service Request  
- URL: /track_request/<request_id>  
- Method: GET  
- Response:  
    {  
      "request_type": "Gas Leakage",  
      "status": "Pending",  
      "created_at": "2025-03-24T14:30:00",  
      "resolved_at": null  
    }  


Additional Notes  

- SQLite (db.sqlite) will be created automatically on the first run using SQLAlchemy.  
- File uploads will be stored in the uploads directory.  
- Rate limiting is applied using Flask-Limiter.  
- Customize rate limits in the app.py if needed.  


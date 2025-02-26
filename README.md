# 📚 Library Management System (Django & PostgreSQL)

A simple **Library Management System** built with **Django** and **PostgreSQL**.  
It allows users to **register, login, browse books, borrow books, and return them.**  
Administrators can **add, update, and delete books** while users can only **borrow and return books**.

---

## 🚀 Features  

✅ **User Authentication (Register/Login)**  
✅ **Browse Available Books (Public Access)**  
✅ **Borrow & Return Books (Authenticated Users Only)**  
✅ **Admin Panel for Managing Books and Users**  
✅ **Search, Filtering, and Pagination for Books**  
✅ **JWT-Based Authentication**  
✅ **Secured Against CSRF, XSS, and SQL Injection**  
✅ **Dockerized for Easy Deployment**  

---

## 🏗️ Tech Stack  

- **Backend**: Django, Django REST Framework  
- **Database**: PostgreSQL  
- **Authentication**: JWT (JSON Web Token)  
- **Containerization**: Docker & Docker Compose  

---


## 🛠️ Setup Instructions (Docker)  

### 📌 Prerequisites  
Ensure you have the following installed:  

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  

Check versions:  
```sh
docker --version  
docker-compose --version  
```

### 🚀 Clone the Repository

```sh
git clone https://github.com/piyushnakrani1/library-management-system.git  
cd library-management-system   
```

### 🚀 Environment Configuration
Create a .env file in the root directory and add:

```sh
POSTGRES_DB=library_db  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=yourpassword  
POSTGRES_HOST=db  
POSTGRES_PORT=5432     
```

### 🐳 Build & Run the Containers
```sh
docker-compose up --build -d 
```

### 📂 Apply Migrations & Create Superuser
```sh
docker exec -it django_app python manage.py migrate  
docker exec -it django_app python manage.py createsuperuser  

```

### 🔗 Access the Application
```sh
Django App: http://127.0.0.1:8000/swagger/
Admin Panel: http://localhost:8000/admin/
API Endpoints: http://localhost:8000/api/
```


### 🎯 You're all set! 🚀

Feel free to contribute or report issues!

This format is structured for GitHub, using proper markdown syntax for code blocks, links, and headers. Let me know if you need any refinements! 🚀
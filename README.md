# UrbanConnect


![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django&logoColor=white)
![GitHub repo size](https://img.shields.io/github/repo-size/suha-fathima/UrbanConnect)
![License](https://img.shields.io/badge/License-MIT-yellow)

**UrbanConnect** is a service-based marketplace web application that connects users with local professionals for home repair, cleaning, plumbing, electrical work, and more.  

---

## 🛠 Features

- Browse services across multiple categories: plumbing, cleaning, electrical, painting, and home appliances.
- Upload and view media/images for services.
- User-friendly interface with responsive design.
- Backend powered by Django and SQLite for easy setup.
- Easily extendable for additional services or functionalities.

---

## 💻 Tech Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Backend:** Python 3.12, Django 4.x
- **Database:** SQLite (local development)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

UrbanConnect/
├── manage.py                  # Django management commands
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files to ignore
├── media/                     # User-uploaded files (ignored in GitHub)
├── services/                  # App for managing services
├── urbanconnect/              # Django project settings
├── templates/                 # HTML templates
├── static/                    # CSS, JS, images
└── venv/                      # Local virtual environment (ignored)

## ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/suha-fathima/UrbanConnect.git
cd UrbanConnect

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows

3. Install dependencies:
pip install -r requirements.txt

4. Run migrations:
python manage.py migrate

5. Start the development server:
python manage.py runserver

6. Open your browser and go to http://127.0.0.1:8000/ to see the application.
```
---

## **📸 Screenshots**

- Home page  
- Services list  
- Service detail page  
- Mobile view

## **📄 License**

This project is open-source and free to use for learning purposes.

## **✉️ Contact**

Suha Fathima – [GitHub](https://github.com/suha-fathima)

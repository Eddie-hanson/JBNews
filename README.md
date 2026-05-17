# JBNews
 
### A Modern Ghanaian Digital News Platform Built with Django

JBNews is a full-stack news publishing platform designed for modern digital journalism in Ghana.  
The application provides a responsive news experience for readers while offering powerful administrative tools for editors, publishers, and media managers.

Built with Django and SQLite, JBNews includes article management, category systems, featured stories, search functionality, newsletter subscriptions, advertisement management, analytics tracking, and a responsive frontend optimized for desktop and mobile devices.

---

# ✨ About The Project

JBNews was developed as a scalable and maintainable news platform focused on delivering fast, structured, and engaging news content.

The platform enables media organizations to:

- Publish and manage articles efficiently
- Organize content by categories
- Feature breaking news and top stories
- Manage advertisements directly from the admin panel
- Track article views and ad interactions
- Allow newsletter subscriptions
- Moderate reader comments
- Deliver responsive experiences across all devices

The architecture separates presentation logic, backend operations, and content management cleanly, making the platform easy to scale and extend.

---

# 🚀 Features

## Frontend Features
- Responsive news homepage
- Breaking news section
- Featured category sliders
- Popular & latest article feeds
- Dynamic search dropdown
- Article detail pages
- Related article recommendations
- Comment submission system
- Mobile-optimized layouts
- Newsletter subscription forms
- Advertisement rendering system

## Backend Features
- Django-powered CMS architecture
- Article publishing workflow
- Draft / Published / Archived states
- Featured & prominence-based article placement
- Automatic slug generation
- Newsletter email automation
- Search relevance scoring
- Atomic article view tracking
- Advertisement click tracking
- Context processors for shared site data
- Media upload handling

## Admin Features
- Custom Django admin dashboard
- Bulk publish/archive actions
- Newsletter broadcast actions
- Ad management system
- Comment moderation
- Contact message management
- Category navigation controls
- Homepage slot availability management

---

# 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Django |
| Database | SQLite3 |
| Admin Panel | Django Admin + Jazzmin |
| Styling | Bootstrap |
| Email Service | SMTP (Gmail SMTP) |
| Image Handling | Django Media Storage |
| Search | Custom Django Query Search |
| Deployment Ready | DigitalOcean / VPS Compatible |

---

# 📁 Project Structure

```bash
JBNews/JBNews/
        ├── manage.py
        ├── .env
        ├── JBNews/
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        │
        NewsApp/
            ├── admin.py
            ├── apps.py
            ├── context_processors.py
            ├── forms.py
            ├── models.py
            ├── newsletter.py
            ├── signals.py
            ├── urls.py
            ├── views.py
        │
        ├── templates/
        ├── templatetags/
        └── static/
```

---

# ⚙️ Getting Started

## Prerequisites

Ensure the following are installed on your machine:

- Python 3.10+
- pip
- virtualenv
- Git

---

# 🔧 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Eddie-hanson/JBNews.git
cd JBNews
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv newsenv
newsenv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv newsenv
source newsenv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

> Gmail SMTP requires App Password authentication.

---

## 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 7. Run Development Server

```bash
python manage.py runserver
```

Application will run on:

```bash
http://127.0.0.1:8000/
```

Admin dashboard:

```bash
http://127.0.0.1:8000/admin/
```

---

# 🔑 Core System Features

## 📰 Article Management
- Draft, Published, and Archived article states
- Breaking news support
- Top story placement logic
- Featured article sliders
- Automatic slug generation

---

## 📧 Newsletter System
- Subscriber management
- Automatic article email notifications
- Unsubscribe token system
- HTML email templates

---

## 📢 Advertisement System
- Sidebar advertisement placements
- Click tracking
- Impression tracking
- Ad scheduling support
- Active/inactive ad states

---

## 🔍 Search System
- AJAX-powered live search
- Relevance scoring
- Category-aware filtering
- Debounced frontend requests

---

## 💬 Comment Moderation
- Reader comments
- Admin approval workflow
- Spam prevention moderation process

---

# 🖼 Gallery / UI Showcase

## Desktop Views

| Website |
|--------|
| [ ] <img width="1339" height="637" alt="image" src="https://github.com/user-attachments/assets/a4363614-d884-4467-bca4-a43ad493c186" />
 | [Categories] <img width="1358" height="632" alt="image" src="https://github.com/user-attachments/assets/bee1a31e-4f92-4eef-b223-538c27dfb8fe" />
 |[Latest News] <img width="903" height="602" alt="image" src="https://github.com/user-attachments/assets/c9abf1d0-b330-4d91-8697-3dc6b3c01d1b" /> 
 |[Popular News]<img width="889" height="534" alt="image" src="https://github.com/user-attachments/assets/783010f1-221e-4c1d-a4b3-34e2f832e488" /> |<img width="1348" height="666" alt="image" src="https://github.com/user-attachments/assets/8a0ff0b4-a0ec-4491-8c3c-fcbd30e09074" />|<img width="901" height="591" alt="image" src="https://github.com/user-attachments/assets/026a24d7-8bd6-4191-a6a4-40fe392205f0" /> 
 | [Article Page] <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/a2439789-50e4-4c1c-a1ae-43a84e282829" />, <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/0ee5456e-0f49-486b-ac53-7570aa695065" />, <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/8e22c02c-9e67-4c90-ad8f-b523b8a42aa1" />






 
---




## Mobile Views

| Mobile View |
|------------|
| 
 <img width="104" height="1280" alt="image" src="https://github.com/user-attachments/assets/bfdca62c-caa1-476f-94a3-23f2bb203f97" />,
<img width="108" height="1280" alt="image" src="https://github.com/user-attachments/assets/c12660c7-42f0-4394-b0b3-f51753ffd9aa" />,<img width="186" height="1280" alt="image" src="https://github.com/user-attachments/assets/e28503b0-9270-4f81-a86e-976ae2b637b7" /> | <img width="591" height="1280" alt="WhatsApp Image 2026-05-17 at 21 21 18" src="https://github.com/user-attachments/assets/0f05af65-60bc-48b1-88e6-6beb69946e8b" /> | <img width="152" height="1280" alt="WhatsApp Image 2026-05-17 at 21 27 52" src="https://github.com/user-attachments/assets/83ef0008-acea-43ed-ad65-a001370fb898" /> | <img width="110" height="1280" alt="WhatsApp Image 2026-05-17 at 21 31 23" src="https://github.com/user-attachments/assets/c179b59f-a15a-4abe-8f3a-e7b5c2e64cc4" /> | 



 |
[Email Notification] <img width="591" height="1280" alt="WhatsApp Image 2026-05-17 at 21 04 53" src="https://github.com/user-attachments/assets/fd75995e-5c44-490e-8233-034daefbe00c" />

---



# 📦 Deployment Notes

JBNews is deployment-ready and compatible with:

- DigitalOcean
- VPS Hosting
- Gunicorn + Nginx
- Docker-based deployments
- Cloud-hosted PostgreSQL upgrades

For production deployment:

- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL in production
- Configure static/media file serving
- Secure environment variables

---

# 🧪 Useful Commands

## Run Server

```bash
python manage.py runserver
```

## Create Migrations

```bash
python manage.py makemigrations
```

## Apply Migrations

```bash
python manage.py migrate
```

## Collect Static Files

```bash
python manage.py collectstatic
```

## Create Admin User

```bash
python manage.py createsuperuser
```

---

# 📌 Future Improvements

- REST API integration
- Real-time breaking news notifications
- Multi-author publishing system
- Analytics dashboard
- Social authentication
- AI-powered article recommendations
- Progressive Web App (PWA) support
- Cloud storage integration

---

# 🤝 Contributing

Contributions are welcome.

## Contribution Workflow

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

```text
MIT License

Copyright (c) 2026 JBNews

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

# 👨‍💻 Author

**JBNews Development Team**

Built for scalable digital journalism and modern news publishing.

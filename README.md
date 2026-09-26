<div align="center">

🎓 CampusFind

Lost. Found. Reconnected.

A campus-focused Lost & Found web platform that helps students and staff report, discover, and reconnect with lost belongings.

<br>








<br>

A simple digital solution for managing lost and found items within a campus community.

</div>

📌 Table of Contents

About the Project

Problem Statement

Solution

Objectives

Key Features

User Flow

How CampusFind Works

Technology Stack

Application Architecture

Project Structure

Database

Installation

Running the Project

Screenshots

Security

Responsive Design

Future Improvements

Learning Outcomes

Project Highlights

Author

🎯 About the Project

CampusFind is a web-based Lost & Found platform designed for college and university environments.

Students and staff can report items they have lost or found on campus. Other users can browse, search, filter, view item details, and contact the person who posted the report.

The goal is to provide one organized digital platform instead of depending on scattered messages, notice boards, or word-of-mouth communication.

Examples of items

📱 Mobile phones

💻 Laptops

🎧 Earphones

🎒 Bags

📚 Books

🪪 ID cards

🔑 Keys

👕 Clothing

🖊️ Stationery

📦 Other personal belongings

❗ Problem Statement

Lost belongings on a campus can be difficult to recover because information is often spread across different communication channels.

A student who loses an item may need to:

Ask nearby students.

Contact friends.

Post in class or department groups.

Ask faculty members.

Check with security.

Wait for someone who found the item to respond.

There is often no single place where campus members can easily publish and discover Lost & Found information.

💡 Solution

CampusFind brings the Lost & Found process into one centralized web application.

If a user loses something

Open CampusFind.

Choose I Lost Something.

Enter the item information.

Add the location and description.

Upload an image if available.

Submit the report.

Other users can discover the listing.

If a user finds something

Open CampusFind.

Choose I Found Something.

Enter the item information.

Add the location and description.

Upload an image if available.

Submit the report.

The owner can discover the listing and contact the poster.

CampusFind is designed around direct user-to-user communication.

🎯 Objectives

The main objectives of CampusFind are:

Create a centralized campus Lost & Found platform.

Make reporting lost items simple.

Make reporting found items simple.

Help users discover relevant item reports.

Provide useful information through detailed listings.

Allow users to contact item posters.

Store application data in a structured database.

Provide a clean and responsive interface.

Reduce dependence on physical notice boards and scattered messages.

Demonstrate full-stack web development using Python and Flask.

✨ Key Features

🔐 User Authentication

Users can access the application through an authentication system and maintain their session while using the platform.

🔴 Lost Item Reports

Users can create reports for items they have lost.

🟢 Found Item Reports

Users can create reports for items they have found and want to help return to the owner.

📝 Item Information

Reports can contain:

Item name

Category

Department

Color

Location

Description

Image

Lost / Found status

🖼️ Image Upload

Users can upload an image of an item when creating a report.

🔎 Search

Users can search item reports using keywords.

Example:

Search: black wallet

🗂️ Category Filters

Items can be organized into categories such as:

Devices / Electronics

Books

Bags

Clothing

Accessories

Other

📍 Location

Reports can include locations such as:

Library

Canteen

Classroom

Ground

Parking

Other

🎨 Color

Users can provide item colors such as:

Black

White

Red

Blue

Green

Other

🏫 Department

Reports can include department information such as:

BCA

BBA

CS / IT

VISCOM

BCOM

📋 Item Details

Users can open an individual report to view its complete information, including the item's description and available poster/contact information.

📞 Contact

Users can contact the person who posted an item to discuss returning or identifying the belonging.

❤️ Favorites

The application can provide a way for users to save useful reports for easier access.

🔔 Notifications

The application can support notification functionality for relevant user activities.

📱 Responsive Interface

The interface is designed to work across desktop, laptop, tablet, and mobile screen sizes.

🔄 User Flow

                 ┌─────────────────────┐
                 │   Open CampusFind   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Login / Register  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Home Page       │
                 └──────────┬──────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
          ┌──────────────┐     ┌──────────────┐
          │  Lost Item   │     │  Found Item  │
          └──────┬───────┘     └──────┬───────┘
                 │                    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │ Enter Item Details  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Upload Image     │
                 │      (Optional)     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Submit Report    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Item Listing     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Search / Filter     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    View Details     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Contact Poster    │
                 └─────────────────────┘

⚙️ How CampusFind Works

Step 1 — Authentication

The user logs into the application.

Step 2 — Browse

The home page displays available Lost and Found reports.

Step 3 — Search and Filter

Users can search for items and narrow results using available filters.

Step 4 — Report

The user chooses whether they lost or found an item and enters the required information.

Step 5 — Submit

The report is stored in the application's database.

Step 6 — Discover

Other users can browse and search published reports.

Step 7 — Details

Users can open an item to view complete information.

Step 8 — Contact

An interested user can contact the person who created the report.

🧰 Technology Stack

Technology

Purpose

HTML5

Page structure

CSS3

Styling and responsive UI

JavaScript

Client-side interactions

Python

Backend programming

Flask

Web application framework

SQLite

Database

Jinja Templates

Dynamic HTML rendering

Werkzeug

Flask utilities and security-related functionality

Git

Version control

GitHub

Source-code hosting

🏗️ Application Architecture

┌──────────────────────────────┐
│            USER              │
│      Browser / Mobile        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          FRONTEND            │
│                              │
│  HTML + CSS + JavaScript     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          FLASK               │
│          BACKEND             │
│                              │
│  Routes                      │
│  Authentication              │
│  Form Processing             │
│  Application Logic           │
│  Database Operations         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           SQLite             │
│          DATABASE            │
│                              │
│  Users / Items / Reports     │
└──────────────────────────────┘

📁 Project Structure

CampusFind/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── login.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   └── login.js
│   │
│   └── images/
│       └── jmc-logo.png
│
└── campusfind.db

campusfind.db is a local development database and should remain excluded from the public repository through .gitignore.

🗄️ Database

CampusFind uses SQLite for local data storage.

SQLite is suitable for this project because it is:

Lightweight

File-based

Easy to configure

Easy to integrate with Flask

Suitable for local development

Suitable for academic projects and prototypes

The database can store information related to users and item reports.

Example conceptual data:

Users
│
├── User information
├── Authentication information
└── Profile information

Items
│
├── Item information
├── Lost / Found status
├── Category
├── Department
├── Color
├── Location
├── Description
└── Image information

🚫 Git Ignore

Local and generated files should not be unnecessarily committed.

Example .gitignore:

*.db
*.sqlite
*.sqlite3
__pycache__/
*.pyc
.venv/
venv/
.env
static/uploads/*
uploads/*

This keeps local databases, Python cache files, virtual environments, environment files, and uploaded files out of the repository.

🚀 Installation

1. Clone the Repository

git clone https://github.com/mohamedabisn/CampusFind.git

Move into the project:

cd CampusFind

2. Create a Virtual Environment

On Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

▶️ Running the Project

Start the Flask application:

python app.py

Then open the local Flask address in your browser:

http://127.0.0.1:5000/

🖥️ Development Environment

Recommended development tools:

Visual Studio Code

Python 3.x

Flask

SQLite

Git

GitHub

Modern web browser

📸 Screenshots

Create a screenshots folder inside the project and add your actual screenshots.

Recommended structure:

screenshots/
├── campusfind-home.png
├── campusfind-login.png
├── campusfind-report.png
└── campusfind-details.png

🏠 Home Page



🔐 Login Page



📝 Report Item



📋 Item Details



If you have not added these images yet, GitHub will show broken image placeholders. Add the actual screenshot files before publishing this section.

🔐 Security

The project considers common web application security practices, including:

User authentication

Session management

Password protection

Input handling

File upload handling

Database-based data storage

Keeping sensitive local configuration outside Git

Local files such as:

.env
*.db
uploads/

should not be committed to a public repository.

📱 Responsive Design

CampusFind is designed with responsive web development principles.

The interface can adapt to:

Desktop
   ↓
Laptop
   ↓
Tablet
   ↓
Mobile

CSS layouts and media queries can be used to maintain usability across different screen sizes.

🧩 Core Modules

1. Authentication Module

Handles user login and session-related functionality.

2. Item Reporting Module

Allows users to submit Lost and Found reports.

3. Item Discovery Module

Allows users to browse, search, filter, and sort reports.

4. Item Details Module

Displays complete information about a selected report.

5. Contact Module

Allows users to communicate with the person who posted an item.

6. Database Module

Handles application data using SQLite.

7. Frontend Module

Provides the user interface using HTML, CSS, and JavaScript.

🔮 Future Improvements

Possible future improvements include:

📍 Campus map integration

📌 Location-based item discovery

💬 Built-in messaging

🔔 Improved notifications

📷 Improved image management

☁️ Cloud database deployment

☁️ Cloud image storage

👤 Enhanced user profiles

📊 User activity dashboard

🔎 Advanced search

📱 Progressive Web App support

🏫 Multi-campus support

📱 Dedicated mobile application

🎓 Learning Outcomes

Developing CampusFind provides practical experience in:

Frontend Development

HTML

CSS

JavaScript

Responsive design

UI development

Backend Development

Python

Flask

Routing

Forms

Sessions

Server-side processing

Database Development

SQLite

Database connectivity

Data storage

Data retrieval

Database-driven applications

Full-Stack Development

The project demonstrates how frontend, backend, and database components communicate:

Frontend
   ↓
Flask Backend
   ↓
SQLite Database
   ↓
Flask Response
   ↓
Frontend

Development Practices

The project also provides experience with:

Git

GitHub

Project organization

Virtual environments

Dependency management

Debugging

Local development

📌 Project Highlights

🌐 Full-Stack Web Application

CampusFind combines:

HTML
+
CSS
+
JavaScript
+
Python
+
Flask
+
SQLite

to create a complete web application.

🎯 Real-World Problem

The project addresses a practical problem faced by students and staff in educational institutions.

👥 User-Centered Approach

The platform focuses on making reporting and discovering lost belongings straightforward.

🗄️ Database Integration

The application uses a database to store and retrieve structured application data.

🧱 Scalable Foundation

The Flask-based architecture provides a foundation for future features and deployment.

🎯 Project Purpose

CampusFind was developed as a practical full-stack project to demonstrate the ability to:

Identify a real-world problem

Design a digital solution

Build a frontend

Develop a backend

Connect a database

Handle user interactions

Manage application data

Use Git and GitHub

Structure a complete software project

🌐 GitHub Repository

Repository:

https://github.com/mohamedabisn/CampusFind

Clone command:

git clone https://github.com/mohamedabisn/CampusFind.git

👨‍💻 Author

Mohamed Abis

BCA Student | Full-Stack Developer

Interests

Web Development

Python

Flask

Database Applications

UI/UX

Software Development

GitHub

https://github.com/mohamedabisn

⭐ Support

If you find CampusFind useful or interesting, consider giving the repository a ⭐ on GitHub.

<div align="center">

🎓 CampusFind

Lost. Found. Reconnected.

Built with Python, Flask, HTML, CSS, JavaScript and SQLite.

</div>

# CS50W Final Project - Capstone

# Veterinary Stock Management and Consultation System

## Distinctiveness and Complexity

This project, developed as the final project for CS50W, is a Veterinary Stock Management and Consultation System. Combining stock management, client consultation, and secretary management into a single web application. The complexity arises from the integration of various Django models, views, and templates to create a seamless system.

**Distinctive Features:**

1. **Comprehensive Stock Management:** The project includes the management of items, treatments, categories, and movements. It allows for easy addition, updating, and deletion of items and treatments, while also tracking stock levels.

2. **Secretary Dashboard:** For the secretary, there is a dedicated dashboard to view and manage client consultations. The secretary can mark consultations as paid and maintain a record of past consultations.

3. **Barcode Scanning:** The system includes a feature to search for items using barcode scanning, making it efficient for users to find and update item information.

4. **Data Serialization:** Most models have a serialize method that converts data into JSON format, making it easy to communicate with the frontend.

5. **Responsive UI:** The project uses HTML templates to provide a responsive user interface, ensuring it is accessible and functional across different devices.

6. **CRUD Functionality:** The application offers Create, Read, Update, and Delete (CRUD) operations for items, treatments, categories, and movements, adhering to Django's best practices.

## Files and Their Contents

Here is an overview of the main files and directories in the project:

- **item_track:** This is the main Django app that contains the models, views, and templates for the project.

- **item_track/models.py:** Defines the Django models for User, Item, Client, Category, Treatment, TransactionRecord, and Movements. These models represent the database structure for the application.

- **item_track/views.py:** Contains Django views for rendering HTML templates and handling various HTTP requests, such as GET and POST.

- **item_track/templates/item_track:** This directory contains HTML templates for different pages in the application, including index.html, vet.html, front_desk.html, and more.

- **item_track/urls.py:** Specifies the URL patterns and routing for the application.

- **manage.py:** The standard Django management script for running administrative tasks and managing the development server.

- **db.sqlite3:** The SQLite database file where the application's data is stored.

## Running the Application

To run this Django-based Veterinary Stock Management and Consultation System, follow these steps:

1. **Clone the Repository:** Clone this GitHub repository to your local machine using the `git clone` command.

2. **Navigate to the Project Directory:** Open your terminal or command prompt, navigate to the project's root directory, and make sure you are in the same directory as `manage.py`.

3. **Run Migrations:** Apply the database migrations to create the necessary database schema by running the following command:



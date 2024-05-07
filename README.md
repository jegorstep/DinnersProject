# Canteen Management System

This is a Canteen Management System that allows users to perform CRUD (Create, Read, Update, Delete) operations on canteen data. It consists of a Flask-based backend API for data management and a Tkinter-based GUI for the frontend interface.

## Requirements
   pip install -r requirements.txt

## Features (database)

- Read data from a CSV file and populate the database with canteen information. 

### How to use (database)?

- write down here path to your csv file and run database.py
```bash 
read_file("../canteens/Canteens.csv")  # your csv file here
```



## Features (webapp)

- Retrieve a list of canteens from the database.
- Filter canteens by open time.
- Add new canteens to the database.
- Update existing canteen information.
- Delete canteens from the database.

### How to use (webapp)?
1. Run the `webapp.py` file to start the Flask server.
2. Access the web interface by navigating to `http://127.0.0.1:5000` in your web browser.
3. Use the provided web interface to perform CRUD operations on canteen data.


## Features (GUIapp)

- Add new canteens with name, location, open time, and closed time.
- Update existing canteen information.
- Delete canteens from the system.
- View a list of canteens with options to filter by open time.

### How to use (GUIapp)?
1. Run the `webapp.py` file to start the Flask server.
2. Launch the `GUIapp.py` file to open the Tkinter-based GUI interface.
3. Use the provided interface to perform CRUD operations on canteen data.

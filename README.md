
# Project README

## Project Description
This project is a PyQt5 application integrated with a Folium map that allows users to find routes between two locations, visualize them on the map, and manage user history. It interacts with a PostgreSQL database to store user information and route history.

## Requirements
- PyQt5
- Folium
- Psycopg2
- Jinja2
- Branca

## Installation
1. Make sure you have Python 3.x installed.
2. Install required Python packages using pip:
   ```bash
   pip install requierements.txt
   ```
3. Ensure you have PostgreSQL installed and set up with a database named "projet" and required tables ("stops", "itinerary", "vehicle", "p_users", "p_history").
4. Update the database connection details in the `connect_DB` method of `MainWindow` class.
5. Run the script `main.py`.

## Usage
1. Upon running the application, you'll see the main window with various controls.
2. Use the dropdown boxes to select the user, starting point, and destination.
3. Click the "Find a way!" button to search for routes between the selected locations.
4. Routes will be displayed in the table below.
5. Double-click on a route in the table to visualize it on the map.
6. Click the "Show history" button to display the route history of the selected user.
7. Click the "Delete history" button to delete the route history of the selected user.
8. You can add a new user by clicking the "Add user" button and entering the user's name.



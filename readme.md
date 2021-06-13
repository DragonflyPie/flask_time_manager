# TimeManager

#### Video Demo: <URL HERE>

#### Description:

Time manager is web application designed to help dealing with different tasks, routines and setting long-term and short-term goals.

The application supports different users and saves information in sqlite database. Objectives are stored as:

- tasks - be done at certain date and time
- routines - to be done on certain day (days) of the week
- goals - to be done prior to certain deadline

Taks and goals support setting subobjectives.

## Pages of the application

### Lookup

Contains:

- datepicker
- tasks for the chosen date
- routines for this day of the week
- goals with deadline on or after the chosen date
- subobjectives of given tasks and goals
- tasks and goals with no date (unsorted)

Tasks and routines sorted by time.
Depending on the type of objective there are buttons for updating the objective, deleting it, making subobjective and for marking objective as done.

Main page (for logged user) is lookup page defaulted to current date.

### New objective

Form to set objective.

### Update

Form to update the contents of the objective.

### Login, register

Deal with corresponding functions.

### Welcome

Default main page for unlogged user.

## Files

### HTML files

Layout.html - flask layout for other pages.

Other files are responsible for corresponding pages, described above.

### app.py

Main file of the application. Contains:

- imports
- app configuration
- database structure
- forms for WTForms
- routes

### plans.db

Sqlite database. Accessed through flask SQLAlchemy.

### requirements.txt

List of used libraries and packages.

### style.css

Stylesheet

### app.js

Javascript script. Configurates 3 Flatpickr instances. Flatpickr - datetime picker that was used in this project. https://flatpickr.js.org/

### new.js

Javascript script, used on new.html and add.html. Changes form appearance depending on the chosen type of objective.

### favicon.png

Website icon.

## Choices and concerns

1. Technologies and components. The main concern was to make application with modern, actual methods but in the same time doable for my level of experience in computer science. Using SQLAlchemy and WTForms was a challenge, that costed me a lot of time and probably some understanding and even quality of the project.

2. Complexity. The inital idea of the application was way more complex. But in the process of developing i had to sacrifice some features.

3. Responsiveness. Styling for narrow devices was harder than i expected. The final solution not as clean as i wanted.

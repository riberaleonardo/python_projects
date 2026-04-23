# Django Data Web App

## Authors
- **Brandon Pina** — bp22c@fsu.edu  
- **Leonardo Ribera** — lr21k@fsu.edu  

---

## Overview
This project is a Django-based web application that builds on previous CIS4930 assignments.

The application analyzes a dataset of train rides in Spain and enhances it by integrating real-time weather data using geographic coordinates. Each trip record can be viewed alongside corresponding weather conditions for both departure and destination locations.

---

## Data Sources

### Dataset
- Spain Public Transportation Dataset (Kaggle):  
  https://www.kaggle.com/code/qusaybtoush1990/spain-public-transportation  

### API
- Open-Meteo Weather API:  
  https://open-meteo.com/  

- Provides free weather data in JSON format  
- No authentication required  

---

## Features

### Core Pages
- **Home**
  - Overview of the project
  - Navigation to all sections

- **Records**
  - Displays table of all train trips

- **View**
  - Detailed view of a single trip
  - Includes weather data for both locations

- **Add**
  - Create a new record

- **Edit**
  - Modify an existing record

- **Delete**
  - Remove a record

- **Analytics**
  - Visualizations based on dataset
  - Includes graphs for trip patterns

- **Admin**
  - Django admin panel for database and user management

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Load and Prepare Data
```bash
python manage.py seed_data
python manage.py fetch_data
```

---

### 6. Run Development Server
```bash
python manage.py runserver
```

---

## Screenshots
<img width="1195" height="584" alt="Screenshot 2026-04-23 at 1 15 58 PM" src="https://github.com/user-attachments/assets/708751df-ac53-42d3-90ce-795ba9a8dfe1" />
<img width="1171" height="756" alt="Screenshot 2026-04-23 at 1 16 19 PM" src="https://github.com/user-attachments/assets/cc91db8a-4b42-496b-80b5-9106d674cbf5" />
<img width="747" height="722" alt="Screenshot 2026-04-23 at 1 16 37 PM" src="https://github.com/user-attachments/assets/f92db503-6ae5-4be7-9a69-b6c38bc24534" />


---

## Notes
- This project uses server-side rendering via Django templates.
- Weather data is fetched dynamically using the Open-Meteo API.
- Designed for educational purposes and dataset exploration.

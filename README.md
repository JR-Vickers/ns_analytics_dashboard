# Network School Analytics Dashboard

A comprehensive educational data analytics dashboard built with Django and PostgreSQL, featuring interactive visualizations and data analysis tools.

## Features

- Interactive data visualizations using Plotly, Seaborn, and Matplotlib
- PostgreSQL backend for robust data storage and querying
- Real-time data analysis and statistical computations
- Customizable dashboard views
- Export functionality for data and visualizations

## Tech Stack

- Backend: Django, PostgreSQL
- Data Processing: Pandas, NumPy
- Visualization: Plotly, Seaborn, Matplotlib
- Frontend: Django Templates, JavaScript

## Setup

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure PostgreSQL:
   - Create database
   - Update settings in `ns_analytics/settings.py`

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
ns_analytics_dashboard/
├── dashboard/           # Main application
├── ns_analytics/       # Project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Development

This project is under active development. See `plan.md` for detailed progress tracking. 
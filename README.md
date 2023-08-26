# task-management

# this command is used to create the venv folder :
    python -m venv venv

# this command is used to run the project in the development mode :
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate'

# we use this command to install our used library :
    pip install Flask SQLAlchemy psycopg2 python-dotenv flask_migrate flask_sqlalchemy

# Run the following command to create the database tables:
    flask db init
    flask db migrate
    flask db upgrade

# Run the following command to start the Flask development server:
    flask run
    
    By default, the application will be accessible at `http://localhost:5000/` in your web browser.

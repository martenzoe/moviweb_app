# MovieWeb App

A web application for managing and reviewing movies, built with Flask and SQLAlchemy.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- **User management**: Add and view users
- **Movie management**: Add, update, and delete movies
- **Favorite movies**: Users can mark movies as favorites
- **Movie reviews**: Users can add reviews and ratings for movies
- **Genre management**: Add, update, and delete movie genres
- **Search functionality**: Search for movies by title or director
- **Integration with OMDb API** for fetching movie details

## Installation

### Clone the repository:
```sh
git clone https://github.com/martenzoe/moviweb_app.git
cd moviweb_app
```

### Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the required packages:
```sh
pip install -r requirements.txt
```

### Set up environment variables:
Create a `.env` file in the project root and add:
```sh
FLASK_APP=app.py
FLASK_ENV=development
OMDB_API_KEY=your_omdb_api_key
```

### Initialize the database:
```sh
flask db init
flask db migrate
flask db upgrade
```

## Usage
Run the application:
```sh
flask run
```
Open a web browser and navigate to [http://localhost:5000](http://localhost:5000).
Use the navigation menu to explore different features of the app.

## API Integration
This app uses the OMDb API to fetch movie details. Ensure you have a valid API key set in your environment variables.

## Project Structure
```
moviweb_app/
│
├── app.py
├── requirements.txt
├── README.md
│
├── instance/
│   └── moviweb_app.db
│
├── datamanager/
│   ├── __init__.py
│   ├── data_models.py
│   └── sqlite_data_manager.py
│
├── static/
│   ├── style.css
│   └── images/
│       └── MovieWeb.png
│
├── templates/
│   ├── base.html
│   ├── home.html
│   └── ...
│
└── tests/
    └── test_app.py
```

## Testing
Run the tests using pytest:
```sh
pytest
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

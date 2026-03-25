# Keerthana JM — Personal Portfolio Website

A modern, fully responsive single-page portfolio website for a BCA undergraduate student.

## Tech Stack

| Layer     | Technology                     |
|-----------|-------------------------------|
| Frontend  | HTML5, Tailwind CSS, JavaScript |
| Backend   | Python 3, Flask                |
| Database  | PostgreSQL                     |
| Icons     | Font Awesome                   |
| Fonts     | Google Fonts (Poppins, Space Grotesk) |

## Features

- Responsive single-page design (mobile + desktop)
- Dark / Light mode toggle
- Typing animation in the hero section
- Scroll reveal animations
- Animated skill progress bars
- Contact form that saves to PostgreSQL database
- Sticky navbar with active link highlighting

## Project Structure

```
portfolio-app/
├── app.py              # Flask Python backend
├── requirements.txt    # Python dependencies
└── templates/
    └── index.html      # Single-page HTML + Tailwind CSS + JS
```

## Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/keerthanajm/portfolio.git
cd portfolio/portfolio-app
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up the database
Create a PostgreSQL database and set the connection URL:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/portfolio_db"
```

### 4. Run the server
```bash
python app.py
```

Open your browser and go to `http://localhost:5000`

## API Endpoints

| Method | Endpoint   | Description                    |
|--------|------------|-------------------------------|
| GET    | `/`        | Serves the portfolio page      |
| POST   | `/contact` | Save contact form submission   |
| GET    | `/contacts`| View all contact submissions   |

## Contact Form

The contact form (Name, Email, Message) sends data to the `/contact` endpoint.  
Data is stored in a PostgreSQL database table called `contacts`.

The table is created automatically when the server starts.

## Author

**Keerthana JM**  
BCA Undergraduate Student  
Email: Keerthanamukundkeerthanamukund@gmail.com  
GitHub: [github.com/keertha2007](https://github.com/keertha2007)
LinkedIn: [linkedin.com/in/keerthana-jm](https://www.linkedin.com/in/keerthana-jm-271616384)

---
*Built as a college project using basic web development technologies.*

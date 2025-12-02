# MedAssistant

MedAssistant is a Python project designed to manage and quickly access medical-related data and functionalities. It can serve as a helpful tool for doctors, medical students, or clinics.

## Features
- Manage medical information efficiently
- Quick access to data
- Easy to extend with new modules
- Docker support for hassle-free deployment

## Requirements
- Python 3.10 or higher
- Docker (optional, for containerized execution)
- Python packages listed in `requirements.txt`

## Installation

### Using Python
1. Clone the repository:
```bash
git clone https://github.com/nimaohamdi/MedAssistant.git
cd MedAssistant

    Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

    Install dependencies:

pip install -r requirements.txt

    Run the program:

python med.py

Using Docker

docker build -t medassistant .
docker run -it --rm medassistant

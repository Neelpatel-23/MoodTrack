# MoodTrack

#### Video Demo

https://youtu.be/31qoRm8AZRE?si=NuNz4q3wtiCCs9KE

#### Description

MoodTrack is a command-line mood journaling application built with Python.

It allows users to record their moods and emotional intensity, manage
their journal entries, search through their data, view statistics and
insights, and visualize mood data using graphs.

#### Features

- Log mood journal entries
- Prevent accidental duplicate entries for the same person and date
- View journal entries with different sorting options
- Edit existing entries
- Delete journal entries
- Search entries by:
    - Name
    - Mood
    - Date
    - Minimum Intensity
    - Maximum Intensity
    - Intensity Range
- View mood statistics
- View mood insights
- Visualize mood distribution
- Visualize emotional intensity distribution
- Choose between bar graphs and pie charts
- Store journal data using JSON
- Validate user input
- Automated testing using Pytest

#### Mood Intensity

MoodTrack uses a scale from 1 to 10 for emotional intensity.

The intensity levels are grouped into three categories:
- Low: 1-3
- Moderate: 4-6
- High: 7-10


#### Visualization

MoodTrack can generate visualizations for individual users.

Users can choose between:
- Bar Graph
- Pie Chart

Two types of data can be visualized:
- Mood Distribution
- Emotional Intensity Distribution

The generated graphs are saved as PNG files.

#### Data Storage

Journal entries are stored in:
data/moods.json

Each entry contains:
- Name
- Date
- Mood
- Emotional Intensity

#### Testing

MoodTrack uses Pytest for automated testing.

The test suite covers important functionalities including:
- Loading data
- Saving data
- Finding entries by name
- Categorizing intensity
- Counting intensity categories
- Counting moods
- Validating names
- Validating dates
- Handling invalid input

The project includes a reusable Pytest fixture for sample data and uses tools
such as 'monkeypatch' and 'tmp_path' for testing input and file operations.

#### Technologies Used

- Python
- JSON
- Matplotlib
- Pytest

## Project Structure

```text
MoodTrack/
├── project.py
├── test_project.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── moods.json
└── graphs/
```

#### How to Run

Run the program using:
python project.py

To run the automated tests:
pytest

#### Git Ignore

Generated graph PNG files are excluded from version control.

#### Author

Neel

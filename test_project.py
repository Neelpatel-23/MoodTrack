import pytest
import project as pj

@pytest.fixture
def sample_data():
    return [
        {"name": "Neel", "date": "2026-01-01", "mood": "Happy", "intensity": 10},
        {"name": "Tom", "date": "2026-01-02", "mood": "Angry", "intensity": 2},
        {"name": "Neel", "date": "2026-01-03", "mood": "Energetic", "intensity": 6},
        {"name": "Sam", "date": "2026-01-04", "mood": "Sad", "intensity": 9},
        {"name": "Tom", "date": "2026-01-05", "mood": "Neutral", "intensity": 1},
        {"name": "Dex", "date": "2026-01-06", "mood": "Happy", "intensity": 7}
    ]

def test_load_data(tmp_path, monkeypatch):
    data = [
        {"name": "Neel", "date": "2026-01-01", "mood": "Happy", "intensity": 10}
    ]
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    with open("data/moods.json", "w") as file:
        pj.json.dump(data, file)
    result = pj.load_data()

    assert result == data

def test_find_entries_by_name(sample_data):
    result = pj.find_entries_by_name(sample_data, "neel")

    assert len(result) == 2
    assert result[0]["mood"] == "Happy"
    assert result[1]["mood"] == "Energetic"

@pytest.mark.parametrize(
    "intensity, expected",
    [
        (1, "Low"),
        (3, "Low"),
        (4, "Moderate"),
        (6, "Moderate"),
        (7, "High"),
        (10, "High"),
        (0, None),
        (11, None)
    ]
)
def test_intensity_category(intensity, expected):
    assert pj.intensity_category(intensity) == expected

def test_count_intensities(sample_data):
    result = pj.count_intensities(sample_data)

    assert result == {
        "Low": 2,
        "Moderate": 1,
        "High": 3
    }

def test_count_moods(sample_data):
    result = pj.count_moods(sample_data)

    assert result == {
        "Happy": 2,
        "Angry": 1,
        "Energetic": 1,
        "Sad": 1,
        "Neutral": 1
    }

def test_save_data(tmp_path, monkeypatch):
    data = [
        {"name": "Neel", "date": "2026-01-01", "mood": "Happy", "intensity": 10}
    ]
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    pj.save_data(data)
    with open("data/moods.json", "r") as file:
        saved_data = pj.json.load(file)

    assert saved_data == data

def test_get_name(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "  nEeL  ")
    assert pj.get_name() == "Neel"

def test_get_name_invalid_then_valid(monkeypatch):
    inputs = iter(["12345", "  nEeL  "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert pj.get_name() == "Neel"

def test_get_date(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2026-01-01")
    assert pj.get_date() == "2026-01-01"

def test_get_date_invalid_then_valid(monkeypatch):
    inputs = iter(["2026-99-99", "2026-01-01"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert pj.get_date() == "2026-01-01"

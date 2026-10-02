import json
from datetime import datetime
import matplotlib.pyplot as plt

def main():
    data = load_data()
    options = {
        "1" : "Log Data",
        "2" : "View Journal",
        "3" : "Delete Data",
        "4" : "Edit Data",
        "5" : "Search Data",
        "6" : "View Statistics",
        "7" : "Mood Insights",
        "8" : "Mood Visualization",
        "9" : "Exit"
    }

    while True:
        print("\nChoose your option: ")
        for num, option in options.items():
            print(f"{num}. {option}")
        choice = input("Option Number: ").strip()

        if choice == "1":
            print(log_data(data))
        elif choice == "2":
            view_journal(data)
        elif choice == "3":
            del_data(data)
        elif choice == "4":
            edit_data(data)
        elif choice == "5":
            search_data(data)
        elif choice == "6":
            view_stat(data)
        elif choice == "7":
            mood_insights(data)
        elif choice == "8":
            visualize_data(data)
        elif choice == "9":
            print("\n===== Exiting --- Thank You For Using MoodTrack --- Goodbye! =====\n")
            break
        else:
            print("\nChoose Appropriate Option Number")

def load_data():
    try:
        with open("data/moods.json", "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def log_data(data):
    name = get_name()
    date = get_date()

    existing = [
        item for item in find_entries_by_name(data, name)
        if item["date"] == date
    ]
    if existing:
        print("\n--- An Entry For This Person Already Exists On This Date ---")
        while True:
            choice = input("Continue anyway? (y/n): ").strip().lower()
            if choice == "y":
                break
            elif choice == "n":
                return "\n--- Data Not Saved ---"
            else:
                print("Choose 'y' or 'n'")

    mood = get_mood()
    intensity = get_intensity()

    entry = {
    "name" : name,
    "date" : date,
    "mood" : mood,
    "intensity" : intensity
    }

    data.append(entry)
    save_data(data)
    return "\n--- Data Saved ---"

def view_journal(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    view_options = {
        "1": "Date - Newest to Oldest",
        "2": "Date - Oldest to Newest",
        "3": "Name - A to Z",
        "4": "Name - Z to A",
        "5": "Intensity - Highest to Lowest",
        "6": "Intensity - Lowest to Highest"
    }

    while True:
        print("\n===== JOURNAL VIEW =====")
        for num, option in view_options.items():
            print(f"{num}. {option}")
        choice = input("Option Number: ").strip()

        if choice == "1":
            sorted_data = sorted(data, key = lambda item: item["date"], reverse = True)
            break
        elif choice == "2":
            sorted_data = sorted(data, key = lambda item: item["date"])
            break
        elif choice == "3":
            sorted_data = sorted(data, key = lambda item: item["name"].lower())
            break
        elif choice == "4":
            sorted_data = sorted(data, key = lambda item: item["name"].lower(), reverse = True)
            break
        elif choice == "5":
            sorted_data = sorted(data, key = lambda item: item["intensity"], reverse = True)
            break
        elif choice == "6":
            sorted_data = sorted(data, key = lambda item: item["intensity"])
            break
        else:
            print("\nChoose Appropriate Option Number")

    print("\n===== YOUR JOURNAL =====")
    display_entries(sorted_data, "Total Entries")
    print("\n====================")

def del_data(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    while True:
        try:
            num = int(input("\nEnter Entry Number to Delete: "))
            if 1 <= num <= len(data):
                sorted_data = sorted(data, key = lambda item: item["date"], reverse = True)
                entry = sorted_data[num - 1]
                index = data.index(entry)
                removed = entry

                print("\n===== SELECTED ENTRY =====")
                print(f"Date: {removed['date']}")
                print(f"Name: {removed['name']}")
                print(f"Mood: {removed['mood']}")
                print(f"Intensity: {removed['intensity']}/10")
                print("====================")

                while True:
                    confirm = input("Delete this entry (y/n): ").strip().lower()
                    if confirm == "y":
                        data.pop(index)
                        save_data(data)
                        print(f"\n--- Entry Deleted ---")
                        break
                    elif confirm == "n":
                        print("\n--- Deletion Cancelled ---")
                        break
                    else:
                        print("Choose 'y' or 'n'")
                return
        except ValueError:
                pass
        print("\nChoose Appropriate Entry Number")

def edit_data(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    while True:
        try:
            num = int(input("\nEnter Entry Number to Edit: "))
            if 1 <= num <= len(data):
                sorted_data = sorted(data, key = lambda item:  item["date"], reverse = True)
                entry = sorted_data[num - 1]
                index = data.index(entry)

                print("\n===== SELECTED ENTRY =====")
                print(f"Date: {entry['date']}")
                print(f"Name: {entry['name']}")
                print(f"Mood: {entry['mood']}")
                print(f"Intensity: {entry['intensity']}/10")
                print("====================")

                while True:
                    confirm = input("\nEdit this entry? (y/n):").strip().lower()
                    if confirm == "y":
                        break
                    elif confirm == "n":
                        print("\n--- Edit Cancelled ---")
                        return
                    else:
                        print("Choose 'y' or 'n'")

                edit_options = {
                    "1": "Name",
                    "2": "Date",
                    "3": "Mood",
                    "4": "Intensity",
                    "5": "Save Changes"
                }

                while True:
                    print("\n===== EDIT ENTRY =====")
                    for option, field in edit_options.items():
                        print(f"{option}. {field}")
                    choice = input("Option Number: ").strip()

                    if choice == "1":
                        entry["name"] = get_name()
                        print("\n--- Name Updated ---")
                    elif choice == "2":
                        entry["date"] = get_date()
                        print("\n--- Date Updated ---")
                    elif choice == "3":
                        entry["mood"] = get_mood()
                        print("\n--- Mood Updated ---")
                    elif choice == "4":
                        entry["intensity"] = get_intensity()
                        print("\n--- Intensity Updated ---")
                    elif choice == "5":
                        duplicate = any(
                            item is not entry
                            and item["name"].lower() == entry["name"].lower()
                            and item["date"] == entry["date"]
                            for item in data
                        )
                        if duplicate:
                            print("\n--- An Entry For This Person Already Exists On This Date ---")
                            print("--- Change Not Saved ---")
                            continue
                        save_data(data)
                        print("\n--- Data Updated ---")
                        return
                    else:
                        print("\nChoose Appropriate Option Number")

        except ValueError:
            pass
        print("\nChoose Appropriate Entry Number")

def search_data(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    search_options = {
        "1": "Search by Name",
        "2": "Search by Mood",
        "3": "Search by Date",
        "4": "Search by Minimum Intensity",
        "5": "Search by Maximum Intensity",
        "6": "Search by Intensity Range"
    }

    while True:
        print("\n===== SEARCH OPTIONS =====")

        for num, option in search_options.items():
            print(f"{num}. {option}")

        choice = input("Option Number: ").strip()

        if choice == "1":
            search = input("\nEnter Name: ").strip().lower()
            results = [
                item for item in data
                if search in item["name"].lower()
            ]
            break

        elif choice == "2":
            search = input("\nEnter Mood: ").strip().lower()
            results = [
                item for item in data
                if search in item["mood"].lower()
            ]
            break

        elif choice == "3":
            search = input("\nEnter Date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(search, "%Y-%m-%d")
            except ValueError:
                print("\n--- Invalid Date ---")
                return
            results = [
                item for item in data
                if item["date"] == search
            ]
            break

        elif choice == "4":
            try:
                minimum = int(input("\nEnter Minimum Intensity (1-10): "))
                if not 1 <= minimum <= 10:
                    print("\nEnter Appropriate Number Between 1 & 10")
                    return
            except ValueError:
                print("\nEnter Appropriate Number")
                return
            results = [
                item for item in data
                if item["intensity"] >= minimum
            ]
            break

        elif choice == "5":
            try:
                maximum = int(input("\nEnter Maximum Intensity (1-10): "))
                if not 1 <= maximum <= 10:
                    print("\nEnter Appropriate Number Between 1 & 10")
                    return
            except ValueError:
                print("\nEnter Appropriate Number")
                return
            results = [
                item for item in data
                if item["intensity"] <= maximum
            ]
            break

        elif choice == "6":
            try:
                minimum = int(input("\nEnter Minimum Intensity (1 - 10): "))
                maximum = int(input("Enter Maximum Intensity (1 - 10): "))
                if not 1 <= minimum <= 10 or not 1 <= maximum <= 10:
                    print("\nEnter Appropriate Numbers Between 1 & 10")
                    return
                if minimum > maximum:
                    print("\n--- Minimum Cannot Be Greater Than Maximum ---")
                    return
            except ValueError:
                print("\nEnter Appropriate Numbers")
                return
            results = [
                item for item in data
                if minimum <= item["intensity"] <= maximum
            ]
            break

        else:
            print("\nChoose Appropriate Option Number")

    if not results:
        print("\n--- No Matching Entries Found ---")
        return

    print("\n===== SEARCH RESULTS =====")
    display_entries(results, "Matching Entries")
    print("\n====================")


def view_stat(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    name = input("\nEnter Name: ").strip().lower()
    user_data = find_entries_by_name(data, name)
    if not user_data:
        print("\n--- No Data Found For This Name ---")
        return

    intensities = [item["intensity"] for item in user_data]
    total_entries = len(user_data)
    avg_intensity = sum(intensities)/total_entries
    highest_entry = max(user_data, key = lambda item: item["intensity"])
    lowest_entry = min(user_data, key = lambda item: item["intensity"])

    mood_count = count_moods(user_data)
    most_common_mood = max(mood_count, key = mood_count.get)
    most_common_count = mood_count[most_common_mood]
    most_common_percentage = most_common_count / total_entries * 100
    unique_moods = len(mood_count)
    total_moods = 20
    mood_variety = unique_moods / total_moods * 100

    intensity_count = count_intensities(user_data)
    low_intensity = intensity_count["Low"]
    moderate_intensity = intensity_count["Moderate"]
    high_intensity = intensity_count["High"]

    print("\n===== MOOD STATISTICS =====")
    print(f"Name: {user_data[0]['name']}")

    print(f"\nTotal Entries: {total_entries}")
    print(f"Average Intensity: {avg_intensity:.1f}/10")
    print(f"Highest Intensity: {highest_entry['intensity']}/10 ({highest_entry['mood']})")
    print(f"Lowest Intensity: {lowest_entry['intensity']}/10 ({lowest_entry['mood']})")

    print(f"\nDifferent Moods Recorded: {unique_moods}/{total_moods}")
    print(f"Mood Variety: {mood_variety:.1f}%")
    print(f"Most Common Mood: {most_common_mood} ({mood_count[most_common_mood]} times, {most_common_percentage:.1f}%)")

    print("\nMood Distribution:")
    for mood, count in mood_count.items():
        percentage = count / total_entries * 100
        if count > 1:
            print(f"{mood}: {count} entries ({percentage:.1f}%)")
        elif count == 1:
            print(f"{mood}: {count} entry ({percentage:.1f}%)")

    print("\nIntensity Distribution:")
    print(f"1-3: {low_intensity} entries")
    print(f"4-6: {moderate_intensity} entries")
    print(f"7-10: {high_intensity} entries")
    print("====================")

def mood_insights(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    name = input("\nEnter Name: ").strip().lower()
    user_data = find_entries_by_name(data, name)
    if not user_data:
        print("\n--- No Data Found For This Name ---")
        return
    intensities = [item["intensity"] for item in user_data]
    avg_intensity = sum(intensities) / len(intensities)

    intensity_count = count_intensities(user_data)
    low_intensity = intensity_count["Low"]
    moderate_intensity = intensity_count["Moderate"]
    high_intensity = intensity_count["High"]

    mood_count = count_moods(user_data)
    most_common_mood = max(mood_count, key = mood_count.get)
    unique_moods = len(mood_count)
    total_moods = 20
    mood_variety = unique_moods / total_moods * 100
    most_common_count = mood_count[most_common_mood]
    total_entries = len(user_data)
    common_percentage = most_common_count / total_entries * 100

    print("\n===== MOOD INSIGHTS =====")
    print(f"Name: {user_data[0]['name']}")
    print(f"\nYour most frequently recorded mood is {most_common_mood}.")
    print(f"It represents {common_percentage:.1f}% of your recorded entries.")

    if mood_variety >= 75:
        print("Your recorded moods cover a very broad range of the available moods.")
    elif mood_variety >= 50:
        print("Your recorded moods cover a fairly broad range of the available moods.")
    elif mood_variety >= 25:
        print("Your recorded moods cover a moderate range of the available moods.")
    else:
        print("Your recorded moods cover a relatively small range of the available moods.")

    print(f"\nYour average emotional intensity is {avg_intensity:.1f}/10.")

    if avg_intensity >= 8:
        print("Your emotional intensity has been quite intense.")
    elif avg_intensity >= 5:
        print("Your emotional intensity has generally been moderate.")
    else:
        print("Your emotional intensity has generally been relatively low.")

    if high_intensity > moderate_intensity and high_intensity > low_intensity:
        print("Most of your recorded entries have high emotional intensity.")
    elif moderate_intensity > high_intensity and moderate_intensity > low_intensity:
        print("Most of your recorded entries have moderate emotional intensity.")
    elif low_intensity > high_intensity and low_intensity > moderate_intensity:
        print("Most of your recorded entries have low emotional intensity.")
    else:
        print("Your recorded entries have a relatively balanced intensity distribution.")
    print("\n====================")

def visualize_data(data):
    if not data:
        print("\n--- Journal is Empty ---")
        return

    names = sorted(set(item["name"] for item in data))
    while True:
        print("\n===== SELECT PERSON =====")
        for num, name in enumerate(names, start = 1):
            print(f"{num}. {name}")
        print(f"{len(names) + 1}. Back")

        while True:
            try:
                choice = int(input("\nChoose Person Number To Visualize: "))
                if 1 <= choice <= len(names):
                    selected_name = names[choice - 1]
                    break
                elif choice == len(names) + 1:
                    return
                else:
                    print("\nChoose Appropriate Person Number")
            except ValueError:
                print("Enter Appropriate Number")

        person_data = [
            item for item in data
            if item["name"] == selected_name
            ]

        while True:
            print("\n===== VISUALIZATION =====")
            print("1. Mood Distribution")
            print("2. Intensity Distribution")
            print("3. Back")
            choice = input("Option Number: ").strip()

            if choice == "1":
                mood_distribution(person_data, selected_name)
            elif choice == "2":
                intensity_distribution(person_data, selected_name)
            elif choice == "3":
                break
            else:
                print("\nChoose Appropriate Option Number")

def chart_type_selection():
    while True:
        print("\n===== CHART TYPE =====")
        print("1. Bar Graph")
        print("2. Pie Chart")
        print("3. Back")
        choice = input("Option Number: ").strip()

        if choice in ["1", "2"]:
            return choice
        elif choice == "3":
            return None
        else:
            print("\nChoose Appropriate Option Number")

def mood_distribution(entries, name):
    mood_count = count_moods(entries)

    chart_type = chart_type_selection()
    if chart_type is None:
        return

    moods = list(mood_count.keys())
    counts = list(mood_count.values())
    plt.figure(figsize = (10, 6))

    if chart_type == "1":
        plt.bar(moods, counts)
        plt.xlabel("Mood")
        plt.ylabel("Number of Entries")
        filename = f"graphs/{name}'s_mood_distribution_bar.png"
    elif chart_type == "2":
        plt.pie(counts, labels = moods, autopct = "%1.1f%%")
        filename = f"graphs/{name}'s_mood_distribution_pie.png"

    plt.title(f"Mood Distribution - {name}")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"\n--- Graph saved as {filename} ---")

def intensity_distribution(entries, name):
    intensity_count = count_intensities(entries)
    chart_type = chart_type_selection()
    if chart_type is None:
        return

    categories = list(intensity_count.keys())
    counts = list(intensity_count.values())
    plt.figure(figsize = (10, 6))

    if chart_type == "1":
        plt.bar(categories, counts)
        plt.xlabel("Emotional Intensity")
        plt.ylabel("Number of Entries")
        filename = f"graphs/{name}'s_intensity_distribution_bar.png"
    elif chart_type == "2":
        plt.pie(counts, labels = categories, autopct = "%1.1f%%")
        filename = f"graphs/{name}'s_intensity_distribution_pie.png"

    plt.title(f"Emotional Intensity Distribution - {name}")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"\n--- Graph saved as {filename} ---")

def display_entries(entries, message):
    print(f"\n{message}: {len(entries)}")
    for num, item in enumerate(entries, start = 1):
        print(f"\nEntry#{num}")
        print(f"Date: {item['date']}")
        print(f"Name: {item['name']}")
        print(f"Mood: {item['mood']}")
        print(f"Intensity: {item['intensity']}/10")
        print("--------------------")

def find_entries_by_name(data, name):
    name = name.strip().lower()
    return [
        item for item in data
        if item["name"].lower() == name
    ]

def intensity_category(intensity):
    if 1 <= intensity <= 3:
        return "Low"
    elif 4 <= intensity <= 6:
        return "Moderate"
    elif 7 <= intensity <= 10:
        return "High"
    return None

def count_intensities(entries):
    intensity_count = {
        "Low": 0,
        "Moderate": 0,
        "High": 0
    }

    for item in entries:
        category = intensity_category(item["intensity"])
        if category:
            intensity_count[category] += 1
    return intensity_count

def count_moods(entries):
    mood_count = {}

    for item in entries:
        mood = item["mood"]
        mood_count[mood] = mood_count.get(mood, 0) + 1
    return mood_count

def save_data(data):
    with open("data/moods.json", "w") as file:
        json.dump(data, file, indent = 4)

def get_name():
    while True:
        name = input("Name: ").strip()

        if name and all(char.isalpha() or char.isspace() for char in name):
            return name.title()
        print("Enter Appropriate Name")

def get_date():
    while True:
        date = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Enter Appropriate Date")

def get_mood():
    moods = {
        "1" : "Happy",
        "2" : "Sad",
        "3" : "Angry",
        "4" : "Calm",
        "5" : "Excited",
        "6" : "Anxious",
        "7" : "Tired",
        "8" : "Grateful",
        "9" : "Neutral",
        "10" : "Confident",
        "11" : "Stressed",
        "12" : "Lonely",
        "13" : "Bored",
        "14" : "Motivated",
        "15" : "Frustrated",
        "16" : "Peaceful",
        "17" : "Hopeful",
        "18" : "Proud",
        "19" : "Confused",
        "20" : "Energetic",
        }

    while True:
        print("\nChoose your mood: ")
        for num, mood in moods.items():
            print(f"{num}. {mood}")
        choice = input("Mood Number: ").strip()
        if choice in moods:
            return moods[choice]
        else:
            print("Choose Appropriate Mood Number")

def get_intensity():
    while True:
        try:
            intensity = int(input("Emotional Intensity (1-10): "))
            if 1 <= intensity <= 10:
                return intensity
        except ValueError:
            pass
        print("Enter Appropriate Number Between 1 & 10")

if __name__ == "__main__":
    main()

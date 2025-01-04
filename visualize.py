import matplotlib.pyplot as plt
from crud import get_students

def generate_score_chart():
    students = get_students()
    print("Retrieved students:", students)  # Debugging line

    if not students:  # Check if students list is empty
        print("No students found!")
        return

    try:
        # Extract names and scores
        names = [s["name"] for s in students]
        scores = [float(s["score"]) for s in students]

        print("Names:", names)  # Debugging log
        print("Scores:", scores)  # Debugging log

        # Create the bar chart
        plt.figure(figsize=(10, 6))  # Adjust size for clarity
        plt.bar(names, scores, color='blue')
        plt.xlabel("Students")
        plt.ylabel("Scores")
        plt.title("Student Performance")
        plt.xticks(rotation=45)  # Rotate names for better visibility
        plt.tight_layout()  # Prevent clipping of labels
        plt.savefig("score_chart.png")
        print("Chart saved as score_chart.png")
    except Exception as e:
        print(f"Error generating chart: {e}")
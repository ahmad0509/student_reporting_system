import matplotlib.pyplot as plt
from crud import get_students

def generate_score_chart():
    students = get_students()
    
    if not students:
        print("No students found!")
        return

    try:
        # Extract names and average scores from science_total and math_total
        names, scores = zip(*[
            (s["name"], (float(s.get("science_total", 0)) + float(s.get("math_total", 0))) / 2)
            for s in students
        ])

        # Create and save the chart
        plt.figure(figsize=(10, 6))
        plt.bar(names, scores, color='blue')
        plt.xlabel("Students")
        plt.ylabel("Average Score")
        plt.title("Student Performance (Math & Science)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("score_chart.png")

        print("Chart saved as score_chart.png")
    except Exception as e:
        print(f"Error generating chart: {e}")

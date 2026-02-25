import csv
from statistics import mean, median

snake_days = []
no_snake_days = []

with open("garden_simulation_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        day = int(row["day_of_fall"])
        if row["snake_present"] == "True":
            snake_days.append(day)
        else:
            no_snake_days.append(day)

def summarize(days, label):
    print(f"\n--- {label} ---")
    print(f"Average day of fall: {mean(days):.2f}")
    print(f"Median day of fall: {median(days)}")
    print(f"Min day of fall: {min(days)}")
    print(f"Max day of fall: {max(days)}")
    print(f"Total runs: {len(days)}")

summarize(snake_days, "With Snake")
summarize(no_snake_days, "Without Snake")

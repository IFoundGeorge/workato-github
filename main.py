import random
import csv

class Agent:
    def __init__(self, name, curiosity, obedience, awareness=0, trust_authority=1.0, trust_other=1.0):
        self.name = name
        self.curiosity = curiosity
        self.obedience = obedience
        self.awareness = awareness
        self.trust_authority = trust_authority
        self.trust_other = trust_other
        self.has_touched_tree = False

    def natural_drift(self):
        self.curiosity = min(10, self.curiosity + random.uniform(0, 0.3))
        self.obedience = max(0, self.obedience - random.uniform(0, 0.1))

    def social_influence(self, other):
        influence = (other.curiosity - other.obedience) * 0.1 * self.trust_other
        self.curiosity = min(10, self.curiosity + max(0, influence))

    def reflect(self):
        if self.curiosity > self.obedience:
            self.awareness = min(10, self.awareness + random.uniform(0.1, 0.3))

    def evaluate_decision(self, temptation=0):
        pressure = self.curiosity + temptation - self.obedience
        threshold = random.uniform(0, 10)
        return pressure > threshold

class Snake:
    def __init__(self, persuasion=2.0, chance_per_day=0.6):
        self.persuasion = persuasion
        self.chance_per_day = chance_per_day

    def interact(self, agent):
        if random.random() < self.chance_per_day:
            agent.curiosity = min(10, agent.curiosity + self.persuasion)
            agent.trust_authority = max(0, agent.trust_authority - 0.05)

class Garden:
    def __init__(self, snake_present=True):
        self.day = 1
        self.snake = Snake() if snake_present else None
        # Start Adam and Eve completely fresh
        self.adam = Agent("Adam", curiosity=0, obedience=0, awareness=0, trust_authority=0, trust_other=0)
        self.eve = Agent("Eve", curiosity=0, obedience=0, awareness=0, trust_authority=0, trust_other=0)

    def simulate_day(self):
        self.adam.natural_drift()
        self.eve.natural_drift()

        if self.snake:
            self.snake.interact(self.eve)

        self.adam.reflect()
        self.eve.reflect()

        self.adam.social_influence(self.eve)
        self.eve.social_influence(self.adam)

        for agent in [self.eve, self.adam]:
            if not agent.has_touched_tree and agent.evaluate_decision():
                agent.has_touched_tree = True
                return True, agent.name  # Simulation ends

        return False, None

    def run(self):
        while True:
            fallen, who = self.simulate_day()
            if fallen:
                return self.day, who
            self.day += 1

# ---------------- RUN 500 SIMULATIONS ----------------
def run_multiple_simulations(num_runs=500, snake_present=True):
    results = []
    for i in range(num_runs):
        garden = Garden(snake_present=snake_present)
        day, who = garden.run()
        results.append({
            "run": i+1,
            "day_of_fall": day,
            "who_touched_first": who,
            "snake_present": snake_present
        })
    return results

# Run simulations with and without snake
results_with_snake = run_multiple_simulations(500, snake_present=True)
results_without_snake = run_multiple_simulations(500, snake_present=False)

# Combine all results
all_results = results_with_snake + results_without_snake

# Save to CSV for analysis
with open("garden_simulation_results.csv", "w", newline="") as csvfile:
    fieldnames = ["run", "day_of_fall", "who_touched_first", "snake_present"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_results)

print("500 simulations completed for each condition. Results saved to garden_simulation_results.csv")

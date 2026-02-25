import random
import csv

class Agent:
    def __init__(self, name, curiosity=None, obedience=None, awareness=0, trust_authority=1.0, trust_other=1.0):
        self.name = name
        self.curiosity = curiosity if curiosity is not None else random.uniform(3, 7)
        self.obedience = obedience if obedience is not None else random.uniform(3, 7)
        self.awareness = awareness
        self.trust_authority = trust_authority
        self.trust_other = trust_other
        self.has_touched_tree = False

    def natural_drift(self):
        # Natural curiosity growth and obedience decay
        self.curiosity = min(10, self.curiosity + random.uniform(0, 0.5))
        self.obedience = max(0, self.obedience - random.uniform(0, 0.2))

    def social_influence(self, other):
        # Influence based on difference in curiosity/obedience and trust in others
        influence = (other.curiosity - self.curiosity) * 0.1 * self.trust_other
        self.curiosity = min(10, max(0, self.curiosity + influence))

    def reflect(self):
        # Awareness grows if curiosity exceeds obedience
        if self.curiosity > self.obedience:
            self.awareness = min(10, self.awareness + random.uniform(0.05, 0.25))

    def evaluate_decision(self, temptation=0):
        # More sophisticated decision: curiosity + temptation - obedience, mitigated by awareness
        pressure = self.curiosity + temptation - self.obedience
        risk_factor = max(0, 10 - self.awareness)  # higher awareness reduces risk-taking
        threshold = random.uniform(0, 10) * (risk_factor / 10)
        return pressure > threshold

class Snake:
    def __init__(self, persuasion=1.5, chance_per_day=0.5):
        self.persuasion = persuasion
        self.chance_per_day = chance_per_day

    def interact(self, agent):
        if random.random() < self.chance_per_day:
            # Influence scaled by trust in authority and remaining curiosity room
            agent.curiosity = min(10, agent.curiosity + self.persuasion * agent.trust_authority)
            agent.trust_authority = max(0, agent.trust_authority - 0.03)

class Garden:
    def __init__(self, snake_present=True):
        self.day = 1
        self.snake = Snake() if snake_present else None
        self.agents = [
            Agent("Adam", trust_authority=0.5, trust_other=0.5),
            Agent("Eve", trust_authority=0.5, trust_other=0.5)
        ]

    def simulate_day(self):
        # Shuffle agents to avoid order bias
        random.shuffle(self.agents)

        # Natural drift
        for agent in self.agents:
            agent.natural_drift()

        # Snake interaction
        if self.snake:
            self.snake.interact(random.choice(self.agents))

        # Reflection and social influence
        for agent in self.agents:
            agent.reflect()
            for other in self.agents:
                if agent != other:
                    agent.social_influence(other)

        # Evaluate decision to touch the tree
        for agent in self.agents:
            if not agent.has_touched_tree and agent.evaluate_decision(temptation=1.5):
                agent.has_touched_tree = True
                return True, agent.name

        return False, None

    def run(self):
        while True:
            fallen, who = self.simulate_day()
            if fallen:
                return self.day, who
            self.day += 1

# ---------------- RUN MULTIPLE SIMULATIONS ----------------
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

# Run simulations
results_with_snake = run_multiple_simulations(500, snake_present=True)
results_without_snake = run_multiple_simulations(500, snake_present=False)

# Combine and save
all_results = results_with_snake + results_without_snake
with open("garden_simulation_results.csv", "w", newline="") as csvfile:
    fieldnames = ["run", "day_of_fall", "who_touched_first", "snake_present"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_results)

print("Simulations completed. Results saved to garden_simulation_results.csv")
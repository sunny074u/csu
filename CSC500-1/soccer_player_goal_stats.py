# List of 10 popular soccer players
players = [
    "Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappe", "Erling Haaland", "Neymar Jr",
    "Mohamed Salah", "Harry Kane", "Vinicius Jr", "Kevin De Bruyne", "Robert Lewandowski"
]

# Array storing goals scored this season
goals = [32, 28, 30, 36, 15, 22, 25, 18, 10, 24]

# Display player goal stats
print("⚽ Soccer Player Goal Stats:")
for i in range(len(players)):
    print(f"{players[i]} scored {goals[i]} goals.")

# Identify top scorer
max_goals = max(goals)
top_scorer_index = goals.index(max_goals)
print(f"\n🏆 Top Scorer: {players[top_scorer_index]} with {max_goals} goals")

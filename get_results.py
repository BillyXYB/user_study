import csv
from collections import defaultdict

def get_win_counts(filename="results.csv"):
    # Initialize counts dicts
    wins = defaultdict(lambda: {"quality": 0, "view_consistency": 0, "diversity": 0})
    total_votes = defaultdict(lambda: {"quality": 0, "view_consistency": 0, "diversity": 0})

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # row format:
            # user_id, prompt, method_a, method_b,
            # quality_choice, quality_winner,
            # relevance_choice, relevance_winner,
            # creativity_choice, creativity_winner
            if len(row) < 10:
                continue  # skip malformed rows

            method_a = row[2]
            method_b = row[3]

            quality_winner = row[5]
            relevance_winner = row[7]
            creativity_winner = row[9]

            # Every method in pair got one vote opportunity per metric
            for method in [method_a, method_b]:
                total_votes[method]["quality"] += 1
                total_votes[method]["view_consistency"] += 1
                total_votes[method]["diversity"] += 1

            # Count wins
            wins[quality_winner]["quality"] += 1
            wins[relevance_winner]["view_consistency"] += 1
            wins[creativity_winner]["diversity"] += 1

    return wins, total_votes

def print_summary(wins, total_votes):
    methods = sorted(set(list(wins.keys()) + list(total_votes.keys())))
    print(f"{'Method':<15} {'Quality':>8} {'Win%':>6} {'ViewCons':>10} {'Win%':>6} {'Diversity':>10} {'Win%':>6}")
    print("-" * 70)
    for m in methods:
        q_wins = wins[m]["quality"]
        q_total = total_votes[m]["quality"]
        q_pct = (q_wins / q_total * 100) if q_total > 0 else 0

        v_wins = wins[m]["view_consistency"]
        v_total = total_votes[m]["view_consistency"]
        v_pct = (v_wins / v_total * 100) if v_total > 0 else 0

        d_wins = wins[m]["diversity"]
        d_total = total_votes[m]["diversity"]
        d_pct = (d_wins / d_total * 100) if d_total > 0 else 0

        print(f"{m:<15} "
              f"{q_wins:>8} {q_pct:6.1f}% "
              f"{v_wins:>10} {v_pct:6.1f}% "
              f"{d_wins:>10} {d_pct:6.1f}%")

if __name__ == "__main__":
    wins, total_votes = get_win_counts()
    print_summary(wins, total_votes)
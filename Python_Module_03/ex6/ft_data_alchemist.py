#!/usr/bin/python3.10

import random


if __name__ == "__main__":
    print("=== Game Data Alchemist ===\n")
    players = [
        "Alice", "bob", "Charlie", "dylan",
        "Emma", "Gregory", "john", "kevin", "Liam"
    ]
    print(f"Initial list of players: {players}")
    capitalized = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {capitalized}")
    only_caps = [name for name in players if name[0].isupper()]
    print(f"New list of capitalized names only: {only_caps}")
    scores = {name: random.randint(0, 1000) for name in capitalized}
    print(f"\nScore dict: {scores}")
    avg = sum(scores.values()) / len(scores)
    print(f"Score average is {round(avg, 2)}")
    high_scores = {n: s for n, s in scores.items() if s > avg}
    print(f"High scores: {high_scores}")

# def list_comprehension(list_players):
#     print("=== List Comprehension Examples ===")
#     highscorers = [name for name, score, _ in list_players if score > 2000]
#     print(f"High scorers (>2000): {highscorers}")
#     double_scores = [score * 2 for _, score, _ in list_players]
#     print(f"Scores doubled: {double_scores}")
#     active_players = [name for name, _, active in list_players if active]
#     print(f"Active players: {active_players}\n")


# def dict_comprehension(dict_players, achievements):
#     print("=== Dict Comprehension Examples ===")
#     print(f"Player scores: {dict_players}")
#     score_counts = {
#         category: sum(
#             1 for score in dict_players.values()
#             if (score < 2500 and category == "high")
#             or (score <= 2200 and category == "medium")
#             or (score < 1900 and category == "low")
#         )
#         for category in ("high", "medium", "low")
#     }
#     print(f"Score categories: {score_counts}")
#     achievement_counts = {
#         player: len(achievements[player])
#         for player in dict_players
#     }
#     print(f"Achievement counts: {achievement_counts}\n")


# def set_comprehension(set_players, achievements_set_players, player_regions):
#     print("=== Set Comprehension Examples ===")
#     unique_players = {player for player in set_players}
#     print(f"Unique players: {unique_players}")
#     unique_achievements = {
#         achievement
#         for ach_list in achievements_set_players.values()
#         for achievement in ach_list
#     }
#     print(f"Unique Achievements: {unique_achievements}")
#     active_regions = {region for region in player_regions.values()}
#     print(f"Active regions: {active_regions}\n")


# def combined_anal(set_players, achievements, dict_players, list_players):
#     print("=== Combined Analysis ===")
#     total_players = len(set_players)
#     unique_achievements = {
#         ach
#         for ach_list in achievements.values()
#         for ach in ach_list
#     }
#     total_unique_achievements = len(unique_achievements)
#     average_score = sum(score
#                         for _, score, _ in list_players) / len(list_players)
#     top_player = max(dict_players, key=dict_players.get)
#     top_score = dict_players[top_player]
#     top_achievements = len(achievements.get(top_player, []))
#     print(f"Total players: {total_players}")
#     print(f"Total unique achievements: {total_unique_achievements}")
#     print(f"Average score: {average_score}")
#     print(
#         f"Top performer: {top_player} "
#         f"({top_score} points, {top_achievements} achievements)"
#     )


# if __name__ == "__main__":
#     print("=== Game Analytics Dashboard ===\n")
#     list_players: list = [
#         ("alice", 2300, True),
#         ("bob", 1800, True),
#         ("charlie", 2150, True),
#         ("diana", 2050, False)
#     ]
#     list_comprehension(list_players)
#     dict_players: dict = {
#         "alice": 2300,
#         "bob": 1800,
#         "charlie": 2150
#     }
#     achievements: dict[set] = {
#         "alice": ["first_kill", "boss_slayer", "level_10", "speed_runner",
#                   "collector"],
#         "bob": ["first_kill", "level_10", "collector"],
#         "charlie": ["first_kill", "boss_slayer", "level_10", "strategist",
#                     "sharpshooter", "collector", "veteran"],
#         "diana": ["idk", "bruh", "pmo", "ong"]
#     }
#     achievements_set_players: dict[set] = {
#         "alice": ["first kill"],
#         "bob": ["level_10"],
#         "charlie": ["boss_slayer"],
#     }
#     dict_comprehension(dict_players, achievements)
#     set_players: set = {
#         "alice",
#         "bob",
#         "charlie",
#         "diana"
#     }
#     player_regions: dict = {
#         "alice": "north",
#         "bob": "east",
#         "charlie": "central",
#         "diana": "east"
#     }
#     set_comprehension(set_players, achievements_set_players, player_regions)
#     combined_anal(set_players, achievements, dict_players, list_players)

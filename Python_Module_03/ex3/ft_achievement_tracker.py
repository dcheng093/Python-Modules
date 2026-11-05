#!/usr/bin/env python3

import random

ACHIEVEMENTS = [
    "First Steps", "Speed Runner", "Survivor", "Strategist",
    "Master Explorer", "Treasure Hunter", "Collector Supreme",
    "Untouchable", "Boss Slayer", "Sharp Mind",
    "Crafting Genius", "World Savior", "Unstoppable",
    "Hidden Path Finder"
]


def gen_player_achievements() -> set[str]:
    count = random.randint(6, 9)
    return set(random.sample(ACHIEVEMENTS, count))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()
    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}")

    print(f"\nAll distinct achievements: {alice.union(bob, charlie, dylan)}")
    print("\nCommon achievements: "
          f"{alice.intersection(bob, charlie, dylan)}\n")

    print(f"Only Alice has: {alice.difference(bob, charlie, dylan)}")
    print(f"Only Bob has: {bob.difference(alice, charlie, dylan)}")
    print(f"Only Charlie has: {charlie.difference(alice, bob, dylan)}")
    print(f"Only Dylan has: {dylan.difference(alice, bob, charlie)}\n")

    everything = set(ACHIEVEMENTS)
    print(f"Alice is missing: {everything.difference(alice)}")
    print(f"Bob is missing: {everything.difference(bob)}")
    print(f"Charlie is missing: {everything.difference(charlie)}")
    print(f"Dylan is missing: {everything.difference(dylan)}")

# def achievement_tracker(players):
#     print("=== Achievement Tracker System ===\n")
#     for player in players:
#         print(f"Player {player} achievements: {players[player]}")
#     print("=== Achievement Analysis ===\n")
#     unique_achievements = set()
#     for player in players:
#         unique_achievements = unique_achievements.union(players[player])
#     print(f"All unique achievements: {unique_achievements}")
#     print(f"Total unique achievements: {len(unique_achievements)}\n")
#     common = None
#     for player in players:
#         if common is None:
#             common = players[player]
#         else:
#             common = common.intersection(players[player])
#     print(f"Common to all players: {common}")
#     rare = set()
#     for achievements in unique_achievements:
#         count = 0
#         for player in players:
#             if achievements in players[player]:
#                 count += 1
#         if count == 1:
#             rare = rare.union({achievements})
#     print(f"Rare achievements (1 player): {rare}\n")
#     alice = players["alice"]
#     bob = players["bob"]
#     print(f"Alice vs Bob common: {alice.intersection(bob)}")
#     print(f"Alice unique: {alice.difference(bob)}")
#     print(f"Bob unique: {bob.difference(alice)}")


# if __name__ == "__main__":
#     players = {"alice": {'speed_demon', 'level_10', 'treasure_hunter',
#                          'first_kill'},

#                "bob": {'first_kill', 'level_10', 'boss_slayer', 'collector'},

#                "charlie": {'level_10', 'treasure_hunter', 'boss_slayer',
#                            'speed_demon',
#                            'perfectionist'}}
#     achievement_tracker(players)

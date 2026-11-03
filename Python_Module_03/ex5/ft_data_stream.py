#!/usr/bin/python3.10

# from time import perf_counter as timer
import random
import typing


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    names = ["alice",
             "bob",
             "charlie",
             "james",
             "david",
             "mary",
             "daniel",
             "john"]
    actions = [
        "killed monster",
        "found treasure",
        "leveled up",
        "died",
        "used the toilet",
        "is hosting a party",
        "crashed",
        "has been banned",
        "tamed a chicken",
        "just received a Golden Frying Pan!",
        "crafted a M109 howitzer",
        "uninstalled",
        "started a podcast",
        "hates daniel"
    ]
    while True:
        player = random.choice(names)
        action = random.choice(actions)
        yield (player, action)


def consume_event(events: list[tuple[str, str]]
                  ) -> typing.Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        idx = random.randrange(len(events))
        picked = events.pop(idx)
        yield picked


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===")
    stream = gen_event()
    for i in range(1000):
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")
    saved_events: list[tuple[str, str]] = []
    for _ in range(10):
        saved_events.append(next(stream))
    print(f"Built list of 10 events: {saved_events}")
    for event in consume_event(saved_events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {saved_events}")

# def gen_fib(n):
#     a, b = 0, 1
#     for _ in range(n):
#         yield a
#         a, b = b, a + b


# def gen_prime(n):
#     count = 0
#     num = 2
#     while count < n:
#         prime = True
#         for i in range(2, int(num ** (1/2)) + 1):
#             if num % i == 0:
#                 prime = False
#                 break
#         if prime:
#             yield num
#             count += 1
#         num += 1


# def gen_game_events(n_ev, n_fib, n_prime):
#     print("=== Game Data Stream Processor ===\n")
#     print(f"Processing {n_ev} game events...\n")
#     names = [
#         "alice", "bob", "charlie", "james", "david",
#         "mary", "daniel", "john"
#     ]
#     low_level = [5, 8, 3, 2, 1]
#     high_level = [12, 42, 16, 24, 19]
#     events = [
#         "killed monster",
#         "found treasure",
#         "leveled up",
#         "died",
#         "used the toilet",
#         "is hosting a party",
#         "crashed",
#         "has been banned",
#         "tamed a chicken",
#         "just received a Golden Frying Pan!",
#         "crafted a M109 howitzer",
#         "uninstalled",
#         "started a podcast",
#         "hates daniel"
#     ]
#     high_count = 0
#     treasure_count = 0
#     levelup_count = 0
#     start = timer()
#     for i in range(1, n_ev + 1):
#         player = random.choice(names)
#         level = random.choice(low_level + high_level)
#         action = random.choice(events)
#         if level >= 10:
#             high_count += 1
#         if action == "found treasure":
#             treasure_count += 1
#         if action == "leveled up":
#             levelup_count += 1
#         yield f"Event {i}: Player {player} (level {level}) {action}"
#     end = timer()
#     print("")
#     print("=== Stream Analytics ===")
#     print(f"Total events processed: {n_ev}")
#     print(f"High-level players (10+): {high_count}")
#     print(f"Treasure events: {treasure_count}")
#     print(f"Level-up events: {levelup_count}\n")
#     print("Memory usage: Constant (streaming)")
#     print(f"Processing time: {end - start:.3f} seconds\n")
#     print("=== Generator Demonstration ===")
#     print(f"Fibonacci sequence (first {n_fib}):", end=" ")
#     fib_count = 0
#     for num in gen_fib(n_fib):
#         fib_count += 1
#         if fib_count == n_fib:
#             print(num)
#         else:
#             print(num, end=", ")
#     print(f"Prime numbers (first {n_prime}):", end=" ")
#     prime_count = 0
#     for num in gen_prime(n_prime):
#         prime_count += 1
#         if prime_count == n_prime:
#             print(num)
#         else:
#             print(num, end=", ")


# if __name__ == "__main__":
#     for event in gen_game_events(1000, 10, 5):
#         print(event)

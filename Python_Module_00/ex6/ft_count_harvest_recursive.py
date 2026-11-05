# def ft_count_harvest_recursive(days: int = 1, n: int = False):
#     n = n or int(input("Days until harvest: "))
#     print(f"Day {days}" if days <= n else
#           "Harvest time!") or (days <= n and
#                                ft_count_harvest_recursive(days + 1, n))

def ft_count_harvest_recursive() -> None:
    def count(day: int, last: int) -> None:
        if day > last:
            print("Harvest time!")
            return
        print(f"Day {day}")
        count(day + 1, last)

    count(1, int(input("Days until harvest: ")))

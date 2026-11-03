from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    name: str = "Data Processor"

    def __init__(self) -> None:
        self._data: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data left on processor")
        rank = self._rank
        self._rank += 1
        return rank, self._data.pop(0)

    def remaining(self) -> int:
        return len(self._data)

    def total(self) -> int:
        """Items ever ingested: the ones already output + the ones left."""
        return self._rank + len(self._data)


class NumericProcessor(DataProcessor):
    name = "Numeric Processor"

    @staticmethod
    def _is_number(item: Any) -> bool:
        return isinstance(item, (int, float)) and not isinstance(item, bool)

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self._is_number(item) for item in data)
        return self._is_number(data)

    def ingest(  # type: ignore[override]
        self, data: int | float | list[int | float]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        self._data.extend(str(item) for item in items)


class TextProcessor(DataProcessor):
    name = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(  # type: ignore[override]
        self, data: str | list[str]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        items = data if isinstance(data, list) else [data]
        self._data.extend(items)


class LogProcessor(DataProcessor):
    name = "Log Processor"

    @staticmethod
    def _is_log(item: Any) -> bool:
        return isinstance(item, dict) and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in item.items()
        )

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self._is_log(item) for item in data)
        return self._is_log(data)

    def ingest(  # type: ignore[override]
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for entry in items:
            level = entry.get("log_level", "UNKNOWN")
            message = entry.get("log_message", "")
            self._data.append(f"{level}: {message}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            proc = next(
                (p for p in self._processors if p.validate(element)), None
            )
            if proc is None:
                print("DataStream error - "
                      f"Can't process element in stream: {element}")
                continue
            try:
                proc.ingest(element)
            except (ValueError, TypeError) as e:
                print(f"DataStream error - {proc.name} rejected "
                      f"{element}: {e}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(f"{proc.name}: total {proc.total()} items processed, "
                  f"remaining {proc.remaining()} on processor")


def consume(proc: DataProcessor, count: int) -> None:
    for _ in range(count):
        proc.output()


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    num = NumericProcessor()
    stream.register_processor(num)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    consume(num, 3)
    consume(text, 2)
    consume(log, 1)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()

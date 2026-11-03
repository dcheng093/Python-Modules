from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
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


class NumericProcessor(DataProcessor):
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


def extract(proc: DataProcessor, label: str, count: int) -> None:
    plural = "value" if count == 1 else "values"
    print(f" Extracting {count} {plural}...")
    for _ in range(count):
        rank, value = proc.output()
        print(f" {label} {rank}: {value}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    num = NumericProcessor()
    print(f" Trying to validate input '42': {num.validate(42)}")
    print(f" Trying to validate input 'Hello': {num.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")  # wrong type on purpose: mypy flags this line
    except ValueError as e:
        print(f" Got exception: {e}")
    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {numbers}")
    num.ingest(numbers)
    extract(num, "Numeric value", 3)

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f" Trying to validate input '42': {text.validate(42)}")
    words = ["Hello", "Nexus", "World"]
    print(f" Processing data: {words}")
    text.ingest(words)
    extract(text, "Text value", 1)

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f" Trying to validate input 'Hello': {log.validate('Hello')}")
    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f" Processing data: {logs}")
    log.ingest(logs)
    extract(log, "Log entry", 2)


if __name__ == "__main__":
    main()

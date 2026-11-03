from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    @staticmethod
    def _field(value: str) -> str:
        if any(c in value for c in ',"\n'):
            return '"' + value.replace('"', '""') + '"'
        return value

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(self._field(value) for _, value in data))


class JSONExportPlugin:
    @staticmethod
    def _string(value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        escaped = escaped.replace("\n", "\\n")
        return f'"{escaped}"'

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        pairs = [f'{self._string(f"item_{rank}")}: {self._string(value)}'
                 for rank, value in data]
        print("{" + ", ".join(pairs) + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            extracted: list[tuple[int, str]] = []
            for _ in range(min(nb, proc.remaining())):
                extracted.append(proc.output())
            if extracted:
                plugin.process_output(extracted)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors\n")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

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
    print(f"Send first batch of data on stream: {batch}\n")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    print()
    stream.print_processors_stats()

    batch = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {batch}\n")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()

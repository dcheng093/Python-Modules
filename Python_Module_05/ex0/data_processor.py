from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    name: str = "Data Processor"

    def __init__(self) -> None:
        self._data: list[str] = []
        self._index: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available")
        value = self._data.pop(0)
        idx = self._index
        self._index += 1
        return (idx, value)

    def remaining(self) -> int:
        return len(self._data)


class NumericProcessor(DataProcessor):
    name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for x in data:
                self._data.append(str(x))
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):
    name = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            self._data.extend(data)
        else:
            self._data.append(data)


class LogProcessor(DataProcessor):
    name = "Log Processor"

    def validate(self, data: Any) -> bool:
        def valid_dict(d: Any) -> bool:
            return (
                isinstance(d, dict)
                and all(isinstance(k, str) and
                        isinstance(v, str) for k, v in d.items())
            )
        if isinstance(data, dict):
            return valid_dict(data)
        if isinstance(data, list):
            return all(valid_dict(x) for x in data)
        return False

    def ingest(self,
               data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def format_log(d: dict[str, str]) -> str:
            return f"{d.get('log_level', '')}: {d.get('log_message', '')}"
        if isinstance(data, list):
            for d in data:
                self._data.append(format_log(d))
        else:
            self._data.append(format_log(data))


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    # tumeric
    print("\nTesting Numeric Processor...")
    num = NumericProcessor()
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")
    except Exception as e:
        print(f"Got exception: {e}")
    print("Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values...")
    for _ in range(3):
        idx, val = num.output()
        print(f"Numeric value {idx}: {val}")

    # text
    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(['Hello', 'Nexus', 'World'])
    print("Extracting 1 value...")
    idx, val = text.output()
    print(f"Text value {idx}: {val}")

    # leg
    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    logs = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {logs}")
    log.ingest(logs)
    print("Extracting 2 values...")
    for _ in range(2):
        idx, val = log.output()
        print(f"Log entry {idx}: {val}")

# class DataProcessor(ABC):
#     @abstractmethod
#     def validate(self, data: Any) -> bool:
#         pass

#     @abstractmethod
#     def process(self, data: Any) -> str:
#         pass

#     def format_output(self, result: str) -> str:
#         return result


# class NumericProcessor(DataProcessor):
#     def __init__(self):
#         pass

#     def validate(self, data: Any) -> bool:
#         return (
#             isinstance(data, list)
#             and all(isinstance(x, (int, float)) for x in data)
#         )

#     def process(self, data: Any) -> str:
#         if not self.validate(data):
#             raise ValueError("Invalid numeric data")
#         count = len(data)
#         total = sum(data)
#         avg = total / count if count else 0
#         return f"Processed {count} numeric values, sum={total}, avg={avg}"

#     def format_output(self, result: str) -> str:
#         return result


# class TextProcessor(DataProcessor):
#     def __init__(self):
#         pass

#     def validate(self, data: Any) -> bool:
#         return isinstance(data, str)

#     def process(self, data: Any) -> str:
#         if not self.validate(data):
#             raise ValueError("Invalid text data")
#         char_count = len(data)
#         word_count = len(data.split())
#         return f"Processed text: {char_count} characters, {word_count} words"

#     def format_output(self, result: str) -> str:
#         return result


# class LogProcessor(DataProcessor):
#     def __init__(self):
#         pass

#     def validate(self, data: Any) -> bool:
#         if not isinstance(data, str):
#             return False
#         return any(data.startswith(level) for level in ("ERROR:", "INFO:",
#                                                         "WARNING:"))

#     def process(self, data: Any) -> str:
#         if not self.validate(data):
#             raise ValueError("Invalid log entry")
#         level, message = data.split(":", 1)
#         message = message.strip()
#         return f"{level} level detected: {message}"

#     def format_output(self, result: str) -> str:
#         if result.startswith("ERROR"):
#             return f"[ALERT] {result}"
#         elif result.startswith("INFO"):
#             return f"[INFO] {result}"
#         else:
#             return f"[WARNING] {result}"


# if __name__ == "__main__":
#     print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
#     numeric_data = [1, 2, 3, 4, 5]
#     text_data = "Hello Nexus World"
#     log_data = "ERROR: Connection timeout"
#     numeric_processor = NumericProcessor()
#     text_processor = TextProcessor()
#     log_processor = LogProcessor()
#     print("Initializing Numeric Processor...")
#     print(f"Processing data: {numeric_data}")
#     print("Validation: Numeric data verified")
#     output = numeric_processor.format_output(
#         numeric_processor.process(numeric_data))
#     print(f"Output: {output}\n")
#     print("Initializing Text Processor...")
#     print(f'Processing data: "{text_data}"')
#     print("Validation: Text data verified")
#     output = text_processor.format_output(text_processor.process(text_data))
#     print(f"Output: {output}\n")
#     print("Initializing Log Processor...")
#     print(f'Processing data: "{log_data}"')
#     print("Validation: Log entry verified")
#     output = log_processor.format_output(log_processor.process(log_data))
#     print(f"Output: {output}\n")
#     print("=== Polymorphic Processing Demo ===")
#     print("Processing multiple data types through same interface...")
#     processors = [
#         NumericProcessor(),
#         TextProcessor(),
#         LogProcessor()
#     ]
#     data_samples = [
#         [1, 2, 3],
#         "Twelve Chars",
#         "INFO: System ready"
#     ]
#     for i, (processor, data) in enumerate(zip(processors, data_samples),
#                                           start=1):
#         result = processor.process(data)
#         output = processor.format_output(result)
#         print(f"Result {i}: {output}")

#     print("\nFoundation systems online. Nexus ready for advanced streams.")

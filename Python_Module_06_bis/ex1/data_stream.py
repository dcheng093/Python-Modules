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

    def ingest(self, data: int | float | list[int | float]) -> None:
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

    def ingest(self, data: str | list[str]) -> None:
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

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
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


# class DataStream(ABC):
#     def __init__(self, stream_id: str, stream_type: str = "Generic") -> None:
#         self.stream_id = stream_id
#         self.stream_type = stream_type
#         self.processed_batches = 0
#         print(f"Initializing "
#               f"{self.__class__.__name__.replace('Stream', ' Stream')}...")
#         print(f"Stream ID: {self.stream_id}, Type: {self.stream_type} Data")

#     @abstractmethod
#     def process_batch(self, data_batch: List[Any]) -> str:
#         pass

#     @abstractmethod
#     def unified_summary(self, data_batch: List[Any]) -> str:
#         pass

#     def filter_data(self, data_batch: List[Any],
#                     criteria: Optional[str] = None) -> List[Any]:
#         if not criteria:
#             return data_batch
#         return [item for item in data_batch if
#                 criteria.lower() in str(item).lower()]

#     def get_stats(self) -> Dict[str, Union[str, int, float]]:
#         return {
#             "stream_id": self.stream_id,
#             "stream_type": self.stream_type,
#             "processed_batches": self.processed_batches
#         }


# class SensorStream(DataStream):
#     def process_batch(self, data_batch: List[Any]) -> str:
#         sensors = {}
#         for item in data_batch:
#             if isinstance(item, str) and ":" in item:
#                 key, value = item.split(":", 1)
#                 try:
#                     sensors[key] = float(value)
#                 except ValueError:
#                     pass
#         sensor_items = [
#             f"{k}:{int(v) if v.is_integer() else v}"
#             for k, v in sensors.items()
#         ]
#         print(f"Processing sensor batch: [{', '.join(sensor_items)}]")
#         if not sensors:
#             return "Sensor analysis: no valid readings"
#         avg_temp = sensors.get("temp", 0.0)
#         return (
#             f"Sensor analysis: {len(sensors)} readings processed, "
#             f"avg temp: {avg_temp:.1f}°C"
#         )

#     def unified_summary(self, data_batch: List[Any]) -> str:
#         sensors = [item for item in data_batch if isinstance(item, str) and
#                    ":" in item]
#         return f"Sensor data: {len(sensors)} readings processed"

#     def filter_data(
#         self,
#         data_batch: List[Any],
#         criteria: Optional[str] = None
#     ) -> List[Any]:
#         if not criteria:
#             return data_batch
#         return [
#             item for item in data_batch
#             if isinstance(item, str)
#             and ":" in item
#             and (
#                 item.startswith("temp_high")
#                 or item.startswith("humidity_high")
#             )
#         ]


# class TransactionStream(DataStream):
#     def process_batch(self, data_batch: List[Any]) -> str:
#         transactions = []
#         net_flow = 0
#         for item in data_batch:
#             if isinstance(item, str) and ":" in item:
#                 action, value = item.split(":", 1)
#                 try:
#                     amount = int(value)
#                 except ValueError:
#                     continue
#                 transactions.append(f"{action}:{amount}")
#                 if action == "buy":
#                     net_flow += amount
#                 elif action == "sell":
#                     net_flow -= amount
#         print(f"Processing transaction batch: [{', '.join(transactions)}]")
#         sign = "+" if net_flow >= 0 else ""
#         return (
#             f"Transaction analysis: {len(transactions)} operations, "
#             f"net flow: {sign}{net_flow} units"
#         )

#     def unified_summary(self, data_batch: List[Any]) -> str:
#         transactions = [item for item in data_batch if isinstance(item, str)
#                         and ":" in item]
#         return f"Transaction data: {len(transactions)} operations processed"

#     def filter_data(
#         self,
#         data_batch: List[Any],
#         criteria: Optional[str] = None
#     ) -> List[Any]:
#         if not criteria:
#             return data_batch
#         return [
#             item for item in data_batch
#             if isinstance(item, str)
#             and (
#                 "large" in item.lower()
#                 or "high" in item.lower()
#             )
#         ]


# class EventStream(DataStream):
#     def process_batch(self, data_batch: List[Any]) -> str:
#         events = [x for x in data_batch if isinstance(x, str)]
#         errors = [e for e in events if "error" in e.lower()]
#         print(f"Processing event batch: [{', '.join(events)}]")
#         return (
#             f"Event analysis: {len(events)} events, "
#             f"{len(errors)} error detected"
#         )

#     def unified_summary(self, data_batch: List[Any]) -> str:
#         events = [x for x in data_batch if isinstance(x, str)]
#         return f"Event data: {len(events)} events processed"

#     def filter_data(
#         self,
#         data_batch: List[Any],
#         criteria: Optional[str] = None
#     ) -> List[Any]:
#         if not criteria:
#             return data_batch
#         return [
#             item for item in data_batch
#             if isinstance(item, str)
#             and (
#                 "critical" in item.lower()
#                 or "error" in item.lower()
#             )
#         ]


# class StreamProcessor:
#     def __init__(self) -> None:
#         self.streams: List[DataStream] = []

#     def add_stream(self, stream: DataStream) -> None:
#         self.streams.append(stream)

#     def run_unified(self, batch: List[Any],
#                     filter_criteria: Optional[str] = None) -> None:
#         print("\n=== Polymorphic Stream Processing ===")
#         print("Processing mixed stream types through unified interface...\n")
#         print("Batch 1 Results:")
#         for stream in self.streams:
#             try:
#                 filtered_batch = stream.filter_data(batch, filter_criteria)
#                 result = stream.unified_summary(filtered_batch)
#                 print(f"- {result}")
#             except Exception as e:
#                 print(f"Error processing stream {stream.stream_id}: {e}")
#         if filter_criteria:
#             print(f"\nStream filtering active: {filter_criteria}-priority "
#                   "data only")
#             print("Filtered results: 2 critical sensor alerts, 1 large"
#                   " transaction")


# if __name__ == "__main__":
#     print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
#     processor = StreamProcessor()
#     ssensor = SensorStream("SENSOR_001", "Environmental")
#     print(ssensor.process_batch(["temp:22.5", "humidity:65",
#           "pressure:1013"]) + "\n")
#     tsensor = TransactionStream("TRANS_001", "Financial")
#     print(tsensor.process_batch(["buy:100", "sell:150", "buy:75"]) + "\n")
#     esensor = EventStream("EVENT_001", "System")
#     print(esensor.process_batch(["login", "error", "logout"]))
#     processor.add_stream(ssensor)
#     processor.add_stream(tsensor)
#     processor.add_stream(esensor)
#     processor.run_unified([
#         "temp_high:22.5",
#         "humidity_high:65",
#         "pressure:1013",
#         "buy_large:1000",
#         "sell_large:150",
#         "login_critical",
#         "error_critical",
#         "logout_critical"
#     ], filter_criteria="High")
#     print("\nAll streams processed successfully. Nexus throughput optimal.")

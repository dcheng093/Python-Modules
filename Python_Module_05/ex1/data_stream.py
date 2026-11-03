#!/usr/bin/python3.10

from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
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


class NumericProcessor(DataProcessor):
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


class DataStream:
    def __init__(self) -> None:
        self.processors: List[DataProcessor] = []
        self.total_processed: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)
        self.total_processed[proc] = 0

    def process_stream(self, stream: List[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    if isinstance(element, list):
                        self.total_processed[proc] += len(element)
                    else:
                        self.total_processed[proc] += 1
                    handled = True
                    break
            if not handled:
                print("DataStream error - Can't process element in stream: "
                      f"{element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            total = self.total_processed.get(proc, 0)
            remaining = len(proc._data)
            print(f"{name}: total {total} items processed, "
                  f"remaining {remaining} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    ds = DataStream()
    print("\nInitialize Data Stream...")
    ds.print_processors_stats()
    print("\nRegistering Numeric Processor\n")
    num = NumericProcessor()
    ds.register_processor(num)

    stream = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {stream}")
    ds.process_stream(stream)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    ds.register_processor(text)
    ds.register_processor(log)
    print("Send the same batch again")
    ds.process_stream(stream)
    ds.print_processors_stats()

    print("\nConsume some elements from the data "
          "processors: Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        text.output()
    for _ in range(1):
        log.output()

    ds.print_processors_stats()

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

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


# class ProcessingStage(Protocol):
#     def process(self, data: Any) -> Any:
#         pass


# class ProcessingPipeline(ABC):
#     def __init__(self) -> None:
#         self.stages: List[ProcessingStage] = []

#     def add_stage(self, stage: ProcessingStage) -> None:
#         self.stages.append(stage)

#     def process(self, data: Any) -> Any:
#         for idx, stage in enumerate(self.stages, start=1):
#             try:
#                 data = stage.process(data)
#             except Exception as e:
#                 print(f"Error detected in Stage {idx}: {e}")
#         return data


# class NexusManager:
#     def __init__(self) -> None:
#         print("Creating Data Processing Pipeline...")
#         self.pipelines = []

#     def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
#         self.pipelines.append(pipeline)

#     def run_all(self, data: str) -> str:
#         for idx, pipeline in enumerate(self.pipelines, start=1):
#             try:
#                 data = pipeline.process(data)
#             except Exception as e:
#                 print(f"Error detected in Stage {idx}: {e}")
#         return data


# class JSONAdapter(ProcessingPipeline):
#     def __init__(self, pipeline_id: str) -> None:
#         super().__init__()
#         self.pipeline_id = pipeline_id


# class CSVAdapter(ProcessingPipeline):
#     def __init__(self, pipeline_id: str) -> None:
#         super().__init__()
#         self.pipeline_id = pipeline_id


# class StreamAdapter(ProcessingPipeline):
#     def __init__(self, pipeline_id: str) -> None:
#         super().__init__()
#         self.pipeline_id = pipeline_id


# class InputStage:
#     def process(self, data: Any) -> Any:
#         return data


# class TransformStage:
#     def process(self, data: Any) -> Any:
#         return data


# class OutputStage:
#     def process(self, data: Any) -> Any:
#         return data


# if __name__ == "__main__":
#     print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")
#     print("Initializing Nexus Manager...")
#     print("Pipeline capacity: 1000 streams/second\n")
#     manager = NexusManager()
#     stages_description = [
#         "Input validation and parsing",
#         "Data transformation and enrichment",
#         "Output formatting and delivery",
#     ]
#     for i, desc in enumerate(stages_description, start=1):
#         print(f"Stage {i}: {desc}")
#     print()
#     input_stage = InputStage()
#     transform_stage = TransformStage()
#     output_stage = OutputStage()
#     json_pipeline = JSONAdapter("JSON")
#     csv_pipeline = CSVAdapter("CSV")
#     stream_pipeline = StreamAdapter("STREAM")
#     for stage in (input_stage, transform_stage, output_stage):
#         json_pipeline.add_stage(stage)
#     csv_pipeline.stages = json_pipeline.stages
#     stream_pipeline.stages = json_pipeline.stages
#     manager.add_pipeline(json_pipeline)
#     manager.add_pipeline(csv_pipeline)
#     manager.add_pipeline(stream_pipeline)
#     print("=== Multi-Format Data Processing ===\n")
#     process_cases = [
#         (
#             "JSON",
#             json_pipeline,
#             '{"sensor": "temp", "value": 23.5, "unit": "C"}',
#             "Transform: Enriched with metadata and validation",
#             "Output: Processed temperature reading: 23.5°C (Normal range)",
#         ),
#         (
#             "CSV",
#             csv_pipeline,
#             '"user,action,timestamp"',
#             "Transform: Parsed and structured data",
#             "Output: User activity logged: 1 actions processed",
#         ),
#         (
#             "Stream",
#             stream_pipeline,
#             "Real-time sensor stream",
#             "Transform: Aggregated and filtered",
#             "Output: Stream summary: 5 readings, avg: 22.1°C",
#         ),
#     ]
#   for name, pipeline, input_data, transform_msg, output_msg in process_cases:
#         if name == "JSON":
#             print(f"Processing {name} data through pipeline...")
#         else:
#             print(f"Processing {name} data through same pipeline...")
#         pipeline.process(input_data)
#         print(f"Input: {input_data}")
#         print(transform_msg)
#         print(output_msg)
#         print()
#     print("=== Pipeline Chaining Demo ===")
#     print("Pipeline A -> Pipeline B -> Pipeline C")
#     print("Data flow: Raw -> Processed -> Analyzed -> Stored\n")
#     data = "Raw data"
#     for pipeline in (json_pipeline, csv_pipeline, stream_pipeline):
#         data = pipeline.process(data)
#     print("Chain result: 100 records processed through 3-stage pipeline")
#     print("Performance: 95% efficiency, 0.2s total processing time\n")
#     print("=== Error Recovery Test ===")
#     print("Simulating pipeline failure...")
#     print("Error detected in Stage 2: Invalid data format")
#     json_pipeline.process("BROKEN DATA")
#     print("Recovery initiated: Switching to backup processor")
#     print("Recovery successful: Pipeline restored, processing resumed\n")
#     print("Nexus Integration complete. All systems operational.")

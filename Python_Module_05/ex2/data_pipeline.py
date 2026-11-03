#!/usr/bin/python3.10


from typing import Any, List, Tuple, Protocol
from abc import ABC, abstractmethod


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

    def ingest(self, data: Any) -> None:
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

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            self._data.extend(data)
        else:
            self._data.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def valid_dict(d):
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

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def format_log(d):
            return f"{d.get('log_level', '')}: {d.get('log_message', '')}"
        if isinstance(data, list):
            for d in data:
                self._data.append(format_log(d))
        else:
            self._data.append(format_log(data))


class ExportPlugin(Protocol):
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        values = [value for _, value in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        print("JSON Output:")
        items = [f'"item_{idx}": "{value}"' for idx, value in data]
        print("{" + ", ".join(items) + "}")


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
                print("DataStream error - "
                      f"Can't process element in stream: {element}")

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")

        if not self.processors:
            print("No processor found, no data")
            return

        for proc in self.processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            total = self.total_processed.get(proc, 0)
            remaining = len(proc._data)
            print(f"{name}: total {total} items processed, "
                  f"remaining {remaining} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            extracted: List[Tuple[int, str]] = []

            for _ in range(nb):
                try:
                    extracted.append(proc.output())
                except Exception:
                    break

            if extracted:
                plugin.process_output(extracted)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")

    ds = DataStream()

    print("\nInitialize Data Stream...")
    ds.print_processors_stats()

    print("\nRegistering Processors\n")
    num = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    ds.register_processor(num)
    ds.register_processor(text)
    ds.register_processor(log)

    stream1 = [
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

    print(f"Send first batch of data on stream: {stream1}")
    ds.process_stream(stream1)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    ds.output_pipeline(3, csv_plugin)
    ds.print_processors_stats()

    stream2 = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {'log_level': 'ERROR',
             'log_message': '500 server crash'},
            {'log_level': 'NOTICE',
             'log_message': 'Certificate expires in 10 days'}
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]

    print(f"\nSend another batch of data: {stream2}")
    ds.process_stream(stream2)
    ds.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    ds.output_pipeline(5, json_plugin)

    ds.print_processors_stats()


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

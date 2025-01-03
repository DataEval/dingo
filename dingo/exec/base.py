from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict, List, Protocol, Union, Type
import inspect
from dingo.io import MetaData, SummaryModel


class ExecProto(Protocol):
    def load_data(self, path: str, data_type: str) -> List[MetaData]:
        ...

    def execute(self) -> List[SummaryModel]:
        ...

    def evaluate(self) -> SummaryModel:
        ...

    def summarize(self, inputs: MetaData) -> SummaryModel:
        ...


class Executor(ABC):
    exec_map: Dict[str, Type[ExecProto]] = {}

    @abstractmethod
    def load_data(self) -> List[MetaData]:
        raise NotImplementedError()

    @abstractmethod
    def execute(self, *args, **kwargs) -> List[SummaryModel]:
        raise NotImplementedError()

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Union[SummaryModel, List[SummaryModel], Any]:
        raise NotImplementedError()

    @abstractmethod
    def summarize(self) -> SummaryModel:
        raise NotImplementedError()

    @classmethod
    def register(cls, exec_name: str):

        def decorator(root_exec):
            cls.exec_map[exec_name] = root_exec
            if inspect.isclass(root_exec):
                return root_exec
            elif inspect.isfunction(root_exec):
                @wraps(root_exec)
                def wrapped_function(*args, **kwargs):
                    return root_exec(*args, **kwargs)
                return wrapped_function
            else:
                raise ValueError("root_exec must be a class or a function")

        return decorator



import json
from typing import Any, Dict, Generator, Optional, Union

from dingo.data.dataset.base import Dataset
from dingo.data.datasource import DataSource
from dingo.data.datasource.local import LocalDataSource
from dingo.io import Data


@Dataset.register()
class LocalDataset(Dataset):
    """
    Represents a HuggingFace dataset for use with Dingo Tracking.
    """

    @property
    def profile(self) -> Optional[Any]:
        return None

    def __init__(
        self,
        source: LocalDataSource,
        name: Optional[str] = None,
        digest: Optional[str] = None,
    ):
        """
        Args:
            source: The source of the local file data source
            name: The name of the dataset. E.g. "wiki_train". If unspecified, a name is
                automatically generated.
            digest: The digest (hash, fingerprint) of the dataset. If unspecified, a digest
                is automatically computed.
        """
        self._ds = source.load()
        super().__init__(source=source, name=name, digest=digest)

    @staticmethod
    def get_dataset_type() -> str:
        return "local"

    def _compute_digest(self) -> str:
        """
        Computes a digest for the dataset. Called if the user doesn't supply
        a digest when constructing the dataset.
        """
        return str(hash(json.dumps(self.source.to_dict())))[:8]

    def to_dict(self) -> Dict[str, str]:
        """Create config dictionary for the dataset.
        Returns a string dictionary containing the following fields: name, digest, source, source
        type, schema, and profile.
        """
        config = super().to_dict()
        config.update(
            {
                "profile": json.dumps(self.profile),
            }
        )
        return config

    def get_data(self) -> Generator[Data, None, None]:
        """
        Returns the input model for the dataset.
        Convert data here.
        """
        for data_raw in self._ds:
            data: Union[Generator[Data], Data] = self.converter(data_raw)
            if isinstance(data, Generator):
                for d in data:
                    yield d
            else:
                yield data

    @property
    def ds(self):
        """Datasets' generator instance.
        Returns:
            Datasets' generator instance.
        """
        return self._ds

    @property
    def source(self) -> DataSource:
        """Hugging Face dataset source information.
        Returns:
            A :py:class:`mlflow.data.huggingface_dataset_source.HuggingFaceSource`
        """
        return self._source

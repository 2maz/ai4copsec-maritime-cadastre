from argparse import ArgumentParser
from collections import OrderedDict
from pathlib import Path


import damast
import keras
from damast.core.dataframe import AnnotatedDataFrame
from damast.ml.models.base import BaseModel
from damast.core.dataprocessing import PipelineElement, DataProcessingPipeline
from damast.core.data_description import MinMax
from damast.core.transformations import CycleTransformer
from damast.core.units import units
from damast.utils.io import Archive

from damast.ml.experiments import (
    Experiment,
    ForecastTask,
    LearningTask,
    ModelInstanceDescription,
    TrainingParameters,
    )

class Baseline(BaseModel):
    input_specs = OrderedDict({
        "LAT_x": {"length": 1},
        "LAT_y": {"length": 1},
        "LON_x": {"length": 1},
        "LON_y": {"length": 1}
    })

    output_specs = OrderedDict({
        "LAT_x": {"length": 1},
        "LAT_y": {"length": 1},
        "LON_x": {"length": 1},
        "LON_y": {"length": 1}
    })

    def __init__(self,
                 features: list[str],
                 timeline_length: int,
                 output_dir: Path,
                 name: str = "Baseline",
                 targets: list[str] | None = None):
        self.timeline_length = timeline_length

        super().__init__(name=name,
                         output_dir=output_dir,
                         features=features,
                         targets=targets)

    def _init_model(self):
        features_width = len(self.features)
        targets_width = len(self.targets)

        input_layer = keras.Input(shape=(self.timeline_length, features_width))
        x = keras.layers.Flatten()(input_layer)
        x = keras.layers.Dense(targets_width)(x)

        self.model = keras.models.Model(inputs=input_layer, outputs=x)

class LatLonTransformer(PipelineElement):
    @damast.core.describe("Lat/Lon cyclic transformation")
    @damast.core.input({
        "lat": {'unit': 'deg'},
        "lon": {'unit': 'deg'}
    })
    @damast.core.output({
        "{{lat}}_x": {"value_range": MinMax(-1.0, 1.0)},
        "{{lat}}_y": {"value_range": MinMax(-1.0, 1.0)},
        "{{lon}}_x": {"value_range": MinMax(-1.0, 1.0)},
        "{{lon}}_y": {"value_range": MinMax(-1.0, 1.0)}
    })
    def transform(self, df: AnnotatedDataFrame) -> AnnotatedDataFrame:
        lat_cyclic_transformer = CycleTransformer(features=[self.get_name("lat")], n=180.0)
        lon_cyclic_transformer = CycleTransformer(features=[self.get_name("lon")], n=360.0)

        _df = lat_cyclic_transformer.fit_transform(df=df)
        _df = lon_cyclic_transformer.fit_transform(df=_df)
        return _df

def run_experiment(input_files):
    tmp_path = Path() / "experiment-output"
    pipeline = DataProcessingPipeline(name="preparation", base_dir=tmp_path) \
        .add("Latitude Longitude transform", LatLonTransformer(),
                name_mappings = {
                    'lat': 'LAT',
                    'lon': 'LON',
                }
        )

    models = [
        ModelInstanceDescription(model=Baseline, parameters={})
    ]

    features = ["LAT_x", "LAT_y", "LON_x", "LON_y"]

    forecast_task = ForecastTask(
        label="test forecast task",
        pipeline=pipeline,
        features=features,
        models=models,
        sequence_length=20,
        forecast_length=1,
        group_column="MMSI",
        training_parameters=TrainingParameters(epochs=50,
                                               validation_steps=1)
    )

    with Archive(filenames=input_files) as files:
        files = [x for x in files if AnnotatedDataFrame.get_supported_format(Path(x).suffix)]
        if not files:
            raise RuntimeError(f"No supported input files: {files=}")

        experiment = Experiment(learning_task=forecast_task,
                                input_data=files,
                                output_directory=tmp_path)
        report = experiment.run()
        print(report)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-f", "--input-files",
            nargs="+",
            type=str,
            required=True
    )

    args, unknown = parser.parse_known_args()

    run_experiment(input_files=args.input_files)


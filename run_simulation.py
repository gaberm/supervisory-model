from logging import config
import multiprocessing

from adapters.base_adapter import BaseAdapter
import hydra
import logging
from supervisory.supervisory_model import SupervisoryModel
from adapters import AdapterWorker, ChargingAdapter, TransportationAdapter


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()],
    )

    workers = [
        AdapterWorker.from_config(config.rabbitmq, model_cfg)
        for model_cfg in config.models.values()
    ]

    for w in workers:
        multiprocessing.Process(target=w.run).start()

    model = SupervisoryModel(config)
    if getattr(config.simulation, "reset_tables", False):
        model.reset_state_memory(drop_tables=True)
    model.run()


if __name__ == "__main__":
    main()

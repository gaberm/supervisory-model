import hydra
import logging
from supervisory.supervisory_model import SupervisoryModel


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()],
    )
    model = SupervisoryModel(config)
    model.run()


if __name__ == "__main__":
    main()

import hydra


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(config):
    pass


if __name__ == "__main__":
    main()

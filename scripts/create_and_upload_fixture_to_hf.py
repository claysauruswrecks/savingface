import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.fixtures import SimpleFixtureModel

from transformers import AutoModel


if __name__ == "__main__":
    config = {"num_channels": 3, "hidden_size": 32, "num_classes": 10}
    model = SimpleFixtureModel(config=config)

    model.push_to_hub("claysauruswrecks/simple_fixture_model", config=config)

    reloaded_model = AutoModel.from_pretrained("claysauruswrecks/simple_fixture_model")

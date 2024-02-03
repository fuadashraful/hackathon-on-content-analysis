import os
import yaml


def load_environment_variable(base_dir, env_name):
    env = os.path.join(base_dir, f"{env_name}.yml")

    with open(env, "r", encoding="utf8") as env_file:
        env_vars = yaml.safe_load(env_file)

        for key, value in env_vars.items():
            os.environ.setdefault(key, str(value))

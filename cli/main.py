import yaml

import common
from common import HyLangFile


class Cli:
    """Run the CLI version."""
    def __init__(self, args):
        self.args = args

    def run(self) -> common.Translations:
        if not self.args.input:
            raise SystemExit("Please specify --input (-i)")

        if self.args.verbose:
            print(f"Running in CLI mode")
            print(f"Input: {self.args.input}")
            print(f"Verbose: {self.args.verbose}")

        try:
            if self.args.input.endswith((".yaml", ".yml")):
                data = HyLangFile(self.args.input).load_yaml()
                flattend = HyLangFile.convert_yamldict_to_langdict(data)
                path = self.args.input.replace(".yaml", ".lang").replace(".yml", ".lang")
                HyLangFile.save_lang(path, flattend)

            elif self.args.input.endswith(".lang"):
                data = HyLangFile(self.args.input).load_lang()
            else:
                raise SystemExit("Please specify --input (-i) .lang/ .yaml or .yml")

            if self.args.verbose: print(data)

            return data

        except yaml.YAMLError as e:
            raise e
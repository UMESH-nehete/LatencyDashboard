from collections import defaultdict

class ExperimentManager:

    def __init__(self, experiments):

        self.raw = experiments

        self.experiments = {}

        self.build()

    def build(self):

        grouped = defaultdict(dict)

        for exp in self.raw:

            key = (

                exp["date"],

                exp["protocol"],

                exp["variant"]

            )

            grouped[key][exp["log_type"]] = exp

        self.experiments = grouped

    def keys(self):

        return list(self.experiments.keys())

    def get(self, date, protocol, variant):

        return self.experiments.get(

            (date, protocol, variant)

        )
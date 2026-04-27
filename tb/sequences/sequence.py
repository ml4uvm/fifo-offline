import pandas as pd
import os
import random
from pyuvm import uvm_sequence
from tb.sequences.sequence_item import FIFOSeqItem


class FIFOSequence(uvm_sequence):

    def __init__(self, name="FIFOSequence", num_tests=300, use_ml=False):
        super().__init__(name)
        self.num_tests = num_tests
        self.use_ml = use_ml

    # Same idea as ALU, but only for data_in
    def generate_value(self, t):
        if t == "ZERO":
            return 0
        elif t == "SMALL":
            return random.randint(1, 9)
        elif t == "LARGE":
            return random.randint(200, 255)
        elif t == "NEG":
            return random.randint(-20, -1)

    async def body(self):

        # =========================================================
        # ML MODE (clustered testcases)
        # =========================================================
        if self.use_ml:

            base_dir = os.path.dirname(__file__)
            csv_path = os.path.join(base_dir, "../../ml/clustered_tests.csv")

            df = pd.read_csv(csv_path)

            print(f"[ML MODE] Running {len(df)} testcases")

            reverse_map = {
                0: "ZERO",
                1: "SMALL",
                2: "LARGE",
                3: "NEG"
            }

            for _, row in df.iterrows():
                item = FIFOSeqItem("item")

                # Control signals directly from ML
                item.write_en = int(row['write_en'])
                item.read_en  = int(row['read_en'])

                # Data type → actual value
                data_type = reverse_map[int(row['data_type'])]
                item.data_type = data_type
                item.data_in = self.generate_value(data_type)

                await self.start_item(item)
                await self.finish_item(item)

        # =========================================================
        # BASELINE MODE (random)
        # =========================================================
        else:

            print(f"[BASELINE MODE] Running {self.num_tests} random tests")

            for _ in range(self.num_tests):
                item = FIFOSeqItem("item")
                item.randomize()

                await self.start_item(item)
                await self.finish_item(item)
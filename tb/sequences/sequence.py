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
     if self.use_ml:
        ...  # unchanged
        return

     print(f"[BASELINE MODE] Running {self.num_tests} guided tests")
     data_types = ["ZERO", "SMALL", "LARGE", "NEG"]
     dt_idx = 0

     # Scale fill/drain phases with the budget instead of hardcoding 20/20.
     # Reserve at least 25% of the budget for the Mixed phase so it never
     # gets starved out (previously: fixed 20+20, Mixed got num_tests-40,
     # which was negative/empty for any num_tests <= 40).
     fill_len = min(20, max(1, self.num_tests // 4))
     drain_len = fill_len
     mixed_len = max(0, self.num_tests - fill_len - drain_len)

     # PHASE 1: FILL FIFO
     for _ in range(fill_len):
        item = FIFOSeqItem("item")
        item.write_en = 1
        item.read_en = 0
        dt = data_types[dt_idx % 4]; dt_idx += 1
        item.data_type = dt
        item.data_in = self.generate_value(dt)
        await self.start_item(item)
        await self.finish_item(item)

     # PHASE 2: DRAIN FIFO
     for _ in range(drain_len):
        item = FIFOSeqItem("item")
        item.write_en = 0
        item.read_en = 1
        dt = data_types[dt_idx % 4]; dt_idx += 1
        item.data_type = dt
        item.data_in = self.generate_value(dt)
        await self.start_item(item)
        await self.finish_item(item)

     # PHASE 3: MIXED
     for _ in range(mixed_len):
        item = FIFOSeqItem("item")
        item.write_en = random.randint(0, 1)
        item.read_en = random.randint(0, 1)
        dt = data_types[dt_idx % 4]; dt_idx += 1
        item.data_type = dt
        item.data_in = self.generate_value(dt)
        await self.start_item(item)
        await self.finish_item(item)
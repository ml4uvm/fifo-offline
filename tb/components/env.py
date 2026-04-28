import os, csv
from pyuvm import uvm_env, uvm_agent, uvm_sequencer
from pyuvm.s12_uvm_tlm_interfaces import uvm_analysis_export
from tb.components.driver import FIFODriver
from tb.components.monitor import FIFOMonitor
from tb.components.scoreboard import FIFOScoreboard


# ===============================
# FIFO COVERAGE HELPERS
# ===============================

def get_fifo_state(full, empty):
    if empty:
        return "EMPTY"
    elif full:
        return "FULL"
    else:
        return "MID"


# 🔥 NEW: classify data_type from data_in
def classify_data(x):
    if x == 0:
        return "ZERO"
    elif 0 < x < 10:
        return "SMALL"
    else:
        return "LARGE"


def get_bin(write_en, read_en, state, data_type):
    return (write_en, read_en, state, data_type)


TOTAL_BINS = 2 * 2 * 3 * 4  # = 48
covered_bins = set()


# ===============================
# COVERAGE + CSV LOGGER
# ===============================
class CoverageExport(uvm_analysis_export):

    def build_phase(self):
        self.write = self.write

    def start_of_simulation_phase(self):
        os.makedirs("results", exist_ok=True)
        self.log_file = open("results/fifo_coverage_log.csv", "w", newline="")
        self.writer   = csv.writer(self.log_file)

        self.writer.writerow([
            "write_en",
            "read_en",
            "fifo_state",
            "data_type",
            "overflow",
            "underflow",
            "cov_gain",
            "gain_label"
        ])

    def write(self, item):

        fifo_state = get_fifo_state(item.full, item.empty)

        # 🔥 FIX: recompute data_type HERE (not from item)
        data_type = classify_data(item.data_in)

        overflow  = int(item.write_en == 1 and item.full == 1)
        underflow = int(item.read_en  == 1 and item.empty == 1)

        current_bin = get_bin(
            item.write_en,
            item.read_en,
            fifo_state,
            data_type
        )

        old_cov = len(covered_bins)
        covered_bins.add(current_bin)
        new_cov = len(covered_bins)

        coverage_gain = new_cov - old_cov
        gain_label = 1 if coverage_gain > 0 else 0

        self.writer.writerow([
            item.write_en,
            item.read_en,
            fifo_state,
            data_type,
            overflow,
            underflow,
            coverage_gain,
            gain_label
        ])

    def final_phase(self):
        self.log_file.close()
        print(f"Coverage: {len(covered_bins)}/{TOTAL_BINS} bins hit")


# ===============================
# AGENT
# ===============================
class FIFOAgent(uvm_agent):

    def build_phase(self):
        self.seqr    = uvm_sequencer("seqr", self)
        self.driver  = FIFODriver("driver", self)
        self.monitor = FIFOMonitor("monitor", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


# ===============================
# ENVIRONMENT
# ===============================
class FIFOEnv(uvm_env):

    def build_phase(self):
        self.agent      = FIFOAgent("agent", self)
        self.cov_export = CoverageExport("cov_export", self)
        self.scoreboard = FIFOScoreboard("scoreboard", self)

    def connect_phase(self):
        self.agent.monitor.ap.connect(self.cov_export)
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export)
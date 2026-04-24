import cocotb
from pyuvm import uvm_monitor, uvm_analysis_port
from cocotb.triggers import RisingEdge
from tb.sequences.sequence_item import FIFOSeqItem


class FIFOMonitor(uvm_monitor):

    def build_phase(self):
        self.ap  = uvm_analysis_port("ap", self)
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)

            item = FIFOSeqItem("observed")

            # Inputs
            item.write_en = int(self.dut.write_en.value)
            item.read_en  = int(self.dut.read_en.value)
            item.data_in  = int(self.dut.data_in.value)

            # Outputs
            item.data_out = int(self.dut.data_out.value)
            item.full     = int(self.dut.full.value)
            item.empty    = int(self.dut.empty.value)

            self.ap.write(item)
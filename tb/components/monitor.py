import cocotb
from pyuvm import uvm_monitor, uvm_analysis_port
from cocotb.triggers import RisingEdge
from tb.sequences.sequence_item import FIFOSeqItem


class FIFOMonitor(uvm_monitor):

    def build_phase(self):
        self.ap  = uvm_analysis_port("ap", self)
        self.dut = cocotb.top

        # pipeline register
        self.prev_item = None

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)

            curr = FIFOSeqItem("curr")

            curr.write_en = int(self.dut.write_en.value)
            curr.read_en  = int(self.dut.read_en.value)
            curr.data_in  = int(self.dut.data_in.value)

            curr.full  = int(self.dut.full.value)
            curr.empty = int(self.dut.empty.value)

            # data_out belongs to PREVIOUS cycle
            curr.data_out = int(self.dut.data_out.value)

            # --------------------------------
            # Send PREVIOUS cycle transaction
            # --------------------------------
            if self.prev_item is not None:
                self.prev_item.data_out = curr.data_out
                self.ap.write(self.prev_item)

            # store current for next cycle
            self.prev_item = curr
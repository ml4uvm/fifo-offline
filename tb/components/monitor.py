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

            # Capture inputs at this cycle
            write_en = int(self.dut.write_en.value)
            read_en  = int(self.dut.read_en.value)
            data_in  = int(self.dut.data_in.value)

            full  = int(self.dut.full.value)
            empty = int(self.dut.empty.value)

            # 🔥 If read, data_out is valid NEXT cycle
            if read_en:
                await RisingEdge(self.dut.clk)

            item = FIFOSeqItem("observed")

            item.write_en = write_en
            item.read_en  = read_en
            item.data_in  = data_in

            item.data_out = int(self.dut.data_out.value)
            item.full     = full
            item.empty    = empty

            self.ap.write(item)
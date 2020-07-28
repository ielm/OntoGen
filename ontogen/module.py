from ontoagent.config import OntoAgentConfig
from ontoagent.engine.module import OntoAgentReasoningModule, OntoAgentModuleRepository
from ontoagent.engine.xmr import TMR, XMR
from ontograph.Frame import Frame
from ontograph.Query import Query
from typing import Union

from ontogen.generate import generate


class OntoGenModule(OntoAgentReasoningModule):
    def handle_signal(self, tmr: TMR):
        """
        On signal input, generate tmr immediately. 
        """
        print(f"Received signal {tmr.anchor.id}")
        output = generate(tmr)
        return output

    def handle_heartbeat(self):
        """
        On heartbeat, OntoGen will check the generation queue (tbc) for oTMRs and if 
        it's not empty, call generate on the next oTMR. 
        """
        print("Heartbeat pulsed.")

    def allow(self, xmr: XMR) -> bool:
        pass


if __name__ == "__main__":

    m = OntoGenModule.instance()

    for i in range(5):
        tmr = TMR.instance()
        m.signal(tmr)
        m.heartbeat()

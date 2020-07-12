from ontoagent.config import OntoAgentConfig
from ontoagent.engine.module import OntoAgentReasoningModule, OntoAgentModuleRepository
from ontoagent.engine.xmr import TMR
from ontograph.Frame import Frame
from ontograph.Query import Query
from typing import Union

class OntoGenModule(OntoAgentReasoningModule):


    def handle_signal(self, tmr: TMR):
        print(f"Received signal {tmr.anchor.id}")

    def handle_heartbeat(self):
        print("Heartbeat pulsed.")


if __name__ == "__main__":

    m = OntoGenModule.instance()

    for i in range(5):
        tmr = TMR.instance()
        m.signal(tmr)
        m.heartbeat()

from typing import List
from .process import Process


class Pipeline:
    def __init__(self, processes : List[Process]):
        self.processes= processes

    def exec(self):
        for process in self.processes:
            process.run() 

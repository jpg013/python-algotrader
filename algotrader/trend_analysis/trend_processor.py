from queue import Queue
from .tf_static import TFStatic
from .tf_dynamic import TFDynamic

class TrendProcessor():
    def __init__(self, pipe):
        self.dataPipe = pipe
        #TFStatic("ema"),
        self.workers = [TFDynamic("ema")]
        self.run()

    def run(self):
        while True:
            data = self.dataPipe.recv()
            for worker in self.workers:
                worker.run(data)

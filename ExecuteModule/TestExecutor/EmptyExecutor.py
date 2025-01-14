from ExecuteModule.TestExecutor.BaseExecutor import Executor


class EmptyExecutor(Executor):

    def __init__(self):
        super().__init__()

    def exec(self):
        pass

import queue


class MLModel:
    pending_processes = queue.Queue()
    finished_processes = queue.Queue()

    @classmethod
    def start_ml_model(cls):
        while True:
            if not cls.pending_processes.empty():
                # Get the next pending process
                process = cls.pending_processes.get()
                # Add the process to the finished processes queue
                cls.finished_processes.put(process)

    @classmethod
    def add_task(cls, input_data):
        cls.pending_processes.put(input_data)
        return 'Task added successfully'

    @classmethod
    def get_result(cls):
        process = cls.finished_processes.get()
        if process is None:
            return 'No result yet'
        return process


class ValidationException(Exception):
    def __init__(self, content: dict, status_code: int):
        self.content = content
        self.status_code = status_code

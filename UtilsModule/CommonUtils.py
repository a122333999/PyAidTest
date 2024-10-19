from uuid import UUID


class CommonUtils:
    @staticmethod
    def checkUuid(data: str | UUID):
        if isinstance(data, UUID):
            if data.version == 4:
                return True
        if isinstance(data, str):
            try:
                if UUID(data).version == 4:
                    return True
            except ValueError:
                pass

        return False

    @staticmethod
    def strToBool(text: str, dft=False):
        text = text.upper()
        if text == "TRUE":
            return True
        elif text == "FALSE":
            return False
        return dft


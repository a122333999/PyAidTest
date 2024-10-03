from uuid import UUID


class CommonUtils:
    @staticmethod
    def checkUuid(data: str | UUID):
        if isinstance(data, UUID):
            if data.version == 4:
                return data
        if isinstance(data, str):
            try:
                temp = UUID(data)
                if temp.version == 4:
                    return temp
            except ValueError:
                return None




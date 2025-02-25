class ItemDTO:
    def __init__(self, item):
        self.id = item.id
        self.name = item.name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_model(item):
        return ItemDTO(item).to_dict() if item else None

    @staticmethod
    def from_model_list(items):
        return [ItemDTO(item).to_dict() for item in items]

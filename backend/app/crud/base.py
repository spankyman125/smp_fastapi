from app.database import Base

class ItemBase():
    def __init__(self, model: Base, like_relation: Base):
        self.model = model
        self.like_relation = like_relation

    def get(self):
        raise NotImplementedError("Not implemented")

    def get_all(self):
        raise NotImplementedError("Not implemented")

    def like():
        raise NotImplementedError("Not implemented")

    def get_liked():
        raise NotImplementedError("Not implemented")
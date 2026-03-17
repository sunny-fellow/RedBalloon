class ProblemRepository:

    def get_all(self, session):
        pass

    def get_by_id(self, session, id):
        pass

    def create(self, session, entity):
        session.add(entity)

    def delete(self, session, entity):
        session.delete(entity)

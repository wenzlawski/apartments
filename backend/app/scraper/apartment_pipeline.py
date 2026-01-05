from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.db import engine
from app.models import Apartment


class ApartmentPipeline:
    BATCH_SIZE = 50
    # Alternative throughput: Bulk async/COPY, Upsert batch

    def __init__(self):
        self.buffer = []

    def open_spider(self, spider):
        self.engine = engine

    def process_item(self, item, spider):
        self.buffer.append(item)

        if len(self.buffer) >= self.BATCH_SIZE:
            self.flush()

        return item

    def close_spider(self, spider):
        self.flush()

    def flush(self):
        if not self.buffer:
            return

        with Session(self.engine) as session:
            try:
                session.add_all([Apartment(**i) for i in self.buffer])
                session.commit()
            except IntegrityError:
                session.rollback()

        self.buffer.clear()

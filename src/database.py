import csv
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

Base = declarative_base()


class Canteen(Base):

    __tablename__ = "CANTEEN"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    time_open = Column(String)
    time_closed = Column(String)

    def __repr__(self):

        return "<Canteen(name='%s', location='%s', time_open='%s', time_closed='%s')>" % (
            self.name, self.location, self.time_open, self.time_closed)


instance_path = os.path.abspath('instance') # creates path for db in folder instance

engine = create_engine('sqlite:///' + os.path.join(instance_path, 'DINERS.db'), echo=True)


metadata = MetaData()
canteen_table = Table(
    'CANTEEN',
    metadata,
    Column('ID', Integer(), primary_key=True),
    Column('Name', String()),
    Column('Location', String()),
    Column('time_open', String()),
    Column('time_closed', String())
)

metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def read_file(file_path):

    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        next(csvreader)
        session = Session()
        for row in csvreader:
            name = row[0].strip()
            location = row[1].strip()

            time_open = row[3].strip().split('-')[0].replace('.', ':')
            time_closed = row[3].strip().split('-')[1].replace('.', ':')

            canteen = Canteen(name=name, location=location, time_open=time_open, time_closed=time_closed)

            existing_canteen = session.query(Canteen).filter_by(name=name, location=location).first()

            if not existing_canteen:
                session.add(canteen)

        session.commit()
        session.close()


read_file("../canteens/Canteens.csv")  # your csv file here

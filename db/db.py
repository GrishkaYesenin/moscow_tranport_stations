from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db/forecast.db', echo=True)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "forecast"
    id = Column(Integer, primary_key=True)
    stop_id = Column(Integer)
    route_path_id = Column(Integer)
    forecast_time = Column(Integer)
    byTelemetry = Column(Integer)
    tmId = Column(Integer)
    routePathId = Column(String)
    request_time = Column(Integer)


class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True)
    stop_id = Column(String)
    name = Column(String)

    route_path_id = Column(String)
    transport_type = Column(String)
    number = Column(String)
    last_stop_name = Column(String)


Base.metadata.create_all(engine)

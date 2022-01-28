import logging
from db.db import engine
from models import Stop
from station import stops
from api import TransAPI
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from logging import basicConfig
import threading
from multiprocessing import Queue
from config import NUM_THREADS

api = TransAPI()
session = sessionmaker(bind=engine)()
stops_coords = list(stops())
basicConfig(level=logging.DEBUG, filemode="w", filename="load_stops.log")

def thread_job():
    """Поток получает координаты остановок из очереди и занимается парсингом"""
    while not stops.empty():
        lon, lat = coords = stops.get()
        print(f"Thread is working with {coords}")
        stop = Stop.parse_obj(api.get_station_info(lon, lat))
        # print(f"{stop}")
        stop.save_stop(session)
    print("Thread finish working")
    return None

stops = Queue()
for stop in stops_coords:
    coord = lon, lat = stop["Lon"], stop["Lat"]
    stops.put(coord)

NUM_THREADS = min(len(stops_coords) - 1, NUM_THREADS)

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=thread_job, name=f"{i}")
    t.start()
    threads.append(t)

for t in threads:
    print(f"Waiting for Thread {t.name}")
    t.join()
    print(f"Thread {t.name} finished")

session.commit()

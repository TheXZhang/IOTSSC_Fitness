import time
import joblib
import datetime
import psycopg2
from mbed_cloud import ConnectAPI
from math import pi

GYRO_RESOURCE = "/3334/0"
ACCELERO_RESOURCE = "/3313/0"
add_row = """insert into classification (timestamp, classification) values (%s, %s) """
add_walking = """update achievement set walking = achievement.walking +1 where id = 1"""
add_running = """update achievement set running = achievement.running +1 where id = 1"""

conn = psycopg2.connect(dbname='iotssc', user='tester', password='password')

clf = joblib.load("svm_model.pkl")


def _run_synchronized():
    api = ConnectAPI()
    api.start_notifications()
    devices = api.list_connected_devices().data

    if not devices:
        raise Exception("No devices registered. Aborting")

    while True:
        # Will get the resource value for button and block the thread whilst doing it
        # See the async example for details on what the 'sync' flag does in the background.
        # Note this will raise a CloudAsyncError if something goes wrong, which we're not catching
        # here for simplicity.
        gyro_new_value = api.get_resource_value(devices[0].id, GYRO_RESOURCE)
        acceler_new_value = api.get_resource_value(devices[0].id, ACCELERO_RESOURCE)
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")
        hour = current_time.hour
        minutes = current_time.minute
        seconds = current_time.second
        microsecond = current_time.microsecond

        accX, accY, accZ = acceler_new_value.values()
        accX, accY, accZ = (float(accX) / 1000), (float(accY) / 1000), (float(accZ) / 1000)
        gyroX, gyroY, gyroZ = gyro_new_value.values()
        gyroX, gyroY, gyroZ = ((float(gyroX) / 1000 / 360) * (pi / 180)), ((float(gyroY) / 1000 / 360) * (pi / 180)), (
            (float(gyroZ) / 1000 / 360) * (pi / 180))

        pred = clf.predict([[accX, accY, accZ, gyroX, gyroY, gyroZ, hour, minutes, seconds, microsecond]])
        print(accX, accY, accZ)
        print(gyroX, gyroY, gyroZ)
        print("gyro {}".format(gyro_new_value))
        print("accelero{}".format(acceler_new_value))

        if pred[0] == 0:
            classification = 'walking'
        else:
            classification = 'running'

        with conn.cursor() as cursor:
            cursor.execute(add_row, (timestamp, classification))
        conn.commit()
        print("row added")


def _run_async():
    api = ConnectAPI()
    api.start_notifications()
    devices = api.list_connected_devices().data
    if not devices:
        raise Exception("No devices registered. Aborting")

    gyro_cur = acceler_cur = None
    while True:
        gyro_resp = api.get_resource_value_async(devices[0].id, GYRO_RESOURCE)
        acceler_resp = api.get_resource_value_async(devices[0].id, ACCELERO_RESOURCE)

        # Busy wait - block the thread and wait for the response to finish.
        while not gyro_resp.is_done:
            time.sleep(0.1)

        while not acceler_resp.is_done:
            time.sleep(0.1)

        # Check if we have a async error response, and abort if it is.
        if gyro_resp.error:
            continue
            raise Exception("Got async error response: %r" % gyro_resp.error)

        if acceler_resp.error:
            continue
            raise Exception("Got async error response: %r" % acceler_resp.error)

        # Get the value from the async response, as we know it's done and it's not
        # an error.
        gyro_new_value = gyro_resp.value
        acceler_new_value = acceler_resp.value

        # Print new value to user, if it has changed.
        if gyro_cur != gyro_new_value and acceler_cur != acceler_new_value:

            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")
            hour = current_time.hour
            minutes = current_time.minute
            seconds = current_time.second
            microsecond = current_time.microsecond

            accX, accY, accZ = acceler_new_value.values()
            accX, accY, accZ = (float(accX) / 1000), (float(accY) / 1000), (float(accZ) / 1000)
            gyroX, gyroY, gyroZ = gyro_new_value.values()
            gyroX, gyroY, gyroZ = ((float(gyroX) / 1000) * (pi / 180)), ((float(gyroY) / 1000) * (pi / 180)), (
                (float(gyroZ) / 1000) * (pi / 180))

            # pred = clf.predict([[accX, accY, accZ, gyroX, gyroY, gyroZ, hour, minutes, seconds, microsecond]])
            start = time.time()
            pred = clf.predict([[accX, accY, accZ, gyroX, gyroY, gyroZ]])
            stop = time.time()
            print(f"classifying time: {stop - start}")
            # print(accX, accY, accZ)
            # print(gyroX, gyroY, gyroZ)
            # print("gyro {}".format(gyro_new_value))
            # print("accelero{}".format(acceler_new_value))

            if pred[0] == 0:
                classification = 'walking'
            else:
                classification = 'running'

            with conn.cursor() as cursor:
                cursor.execute(add_row, (timestamp, classification))
                if classification == 'walking':
                    cursor.execute(add_walking)
                else:
                    cursor.execute(add_running)

            conn.commit()
            print(classification)
            print("row added")

            # Save new current value
            gyro_cur = gyro_new_value
            acceler_cur = acceler_new_value


if __name__ == "__main__":
    # These two methods are doing the same, but one is showing the behaviour of the
    # 'sync' flag to `get_resource`, and the `run_async` shows how you can have
    # a bit more fine grained control.
    # _run_synchronized()
    _run_async()

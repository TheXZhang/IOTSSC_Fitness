import psycopg2
import select
import ast
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pyfcm import FCMNotification

push_service = FCMNotification(
    api_key="AAAAsMhar-E:APA91bE5kRx7Bm6chDeSrA7z8Oq2S5AGCe_X_MabGBPwdskbPh2pQ79H4rQXA3wehQJd3UD1vNxaxrYax5U7mzKh4lnzZE86O-N3JSw3O15y31dRk53YmzYZMQz6px_SmELbCL0m6fRY")
registration_id = "djovPtlXTemQHzbVVgOjyV:APA91bG-GeFuUiz5D3cSQHpAJErhxf6pSqqCx5UIumG7Zvep1xig-oylIJ2-S3MLCTSA40tOBpeezE1aC2XVDfqc0X5A_gloItNPH_Jab0MR1SAOB6bAykMvTV-YqqG3eS6mhYvP-oJz"
message_title = "Achievement"

run_10 = False
run_100 = False
run_1000 = False

walk_10 = False
walk_100 = False
walk_1000 = False

connection = psycopg2.connect(dbname='iotssc', user='tester', password='password')

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = connection.cursor()
cur.execute("LISTEN achievement;")
while True:
    select.select([connection], [], [])
    connection.poll()
    events = []
    while connection.notifies:
        notify = connection.notifies.pop().payload
        notify_dict = ast.literal_eval(notify)
        print(notify_dict)

        if notify_dict['running'] == 30 and run_10 is False:
            run_10 = True
            print("running 30 achieved")
            message_body = "You have reached running achievement {}".format(10)
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
        if notify_dict['walking'] == 35 and walk_10 is False:
            walk_10 = True
            print("walking 10 achieved")
            message_body = "You have reached walking achievement {}".format(10)
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
        if notify_dict['running'] == 100 and run_100 is False:
            run_100 = True
            print("running 10 achieved")
            message_body = "You have reached running achievement {}".format(100)
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
        if notify_dict['walking'] == 100 and walk_100 is False:
            walk_100 = True
            print("walking 100 achieved")
            message_body = "You have reached walking achievement {}".format(100)
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)

        if notify_dict['running'] == 1000 and run_1000 is False:
            run_1000 = True
            print("running 1000 achieved")
            message_body = "You have reached running achievement {}".format(1000)
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
        if notify_dict['walking'] == 1000 and walk_1000 is False:
            walk_1000 = True
            print("walking 1000 achieved")
            message_body = "You have reached walking achievement {}".format(1000)
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)

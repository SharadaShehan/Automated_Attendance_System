import sys, os, functools
from Database import connect_to_database, get_users_data
from RabbitMQ import connect_to_rabbitmq, process_messages, process_single_message
from MessageHandler import callback_function
from MosquittoMQTT import connect_to_mqtt
from CloudMonitoring import get_monitoring_obj

def main():
    db_conn = connect_to_database()
    if db_conn is None:
        print("Exiting...")
        return

    rabbitmq_channel = connect_to_rabbitmq()
    if rabbitmq_channel is None:
        print("Exiting...")
        return

    mqtt_client = connect_to_mqtt()
    if mqtt_client is None:
        print("Exiting...")
        return

    users_data = get_users_data(db_conn)
    if users_data is None:
        print("Exiting...")
        return
    print(users_data)

    monitoringObj = get_monitoring_obj()

    partial_callback = functools.partial(callback_function, users_data, db_conn, mqtt_client, monitoringObj)

    process_messages(rabbitmq_channel, partial_callback)

    print("Closing connections...")
    db_conn.close()
    mqtt_client.disconnect()
    rabbitmq_channel.close()

    print("Main function exited")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


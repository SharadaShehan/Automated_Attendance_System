from google.cloud import monitoring_v3
import time
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

def get_monitoring_obj():
    try:
        project_id = os.getenv('GCP_PROJECT_ID')
        gce_instance_id = os.getenv('GCE_INSTANCE_ID')
        gcp_zone = os.getenv('GCP_ZONE')
        credentials = Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        return MonitoringObj(project_id, gce_instance_id, gcp_zone, credentials)
    except Exception as error:
        print("Error while creating monitoring client:", error)
        return None


class MonitoringObj:
    def __init__(self, project_id, gce_instance_id, gcp_zone, credentials):
        self.project_name = f"projects/{project_id}"
        self.gce_instance_id = gce_instance_id
        self.gcp_zone = gcp_zone
        self.client = monitoring_v3.MetricServiceClient(credentials=credentials)

    def create_time_series(self, metric_name, metric_label_name, value):
        try:
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/{metric_name}"
            series.resource.type = "gce_instance"
            series.resource.labels["instance_id"] = self.gce_instance_id
            series.resource.labels["zone"] = self.gcp_zone
            series.metric.labels["label"] = metric_label_name
            now = time.time()
            seconds = int(now)
            nanos = int((now - seconds) * 10 ** 9)
            print(f"Seconds: {seconds}, Nanos: {nanos}")
            interval = monitoring_v3.TimeInterval(
                {"end_time": {"seconds": seconds, "nanos": nanos}}
            )
            point = monitoring_v3.Point({"interval": interval, "value": {"double_value": value}})
            series.points = [point]
            self.client.create_time_series(name=self.project_name, time_series=[series])
            return True
        except Exception as error:
            print("Error while creating time series:", error)
            return False

    def write_new_message_metric(self, message_value):
        return self.create_time_series("new_message", "Message Reception", message_value)

    def write_attendance_updated_metric(self, attendance_value):
        return self.create_time_series("attendance_updated", "Attendance Update", attendance_value)

    def write_mqtt_publish_metric(self, publish_value):
        return self.create_time_series("mqtt_publish", "MQTT Publish", publish_value)

    def write_error_metric(self, error_value):
        return self.create_time_series("error", "Error", error_value)




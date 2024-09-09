from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def view_index(self):
        self.client.get("/")

    @task(1)
    def view_analytics(self):
        self.client.get("/analytics")

    @task(1)
    def view_settings(self):
        self.client.get("/settings")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")

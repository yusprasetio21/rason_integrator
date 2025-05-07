from locust import HttpUser, task, between

class SandiTest(HttpUser):
    # Define the host URL directly in the class
    # host = "http://172.19.0.202"
    host = "http://192.168.15.187:9081"
        
    # Wait time between tasks in seconds
    wait_time = between(0.1, 0.5)
    
    # @task
    # def test_post_request(self):
    #     # Define the payload for the POST request as a dictionary
    #     payload = {
    #         "message": "SAID52 WITN 050100\nAAXX 05014\n9612312 abcd"
    #     }
        
    #     # Send POST request with form-encoded data
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #     response = self.client.post("/cgi-bin/cmcgi/cmss_web_input.process.pl", data=payload, headers=headers)
        
    #     # Check response status code and print results for debugging
    #     if response.status_code == 200:
    #         print("Request was successful!")
    #     else:
    #         print("Request failed with status:", response.status_code)

    @task
    def test_post_request(self):
        # Define the payload for the POST request as a dictionary
        payload = {
            "username":"96745",
            "password":"opr96745"
        }
        
        # Send POST request with form-encoded data
        response = self.client.post("/db/bmkgsatu/@login", json=payload)
        
        # Check response status code and print results for debugging
        if response.status_code == 200:
            print("Request was successful!")
        else:
            print("Request failed with status:", response.status_code)
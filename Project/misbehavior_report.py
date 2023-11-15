import requests

class MisbehaviorReport:
    def __init__(self, access_token):
        self.path = "https://api.endpoint.com/misbehavior-report"
        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    def submit(self, report_data):
        response = requests.post(self.path, headers=self.headers, json=report_data)
        
        #handle errors
        if response.status_code != 200:
            self.handle_errors(response)
        else:
            print("Misbehavior report submitted successfully.")

    def handle_errors(self, response):
        error_code = response.status_code
        error_detail = response.headers.get("Ieee-1609.2.1-Error")
        
        if error_code == 400 and error_detail:
            errors_map = {
                "400-10": "Absent encryption.",
                "400-40": "Failed certificate chain verification.",
                "400-42": "Failed parsing.",
                "403-43": "Failed signature verification.",
                "400-60": "Invalid appPermissions.",
                "400-81": "Wrong RA."
            }
            print(errors_map.get(error_detail, "Unknown error."))
        
        elif error_code == 500:
            print("Internal server error.")
        
        else:
            print(f"Error {error_code}: {response.text}")

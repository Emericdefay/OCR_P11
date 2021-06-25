from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    """Simulate user actions"""
    wait_time = between(0.5, 1)

    @task
    def display_board(self):
        """Load display board"""
        with self.client.get("/displayBoard", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Request took too long")

    @task
    def book(self):
        """Load book page"""
        competition = "Spring Festival"
        club = "Simply Lift"
        path = f"/book/{competition}/{club}"
        with self.client.get(path, catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Request took too long")

    @task
    def purchase(self):
        """Purchase actions or try to (if not places anymore)"""
        competition = "Spring Festival"
        club = "Simply Lift"
        path = "/purchasePlaces"
        form = {
                "competition": competition,
                "club": club,
                "places": 1,
                }

        with self.client.post(path, form, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long")

    def on_start(self):
        """On start, connect the user."""
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

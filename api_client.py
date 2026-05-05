import requests

class GitHubAPIClient:
    BASE_URL = "https://api.github.com"

    @staticmethod
    def search_users(username):
        if not username:
            return None, "Поле поиска не может быть пустым"

        url = f"{GitHubAPIClient.BASE_URL}/search/users"
        params = {'q': username}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            return None, f"Ошибка при запросе к API: {e}"


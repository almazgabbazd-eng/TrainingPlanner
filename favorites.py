import json
import os

class FavoritesManager:
    FAVORITES_FILE = "data/favorites.json"

    @staticmethod
    def load_favorites():
        if os.path.exists(FavoritesManager.FAVORITES_FILE):
            with open(FavoritesManager.FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def save_favorites(favorites):
        with open(FavoritesManager.FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)

    @staticmethod
    def add_favorite(user):
        favorites = FavoritesManager.load_favorites()
        if user not in favorites:
            favorites.append(user)
            FavoritesManager.save_favorites(favorites)
            return True
        return False

    @staticmethod
    def remove_favorite(username):
        favorites = FavoritesManager.load_favorites()
        updated = [user for user in favorites if user['login'] != username]
        if len(updated) < len(favorites):
            FavoritesManager.save_favorites(updated)
            return True
        return False

import tkinter as tk
from tkinter import ttk, messagebox
from api_client import GitHubAPIClient
from favorites import FavoritesManager

class GitHubUserFinderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        # Поле ввода поиска
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Имя пользователя GitHub:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Найти", command=self.search_users).pack(side=tk.LEFT)

        # Список результатов
        results_frame = ttk.LabelFrame(self.root, text="Результаты поиска")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("login", "name", "location", "public_repos")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления избранным
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=5)

        ttk.Button(buttons_frame, text="Добавить в избранное",
                   command=self.add_to_favorites).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Удалить из избранного",
                   command=self.remove_from_favorites).pack(side=tk.LEFT, padx=5)

        # Список избранных
        favorites_frame = ttk.LabelFrame(self.root, text="Избранные пользователи")
        favorites_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.favorites_listbox = tk.Listbox(favorites_frame)
        self.favorites_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_favorites()

    def search_users(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не может быть пустым")
            return

        data, error = GitHubAPIClient.search_users(username)
        if error:
            messagebox.showerror("Ошибка API", error)
            return

        self.display_results(data.get('items', []))

    def display_results(self, users):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in users:
            self.tree.insert("", tk.END, values=(
                user.get('login', ''),
                user.get('name', 'N/A'),
                user.get('location', 'N/A'),
                user.get('public_repos', 0)
            ))

    def add_to_favorites(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из результатов")
            return

        item = self.tree.item(selected[0])['values']
        user_data = {
            'login': item[0],
            'name': item[1],
            'location': item[2],
            'public_repos': item[3]
        }

        if FavoritesManager.add_favorite(user_data):
            messagebox.showinfo("Успех", f"{user_data['login']} добавлен в избранное")
            self.load_favorites()
        else:
            messagebox.showinfo("Информация", "Пользователь уже в избранном")

    def remove_from_favorites(self):
        selection = self.favorites_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из избранных")
            return

        username = self.favorites_listbox.get(selection[0])
        if FavoritesManager.remove_favorite(username):
            messagebox.showinfo("Успех", f"{username} удалён из избранного")
            self.load_favorites()

    def load_favorites(self):
        self.favorites_listbox.delete(0, tk.END)
        favorites = FavoritesManager.load_favorites()
        for user in favorites:
            self.favorites_listbox.insert(tk.END, user['login'])

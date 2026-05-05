import tkinter as tk
from ui import GitHubUserFinderUI

def main():
    root = tk.Tk()
    app = GitHubUserFinderUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

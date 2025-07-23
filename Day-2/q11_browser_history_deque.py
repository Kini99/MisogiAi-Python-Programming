from collections import deque

class BrowserHistory:
    def __init__(self, max_size=5):
        self.history = deque(maxlen=max_size)  # stores visited URLs (most recent at end)
        self.forward_stack = deque()           # stores URLs that were backed out

    def add_page(self, url):
        if len(self.history) == self.history.maxlen:
            print(f"History full. Removing oldest page: {self.history[0]}")
        self.history.append(url)
        self.forward_stack.clear()  # New visit clears forward stack
        self.print_state(f"Visited: {url}")

    def go_back(self):
        if len(self.history) > 1:
            last_page = self.history.pop()
            self.forward_stack.append(last_page)
            self.print_state(f"Back to: {self.history[-1]}")
        else:
            print("Can't go back. Only one page in history.")

    def go_forward(self):
        if self.forward_stack:
            forward_page = self.forward_stack.pop()
            self.history.append(forward_page)
            self.print_state(f"Forward to: {forward_page}")
        else:
            print("Can't go forward. Forward stack is empty.")

    def print_state(self, action):
        print(f"\n{action}")
        print("History       :", list(self.history))
        print("Forward Stack :", list(self.forward_stack))
        print("-" * 40)

# Example usage:
browser = BrowserHistory()

browser.add_page("google.com")
browser.add_page("openai.com")
browser.add_page("github.com")
browser.add_page("stackoverflow.com")
browser.add_page("wikipedia.org")
browser.add_page("netflix.com")  # Will remove google.com due to size limit

browser.go_back()
browser.go_back()
browser.go_forward()
browser.add_page("amazon.in")    # Will clear forward stack
browser.go_back()

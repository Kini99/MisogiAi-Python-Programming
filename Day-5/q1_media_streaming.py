from abc import ABC, abstractmethod

# ===================== Abstract Base Classes =======================

class MediaContent(ABC):
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        self.ratings = []

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def get_duration(self):
        pass

    @abstractmethod
    def get_file_size(self):
        pass

    @abstractmethod
    def calculate_streaming_cost(self):
        pass

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.ratings.append(rating)

    def get_average_rating(self):
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)

    def is_premium_content(self):
        return self.get_average_rating() > 4.0

class StreamingDevice(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def stream_content(self, content: MediaContent):
        pass

    @abstractmethod
    def adjust_quality(self):
        pass

    def get_device_info(self):
        return f"{self.name} streaming device"

    def check_compatibility(self, content: MediaContent):
        return True

# ===================== Concrete Media Content =======================

class Movie(MediaContent):
    def __init__(self, title, genre, duration, resolution, director):
        super().__init__(title, genre)
        self.duration = duration  # in minutes
        self.resolution = resolution
        self.director = director

    def play(self):
        return f"Playing movie: {self.title}"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return self.duration * 5  # simplistic: 5MB per minute

    def calculate_streaming_cost(self):
        return 0.05 * self.duration  # 5 cents per minute

class TVShow(MediaContent):
    def __init__(self, title, genre, seasons, total_episodes, current_episode):
        super().__init__(title, genre)
        self.seasons = seasons
        self.total_episodes = total_episodes
        self.current_episode = current_episode

    def play(self):
        return f"Playing episode {self.current_episode} of {self.title}"

    def get_duration(self):
        return self.total_episodes * 45  # assume 45 minutes per episode

    def get_file_size(self):
        return self.total_episodes * 45 * 3  # 3MB per minute

    def calculate_streaming_cost(self):
        return self.total_episodes * 0.25  # 25 cents per episode

class Podcast(MediaContent):
    def __init__(self, title, genre, duration, episode_number, transcript_available):
        super().__init__(title, genre)
        self.duration = duration  # in minutes
        self.episode_number = episode_number
        self.transcript_available = transcript_available

    def play(self):
        return f"Playing podcast episode {self.episode_number}: {self.title}"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return self.duration * 2  # 2MB per minute

    def calculate_streaming_cost(self):
        return 0.02 * self.duration

class Music(MediaContent):
    def __init__(self, title, genre, duration, artist, album, lyrics_available):
        super().__init__(title, genre)
        self.duration = duration  # in seconds
        self.artist = artist
        self.album = album
        self.lyrics_available = lyrics_available

    def play(self):
        return f"Playing music: {self.title} by {self.artist}"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return self.duration * 0.5  # 0.5MB per second

    def calculate_streaming_cost(self):
        return 0.01 * (self.duration / 60)  # 1 cent per minute

# ===================== Concrete Devices =======================

class SmartTV(StreamingDevice):
    def __init__(self, name, screen_size, has_surround_sound):
        self.name = name
        self.screen_size = screen_size
        self.has_surround_sound = has_surround_sound

    def connect(self):
        message = f"{self.name} connected via HDMI."
        print(message)
        return message


    def stream_content(self, content):
        message = f"Streaming '{content}' on Laptop"
        print(message)
        return {"device": "Laptop", "content": content, "status": "streaming", "quality": "1080p"}

    def adjust_quality(self):
        print("Auto-adjusting quality for large screen and surround sound.")

    def get_device_info(self):
        return {
            "type": "SmartTV",
            "name": self.name,
            "screen_size": self.screen_size,
            "surround_sound": self.has_surround_sound
        }

    def check_compatibility(self, content):
        return True


class Laptop(StreamingDevice):
    def __init__(self, brand, ram_gb, has_gpu):
        self.brand = brand
        self.ram_gb = ram_gb
        self.has_gpu = has_gpu

    def connect(self):
        print(f"{self.brand} laptop connected via WiFi.")
        return f"{self.brand} laptop connected via WiFi."

    def stream_content(self, content):
        print(f"Streaming '{content.title}' on {self.brand} laptop.")
        return {"device": self.brand, "content": content.title, "status": "streaming", "quality": "1080p"}

    def adjust_quality(self):
        print("Adjusting quality based on RAM and GPU.")

    def get_device_info(self):
        return {
            "type": "Laptop",
            "brand": self.brand,
            "ram_gb": self.ram_gb,
            "has_gpu": self.has_gpu
        }

    def check_compatibility(self, content):
        return self.ram_gb >= 4


class Mobile(StreamingDevice):
    def __init__(self, brand, screen_size, is_5g_enabled):
        self.brand = brand
        self.screen_size = screen_size
        self.is_5g_enabled = is_5g_enabled

    def connect(self):
        print(f"{self.brand} mobile connected via 5G." if self.is_5g_enabled else f"{self.brand} mobile connected via 4G.")
        return f"{self.brand} mobile connected via 5G." if self.is_5g_enabled else f"{self.brand} mobile connected via 4G."

    def stream_content(self, content):
        print(f"Streaming '{content.title}' on {self.brand} mobile.")
        return {"device": self.brand, "content": content.title, "status": "streaming", "quality": "720p"}

    def adjust_quality(self):
        print("Optimizing for mobile data and small screen.")

    def get_device_info(self):
        return {
            "type": "Mobile",
            "brand": self.brand,
            "screen_size": self.screen_size,
            "5g": self.is_5g_enabled
        }

    def check_compatibility(self, content):
        return content.duration <= 1800  # 30 minutes max


class SmartSpeaker(StreamingDevice):
    def __init__(self, name, supports_voice_commands, max_volume):
        self.name = name
        self.supports_voice_commands = supports_voice_commands
        self.max_volume = max_volume

    def connect(self):
        print(f"{self.name} speaker connected via Bluetooth.")
        return f"{self.name} speaker connected via Bluetooth."

    def stream_content(self, content):
        print(f"Playing '{content.title}' on {self.name} speaker.")
        return {"device": self.name, "content": content.title, "status": "streaming", "quality": "audio only"}

    def adjust_quality(self):
        print("Adjusting audio quality based on volume level.")

    def get_device_info(self):
        return {
            "type": "SmartSpeaker",
            "name": self.name,
            "voice_commands": self.supports_voice_commands,
            "max_volume": self.max_volume
        }

    def check_compatibility(self, content):
        return hasattr(content, "is_audio") and content.is_audio

# ===================== User & Platform =======================

class User:
    def __init__(self, name, subscription_tier="Free"):
        self.name = name
        self.subscription_tier = subscription_tier
        self.watch_history = []
        self.preferences = []

    def watch(self, content: MediaContent):
        self.watch_history.append(content.title)
        if content.genre not in self.preferences:
            self.preferences.append(content.genre)

    def get_watch_history(self):
        return self.watch_history

    def get_preferences(self):
        return self.preferences

    def upgrade_subscription(self, tier):
        self.subscription_tier = tier

class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.content_library = []

    def register_user(self, user: User):
        self.users.append(user)

    def add_content(self, content: MediaContent):
        self.content_library.append(content)

    def recommend_content(self, user: User):
        preferred_genres = user.get_preferences()
        for content in self.content_library:
            if content.genre in preferred_genres:
                return content
        return None

    def stream_to_device(self, user: User, content: MediaContent, device: StreamingDevice):
        if device.check_compatibility(content):
            return device.stream_content(content)
        return "Incompatible content or device"



# Test Case 1: Abstract class instantiation should fail
try:
    content = MediaContent("Test", "Test Category")
    assert False, "Should not be able to instantiate abstract class"
except TypeError:
    pass

try:
    device = StreamingDevice("Test Device")
    assert False, "Should not be able to instantiate abstract class"
except TypeError:
    pass

# Test Case 2: Polymorphic content creation and playback
movie = Movie("Inception", "Sci-Fi", 148, "4K", "Christopher Nolan")
tv_show = TVShow("Breaking Bad", "Drama", 5, 62, 1)
podcast = Podcast("Tech Talk", "Technology", 45, 15, True)
music = Music("Bohemian Rhapsody", "Rock", 355, "Queen", "A Night at the Opera", True)

contents = [movie, tv_show, podcast, music]

# All should implement required abstract methods
for content in contents:
    play_result = content.play()
    assert isinstance(play_result, str)
    assert "playing" in play_result.lower()

    duration = content.get_duration()
    assert isinstance(duration, (int, float))
    assert duration > 0

    file_size = content.get_file_size()
    assert isinstance(file_size, (int, float))

    cost = content.calculate_streaming_cost()
    assert isinstance(cost, (int, float))
    assert cost >= 0

# Test Case 3: Device-specific streaming behavior
smart_tv = SmartTV("Samsung 4K TV", "55 inch", True)
laptop = Laptop("MacBook Pro", "13 inch", "Intel i7")
mobile = Mobile("iPhone 13", "iOS", 85)
speaker = SmartSpeaker("Amazon Echo", "Alexa", True)

devices = [smart_tv, laptop, mobile, speaker]

for device in devices:
    connect_result = device.connect()
    assert "connected" in connect_result.lower()

    # Test polymorphic streaming
    stream_result = device.stream_content(movie)
    assert isinstance(stream_result, dict)
    assert "quality" in stream_result
    assert "status" in stream_result

# Test Case 4: Device-content compatibility
# Smart speaker should only play audio content
audio_content = [podcast, music]
video_content = [movie, tv_show]

for content in audio_content:
    result = speaker.stream_content(content)
    assert result["status"] == "success"

for content in video_content:
    result = speaker.stream_content(content)
    assert result["status"] == "error" or "audio only" in result.get("message", "")

# Test Case 5: User subscription and platform integration
user = User("john_doe", "Premium", ["Sci-Fi", "Drama"])
platform = StreamingPlatform("NetStream")

# Add content to platform
for content in contents:
    platform.add_content(content)

# Register user and device
platform.register_user(user)
platform.register_device(smart_tv, user)

# Test recommendation system
recommendations = platform.get_recommendations(user)
assert isinstance(recommendations, list)
assert len(recommendations) > 0

# Test watch history and analytics
watch_session = platform.start_watching(user, movie, smart_tv)
assert watch_session["status"] == "started"

analytics = platform.get_user_analytics(user)
assert "total_watch_time" in analytics
assert "favorite_genres" in analytics

# Test Case 6: Subscription tier restrictions
free_user = User("jane_doe", "Free", ["Comedy"])
platform.register_user(free_user)

# Premium content should be restricted for free users
premium_movie = Movie("Premium Film", "Action", 120, "4K", "Director")
premium_movie.is_premium = True
platform.add_content(premium_movie)

watch_attempt = platform.start_watching(free_user, premium_movie, laptop)
assert watch_attempt["status"] == "error"
assert "subscription" in watch_attempt["message"].lower()

# Test Case 7: Content rating and recommendation impact
movie.add_rating(4.5)
movie.add_rating(4.8)
movie.add_rating(4.2)

assert abs(movie.get_average_rating() - 4.5) < 0.1

# Highly rated content should appear in recommendations
new_recommendations = platform.get_recommendations(user)
highly_rated = [content for content in new_recommendations if content.get_average_rating() > 4.0]
assert len(highly_rated) > 0

print("✅ All tests passed!")

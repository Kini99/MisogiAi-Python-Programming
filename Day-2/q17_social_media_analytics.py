from collections import Counter, defaultdict

posts = [
    {"id": 1, "user": "alice", "content": "Love Python programming!", "likes": 15, "tags": ["python", "coding"]},
    {"id": 2, "user": "bob", "content": "Great weather today", "likes": 8, "tags": ["weather", "life"]},
    {"id": 3, "user": "alice", "content": "Data structures are fun", "likes": 22, "tags": ["python", "learning"]},
]

users = {
    "alice": {"followers": 150, "following": 75},
    "bob": {"followers": 89, "following": 120},
}

# Most Popular Tags - Use collections.Counter
def most_popular_tags():
    all_tags = []
    for post in posts:
        all_tags.extend(post["tags"])
    
    tag_counter = Counter(all_tags)
    print("Most popular tag: ",tag_counter)

# User Engagement Analysis - Use defaultdict
def user_engagement_analysis():
    user_likes = defaultdict(int)
    for post in posts:
        user_likes[post["user"]] += post["likes"]
    
    print("User engagement analysis - user likes: ",user_likes)

# Top Posts by Likes - Use sorted()
def top_posts_by_likes():
    print("Top posts by likes: ",sorted(posts, key=lambda post: post["likes"], reverse=True))

# User Activity Summary - Combine post and user data
def user_activity_summary():
    # Get user engagement data
    user_likes = user_engagement_analysis()
    
    user_post_count = defaultdict(int)
    for post in posts:
        user_post_count[post["user"]] += 1

    summary = {}
    for user in users:
        summary[user] = {
            "posts_count": user_post_count[user],
            "total_likes": user_likes[user],
            "followers": users[user]["followers"],
            "following": users[user]["following"]
        }
    
    print("User activity summary: ",summary)

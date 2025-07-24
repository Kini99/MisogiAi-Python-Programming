def analyze_friendships():
    facebook_friends = {"alice", "bob", "charlie", "diana", "eve", "frank"}
    instagram_friends = {"bob", "charlie", "grace", "henry", "alice", "ivan"}
    twitter_friends = {"alice", "diana", "grace", "jack", "bob", "karen"}
    linkedin_friends = {"charlie", "diana", "frank", "grace", "luke", "mary"}

    # 1. Friends on all four platforms
    all_platforms = facebook_friends & instagram_friends & twitter_friends & linkedin_friends

    # 2. Friends only on Facebook (not on any other platform)
    facebook_only = facebook_friends - (instagram_friends | twitter_friends | linkedin_friends)

    # 3. Friends on Instagram OR Twitter but NOT both (XOR)
    instagram_xor_twitter = instagram_friends.symmetric_difference(twitter_friends)

    # 4. Total unique friends across all platforms
    total_unique = facebook_friends | instagram_friends | twitter_friends | linkedin_friends

    # 5. Friends on exactly 2 platforms
    # Count appearances across sets
    appearances = {}
    platforms = [facebook_friends, instagram_friends, twitter_friends, linkedin_friends]
    for platform in platforms:
        for friend in platform:
            appearances[friend] = appearances.get(friend, 0) + 1
    exactly_two_platforms = {friend for friend, count in appearances.items() if count == 2}

    return {
        'all_platforms': all_platforms,
        'facebook_only': facebook_only,
        'instagram_xor_twitter': instagram_xor_twitter,
        'total_unique': total_unique,
        'exactly_two_platforms': exactly_two_platforms
    }


# Test the function
result = analyze_friendships()
print("All platforms:", result.get('all_platforms'))
print("Facebook only:", result.get('facebook_only'))
print("Instagram XOR Twitter:", result.get('instagram_xor_twitter'))
print("Total unique friends:", result.get('total_unique'))
print("Exactly 2 platforms:", result.get('exactly_two_platforms'))
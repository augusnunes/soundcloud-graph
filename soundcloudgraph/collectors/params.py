# from operator import attrgetter
# TODO
# colocar como attrgetter


def get_config():
    params = {
        "user":[
            "id", 
            "followers_count", 
            "full_name", 
            "permalink", 
            "permalink_url", 
            "username", 
            "verified", 
            "city", 
            "country_code",
        ],
        "comment": [
            "id", 
            "body", 
            "created_at", 
            "track_id", 
            "user_id",
        ],
        "track": [
            "id", 
            "permalink", 
            "permalink_url", 
            "title", 
            "user_id", 
            "full_duration", 
            "public", 
            "policy", 
            "monetization_model",
            "created_at",
            "genre",
            "description",
            "purchase_url",
            "reposts_count",
            "tag_list",
            "comment_count",
            "playback_count",
        ],
        "like": [
            "created_at",
            "track.id", 
            "track.user_id", 
        ],
        "tracklike":[
            "created_at",
            "track.id", 
            "track.user_id",
        ],
        "playlistlike":[
            "created_at",
            "playlist.id",
            "playlist.user_id",
        ],
        "playlist": [
            "id", 
            "created_at", 
            "description", 
            "genre", 
            "likes_count", 
            "duration", 
            "permalink", 
            "permalink_url", 
            "public", 
            "licence", 
            "tag_list", 
            "user_id", 
            "title", 
            "reposts_count", 
            "set_type", 
            "track_count", 
            "published_at",
        ],
        "album": [
            "id", 
            "created_at", 
            "description", 
            "genre", 
            "likes_count", 
            "duration", 
            "permalink", 
            "permalink_url", 
            "public", 
            "licence", 
            "tag_list", 
            "user_id", 
            "title", 
            "reposts_count", 
            "set_type", 
            "track_count", 
            "published_at"
        ],
        "repost": [
            "created_at",
            "caption",
            "user.id",
            "track.user.id"
            "track.id",
            "track.user_id",
        ],
        "stream": [
            "created_at",
            "media",
            "is_repost",
            "media_id",
            "media_artist_id"
        ]
    }
    return params
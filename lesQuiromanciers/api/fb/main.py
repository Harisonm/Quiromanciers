import pandas as pd
import requests
import facebook
import json


def main():
    
    perms: ["manage_pages", "publish_pages"]
    with open("api/fb/src/config.json", "r") as f:
        distros_dict = json.load(f)

    graph = facebook.GraphAPI(access_token=distros_dict["acces_token"], version="2.12")
    result = graph.get_object(
        parent_object="me",
        connection_name="feed",
        fields=["name", "birthday", "likes"],
        id="me",
    )
    print(result)

    result = graph.get_object(
        parent_object="me", connection_name="feed", fields=["hometown"], id="me"
    )
    print(result)
    # # Write a comment on a post.
    # graph.put_object(parent_object='post_id', connection_name='comments',
    #                  message='First!')


if __name__ == "__main__":
    main()

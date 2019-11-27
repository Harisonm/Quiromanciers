import pandas as pd
import requests
import facebook


def main():
    auth = facebook.FACEBOOK_OAUTH_DIALOG_PATH()
    auth.get_access_token_from_code(app_id='572754506881706', app_secret='4017459b518ca0f309106670fad1e8af')
    # graph = facebook.GraphAPI(
    #     access_token="",
    #     version="2.12")
    #
    # # Write 'Hello, world' to the active user's wall.
    # result = graph.get_object(parent_object='me', connection_name='feed', fields=['name', 'user_birthday'], id='me')
    # print(result)
    # Add a link and write a message about it.
    # graph.put_object(
    #     parent_object="me",
    #     connection_name="feed",
    #     message="This is a great website. Everyone should visit it.",
    #     link="https://www.facebook.com")
    #
    # # Write a comment on a post.
    # graph.put_object(parent_object='post_id', connection_name='comments',
    #                  message='First!')


if __name__ == "__main__":
    main()

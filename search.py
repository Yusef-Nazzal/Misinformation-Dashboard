from mastodon import Mastodon

instance_url = 'https://mastodon.social'
client_id = 'H7NhHfUi-jnAIy0DW_2aUR0Yu65LH3D7eqhsnQmAGog'
client_secret = 'XyKu4up2nZnR65ZemcLQgZ2dgh0s7B_yYCtsziAF7tQ'
access_token = 'TPHK86OOqhMKrnjwdkpHeTRk39zoqrWsKUW5OufuCc8'

mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=access_token,
    api_base_url=instance_url
)


def search_for_toots(keyword, max_results=200):
    if ' ' in keyword:
        search_query = f'"{keyword}"'
    else:
        search_query = f'{keyword}'
    search_results = []
    max_id = None
    while len(search_results) < max_results:
        try:
            page_results = mastodon.search(q=search_query, max_id=max_id)
            if not page_results['statuses']:
                break
            search_results.extend(page_results['statuses'])
            max_id = page_results['statuses'][-1]['id']
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return search_results[:max_results]

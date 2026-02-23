# anixart.py

> Unofficial Python wrapper for the [Anixart](https://anixart.tv) mobile API — explore a wide variety of Japanese animation works programmatically.

<p align="center">
  <img src="https://anixart-app.com/assets/images/logo.svg" alt="Anixart Logo" width="200"/>
</p>

---

## Installation

> No package yet — just drop `anixart.py` into your project.

---

## Quick Start

```python
import anixart

client = anixart.Anixart()
client.login(login="example@gmail.com", password="password")
```

---

## Features

- 🔐 **Auth** — login, register, email/password/login changes
- 👤 **Profiles** — user info, comments, watch lists, social links
- 🎌 **Releases** — search, info, voting, favorites, schedule
- 💬 **Comments** — post, edit, report, like on releases and collections
- 👥 **Friends** — requests, recommendations, block list
- 🔔 **Notifications** — counts and alerts
- 🔍 **Search** — releases and profiles
- 📚 **Collections** — browse curated lists
- 🌐 **Discover** — trending discussions, interesting content

---

## Usage

### Authentication

```python
client = anixart.Anixart()

# Login (automatically stores token and user_id)
client.login(login="example@gmail.com", password="password")

# Register
client.register(email="example@gmail.com", password="password", login="username")

# Change credentials
client.change_password(current_password="old", new_password="new")
client.change_email(current_email="old@mail.com", new_email="new@mail.com", password="pass")
```

### Releases

```python
# Get release info
client.get_release_info(release_id=1)

# Search
client.search_release(query="Attack on Titan")

# Vote (1–10 stars)
client.vote_release(release_id=1, star=9)

# Add to watch list (status: 1=watching, 2=completed, 3=planned, etc.)
client.add_into_profile_list(release_id=1, status=1)

# Favorites
client.add_release_to_favorite(release_id=1)
client.delete_release_from_favorite(release_id=1)
```

### Comments

```python
# Post a comment on a release
client.send_comment(message="Great anime!", release_id=1)

# Reply to a comment
client.send_comment(message="Agreed!", release_id=1, reply_to="user_id", spoiler=False)

# Edit a comment
client.edit_comment(message="Updated text", release_comment_id=42)
```

### Friends

```python
client.send_friend_request(user_id=123)
client.accept_friend_request(user_id=123)
client.get_user_friends(user_id=123)
client.get_friend_recommendations()
```

### Profile

```python
client.get_user_info(user_id=123)
client.edit_profile_status(status="Watching everything 👀")
client.edit_profile_social(tg_page="https://t.me/username", vk_page="https://vk.com/username")
client.get_user_profile_list(user_id=123)
```

---

## API Reference

| Category      | Method                          | Description                        |
|---------------|---------------------------------|------------------------------------|
| Auth          | `login`                         | Sign in and store token            |
| Auth          | `register`                      | Create new account                 |
| Auth          | `verify_registration`           | Confirm registration code          |
| Auth          | `change_password`               | Update password                    |
| Auth          | `change_email`                  | Update email                       |
| Auth          | `change_login`                  | Update login/username              |
| Profile       | `get_user_info`                 | Get user profile                   |
| Profile       | `edit_profile_status`           | Update status text                 |
| Profile       | `edit_profile_social`           | Update social links                |
| Profile       | `get_user_profile_list`         | Get user's watch list              |
| Profile       | `get_user_comments`             | Get user's comments                |
| Profile       | `get_user_voted_releases`       | Releases user has voted on         |
| Releases      | `get_release_info`              | Detailed release info              |
| Releases      | `get_random_release`            | Random release                     |
| Releases      | `search_release`                | Search releases by query           |
| Releases      | `vote_release`                  | Vote on a release                  |
| Releases      | `report_release`                | Report a release                   |
| Releases      | `add_into_profile_list`         | Add to watch list                  |
| Releases      | `add_release_to_favorite`       | Add to favorites                   |
| Comments      | `send_comment`                  | Post a comment                     |
| Comments      | `edit_comment`                  | Edit a comment                     |
| Comments      | `get_release_comments`          | Get comments for a release         |
| Comments      | `report_release_comment`        | Report a comment                   |
| Friends       | `send_friend_request`           | Send a friend request              |
| Friends       | `accept_friend_request`         | Accept a friend request            |
| Friends       | `get_friend_recommendations`    | Get suggested friends              |
| Friends       | `get_user_friends`              | List user's friends                |
| Block list    | `block_user`                    | Block a user                       |
| Block list    | `unblock_user`                  | Unblock a user                     |
| Block list    | `get_block_list`                | View blocked users                 |
| Discover      | `discover_discussing`           | Trending discussions               |
| Discover      | `discover_interesting`          | Interesting content                |
| Collections   | `get_collections`               | Browse collections                 |
| Notifications | `get_notification_count`        | Unread notification count          |
| Search        | `search_profile`                | Search users by query              |

---

## Notes

- All methods return a `dict` parsed from the API JSON response.
- `login()` automatically stores the session token — no need to pass it manually to subsequent calls.
- This is an **unofficial** wrapper and is not affiliated with or endorsed by Anixart.

---

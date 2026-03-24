from requests import Session

class Anixart:
    def __init__(self) -> None:
        self.api = "https://api.anixart.tv"
        self.session = Session()
        self.session.headers = {
            "User-Agent": "AnixartApp/8.1.2-23031801 (Android 9; SDK 28; x86_64; Asus ASUS_I003DD; ru)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "api.anixart.tv"
        }
        self.token = None
        self.user_id = None

    def _post(self, path: str, data: dict = None, use_json: bool = False) -> dict:
        kwargs = {"json": data} if use_json else {"data": data}
        return self.session.post(f"{self.api}{path}", **kwargs).json()

    def _get(self, path: str) -> dict:
        return self.session.get(f"{self.api}{path}").json()

    def _with_token(self, path: str) -> str:
        sep = "&" if "?" in path else "?"
        return f"{path}{sep}token={self.token}"

    def login(self, login: str, password: str) -> dict:
        data = {
            "login": login,
            "password": password
        }
        response = self._post("/auth/signIn", data)
        if "profile" in response:
            self.token = response["profileToken"]["token"]
            self.user_id = response["profile"]["id"]
        return response

    def register(
            self,
            email: str,
            password: str,
            login: str) -> dict:
        data = {
            "login": login,
            "email": email,
            "password": password
        }
        return self._post("/auth/signUp", data)

    def verify_registration(
            self,
            login: str,
            email: str,
            password: str,
            code: int,
            registration_hash: str) -> dict:
        data = {
            "login": login,
            "email": email,
            "password": password,
            "code": code,
            "hash": registration_hash
        }
        return self._post("/auth/verify", data)

    def get_login_firebase(self) -> dict:
        return self._post(f"/auth/firebase?token={self.token}")

    def get_user_info(self, user_id: int) -> dict:
        return self._get(self._with_token(f"/profile/{user_id}"))

    def get_user_nickname_history(
            self, user_id: int, page: int = 0) -> dict:
        return self._get(
            f"/profile/login/history/all/{user_id}/{page}")

    def get_block_list(self, page: int = 0) -> dict:
        return self._get(self._with_token(f"/profile/blocklist/all/{page}"))

    def block_user(self, user_id: int) -> dict:
        return self._post(self._with_token(f"/profile/blocklist/add/{user_id}"))

    def unblock_user(self, user_id: int) -> dict:
        return self._post(self._with_token(f"/profile/blocklist/remove/{user_id}"))

    def get_user_voted_releases(
            self, user_id: int, sort: int = 1, page: int = 0) -> dict:
        return self._get(self._with_token(
            f"/profile/vote/release/voted/{user_id}/{page}?sort={sort}"))

    def get_user_unvoted_releases(
            self, user_id: int, sort: int = 1, page: int = 0) -> dict:
        return self._get(self._with_token(
            f"/profile/vote/release/unvoted/{user_id}/{page}?sort={sort}"))

    def get_all_type_of_sounds(self) -> dict:
        return self._get(self._with_token("/type/all"))

    def get_user_friends(self, user_id: int, page: int = 0) -> dict:
        return self._get(self._with_token(f"/profile/friend/all/{user_id}/{page}"))

    def edit_profile_status(self, status: str) -> dict:
        data = {"status": status}
        return self._post(self._with_token("/profile/preference/status/edit"),
            data, use_json=True)

    def edit_profile_social(
            self,
            inst_page: str = None,
            tg_page: str = None,
            vk_page: str = None,
            tt_page: str = None,
            discord_page: str = None) -> dict:
        data = {
            "instPage": inst_page,
            "tgPage": tg_page,
            "vkPage": vk_page,
            "ttPage": tt_page,
            "discordPage": discord_page
        }
        filtered = {k: v for k, v in data.items() if v is not None}
        return self._post(self._with_token("/profile/preference/social/edit"),
            filtered, use_json=True)

    def get_release_info(
            self, release_id: int, extended_mode: bool = True) -> dict:
        return self._get(self._with_token(
            f"/release/{release_id}?extended_mode={extended_mode}"))

    def search_release(self, query: str) -> dict:
        data = {"query": query, "searchBy": 0}
        return self._post(self._with_token("/search/releases/0"), data)

    def search_profile(self, query: str) -> dict:
        data = {"query": query, "searchBy": 0}
        return self._post(self._with_token("/search/profiles/0"), data)

    def get_random_release(self, extended_mode: bool = True) -> dict:
        return self._get(self._with_token(
            f"/release/random?extended_mode={extended_mode}"))

    def get_release_comments(
            self, release_id: int, page: int = 0, sort: int = 0) -> dict:
        return self._get(self._with_token(
            f"/release/comment/all/{release_id}/{page}?sort={sort}"))

    def get_collections(self, page: int = 0) -> dict:
        return self._get(self._with_token(f"/collection/all/{page}"))

    def send_comment(
            self,
            message: str,
            release_id: int = None,
            collection_id: int = None,
            parent_comment_id: str = None,
            reply_to: str = None,
            spoiler: bool = False) -> dict:
        data = {
            "message": message,
            "parentCommentId": parent_comment_id,
            "replyToProfileId": reply_to,
            "spoiler": spoiler
        }
        if release_id:
            path = self._with_token(f"/release/comment/add/{release_id}")
        else:
            path = self._with_token(f"/collection/comment/add/{collection_id}")
        return self._post(path, data, use_json=True)

    def edit_comment(
            self,
            message: str,
            release_comment_id: int = None,
            collection_comment_id: int = None,
            spoiler: bool = False) -> dict:
        data = {
            "message": message,
            "spoiler": spoiler
        }
        if release_comment_id:
            path = self._with_token(f"/release/comment/edit/{release_comment_id}")
        elif collection_comment_id:
            path = self._with_token(f"/collection/comment/edit/{collection_comment_id}")
        else:
            raise ValueError("Either release_comment_id or collection_comment_id must be provided")
        return self._post(path, data, use_json=True)

    def discover_discussing(self) -> dict:
        return self._post(self._with_token("/discover/discussing"))

    def discover_interesting(self) -> dict:
        return self._post("/discover/interesting")

    def discover_comments(self) -> dict:
        return self._post("/discover/comments")

    def discover_collections(self) -> dict:
        return self._post("/discover/collections")

    def get_schedule(self) -> dict:
        return self._get(self._with_token("/schedule"))

    def get_friend_requests(self) -> dict:
        return self._get(self._with_token("/profile/friend/requests/in/last"))

    def get_sent_friend_requests(self) -> dict:
        return self._get(self._with_token("/profile/friend/requests/out/last"))

    def get_friend_recommendations(self) -> dict:
        return self._get(self._with_token("/profile/friend/recommendations"))

    def send_friend_request(self, user_id: int) -> dict:
        return self._get(self._with_token(
            f"/profile/friend/request/send/{user_id}"))

    def accept_friend_request(self, user_id: int) -> dict:
        return self._get(self._with_token(
            f"/profile/friend/request/accept/{user_id}"))

    def get_notification_count(self) -> dict:
        return self._get(self._with_token("/notification/count"))

    def vote_release(self, release_id: int, star: int) -> dict:
        return self._get(self._with_token(
            f"/release/vote/add/{release_id}/{star}"))

    def add_into_profile_list(
            self, release_id: int, status: int = 3) -> dict:
        return self._get(self._with_token(
            f"/profile/list/add/{status}/{release_id}"))

    def delete_from_profile_list(
            self, release_id: int, status: int = 3) -> dict:
        return self._get(self._with_token(
            f"/profile/list/delete/{status}/{release_id}"))

    def add_release_to_favorite(self, release_id: int) -> dict:
        return self._get(self._with_token(f"/favorite/add/{release_id}"))

    def delete_release_from_favorite(self, release_id: int) -> dict:
        return self._get(self._with_token(f"/favorite/delete/{release_id}"))

    def report_release(
            self,
            release_id: int,
            message: str,
            reason: int) -> dict:
        """
        RELEASE-REPORT REASON-TYPES:
            1 - MISTAKE IN DESIGN,
            2 - MISSING SOME SERIES,
            3 - OTHER
        """
        data = {
			"message": message,
			"reason": reason
		}
        return self._post(self._with_token(f"/release/report/{release_id}"), data)

    def report_release_comment(
            self,
            comment_id: int,
            message: str,
            reason: int) -> dict:
        """
        COMMENT-REPORT REASON-TYPES:
            1 - SPAM,
            2 - INSULTS,
            3 - HARASSMENT,
            4 - SPOILER,
            5 - OTHER
        """
        data = {
			"message": message,
			"reason": reason
		}
        return self._post(
            self._with_token(f"/release/comment/report/{comment_id}"), data)

    def get_release_comment_votes(
            self,
            comment_id: int,
            page: int = 0,
            sort: int = 0) -> dict:
        return self._get(self._with_token(
            f"/release/comment/votes/{comment_id}/{page}?sort={sort}"))

    def get_user_profile_list(
            self,
            user_id: int,
            page: int = 1,
            sort: int = 1) -> dict:
        return self._get(self._with_token(
            f"/profile/list/all/{user_id}/{page}/0?sort={sort}"))

    def get_user_comments(
            self,
            user_id: int,
            page: int = 0,
            sort: int = 0) -> dict:
        return self._get(self._with_token(
            f"/release/comment/all/profile/{user_id}/{page}?sort={sort}"))

    def get_login_info(self) -> dict:
        return self._get(self._with_token("/profile/preference/login/info"))

    def change_login(self, login: str) -> dict:
        return self._post(self._with_token(
            f"/profile/preference/login/change?login={login}"))

    def change_password(
            self,
            current_password: str,
            new_password: str) -> dict:
        return self._get(self._with_token(
            f"/profile/preference/password/change?current={current_password}&new={new_password}"))

    def change_email(
            self,
            current_email: str,
            new_email: str,
            password: str) -> dict:
        return self._get(self._with_token(
            f"/profile/preference/email/change?current_password={password}&current={current_email}&new={new_email}"))

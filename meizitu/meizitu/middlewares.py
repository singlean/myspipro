

from fake_useragent import UserAgent

class RandomUserAgent(object):

    user_agent = UserAgent()

    def process_request(self, request, spider):

        request.headers["User-Agent"] = self.user_agent.chrome

from weixin.settings import USER_AGENT_LIST
import random

class RandomUserAgent(object):

    def process_request(self, request, spider):

        UA = random.choice(USER_AGENT_LIST)
        cookies = "noticeLoginFlag=1; pgv_pvi=5210948608; pt2gguin=o2859609774; RK=4I5UPGkF5o; ptcz=771b7a80a81f5c5a861397390d53cdc5ac09a0f777b867192db3c1eddb6d0de6; pgv_pvid=5435302976; o_cookie=2859609774; sd_userid=41401531748490619; sd_cookie_crttime=1531748490619; ua_id=E6fSX6j9M7UjYWMOAAAAAFXw3CqS2hWXurBymxzg98A=; mm_lang=zh_CN; eas_sid=D1I593W1g8I3u7e4j0Z8K5R7A2; LW_uid=d1A5R3I1R8Z337U4K1c4N9x1y9; pgv_pvid_new=2859609774_11409b5d1b0; LW_sid=r1i5s3g293x4k0u6A5S84799S8; noticeLoginFlag=1; pgv_si=s5516811264; uuid=d6969f9e6d1cfebeff0ccb2d86aabb30; bizuin=3536931030; ticket=96ea7130628c83a1c2601c612394f2d459e1a559; ticket_id=gh_3f82fd35e8a0; cert=i1VFrUzVyWhoyAx3ZnocXfoyRCux3LWb; data_bizuin=3536931030; data_ticket=Vn/wqjTlZGnKCzp+ju4EkRH64Oii3cfzhO90+yWMBpnRxW8rGn5iewL8apRzSpoF; slave_sid=Y0VxMk9MVE1TQ0JfZUl5ak54RDhENlFoNkI3WjFaQktjeFcyM0RlR3ZXSG9BWktBSUxKYUkwaGRrbGpQWWVpbFZKNEd5dWJfN2l1ZlhpYjE1cWRKUG5mVTJqUm5UbUZvRnE5Z3YycVdoU2pGVWxNNkhYRlk5WEF6NkVSRXQyQ082ZE9lYTg0MXg0R055T3c4; slave_user=gh_3f82fd35e8a0; xid=089b26c6c571d84f64ee3413c9823dd3; openid2ticket_o1kjR0p9U6-C_TLGkDMxnn2H0zwU=hPDxLXD+y8qjKf49g1fVDoOYSq/drASgMCch+W9CpO8="
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}

        request.headers["User-Agent"] = UA
        request.cookies = cookies





















































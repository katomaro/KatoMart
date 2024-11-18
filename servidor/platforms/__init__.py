# platforms/__init__.py
from .hotmart import HotmartScraper
# from .astronmembers import AstronScraper
# from .kiwify import KiwifyScraper
# from .memberkit import MemberkitScraper
# from .nutror import NutrorScraper
# from .themembers import TheMembersScraper
# from .cademi import CademiScraper

def get_platform_scraper(platform_name, auth_data, session=None, course_id=None):
    if platform_name == 'hotmart':
        return HotmartScraper(auth_data=auth_data, session=session, course_id=course_id)
    # elif platform_name == 'astronmembers':
    #     return AstronScraper(auth_data=auth_data, session=session, course_id=course_id)
    # elif platform_name == 'nutror':
    #     return NutrorScraper(auth_data=auth_data, session=session, course_id=course_id)
    # elif platform_name == 'kiwify':
    #     return KiwifyScraper(auth_data=auth_data, session=session, course_id=course_id)
    # elif platform_name == 'memberkit':
    #     return MemberkitScraper(auth_data=auth_data, session=session, course_id=course_id)
    # elif platform_name == 'themembers':
    #     return TheMembersScraper(auth_data=auth_data, session=session, course_id=course_id)
    # elif platform_name == 'cademi':
    #     return CademiScraper(auth_data=auth_data, session=session, course_id=course_id)
    else:
        raise ValueError(f'Unknown platform: {platform_name}')

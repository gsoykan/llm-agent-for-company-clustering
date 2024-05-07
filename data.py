from enum import Enum

from pydantic import BaseModel
from typing import List, Optional, Any, Set

"""
@dataclass
class StartupPartner:
    company_name: str
    logo_url: str
    city: str
    country: str
    theme_gd: str
    typename: StartupPartnerTypename
    website: Optional[str] = None
"""


class StartupPartner(BaseModel):
    company_name: str
    logo_url: str
    city: str
    website: Optional[str] = None
    country: str
    theme_gd: str


class StartupFriendlyBadge(Enum):
    NO = "NO"
    YES = "YES"


"""
@dataclass
class TopRankedCorporate:
    id: UUID
    name: str
    description: str
    logo_url: str
    industry: None
    hq_city: str
    hq_country: str
    website_url: str
    linkedin_url: str
    startup_partners_count: int
    startup_partners: List[StartupPartner]
    typename: TopRankedCorporateTypename
    twitter_url: Optional[str] = None
    startup_friendly_badge: Optional[StartupFriendlyBadge] = None
"""


class Corporate(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    hq_city: str
    hq_country: Optional[str] = None
    website_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    startup_partners_count: int
    startup_partners: List[StartupPartner]
    # startup_friendly_badge: Optional[StartupFriendlyBadge] = None
    startup_themes: Set[str] = set()  # initialize as empty set

    def model_post_init(self, __context: Any) -> None:
        self.startup_themes = set(
            [item.strip() for partner in self.startup_partners for item in partner.theme_gd.split(',')])

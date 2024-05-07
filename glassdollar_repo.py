from typing import List, Dict

import requests
import json

from data import Corporate

# manually found requests
"""SearchBar
curl 'https://ranking.glassdollar.com/graphql' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://ranking.glassdollar.com/' -H 'content-type: application/json' -H 'Origin: https://ranking.glassdollar.com' -H 'Alt-Used: ranking.glassdollar.com' -H 'Connection: keep-alive' -H 'Cookie: fpestid=YVan2ApqsxuXoRoEgkz-9EwdCIS2dt5s1QC40RfHoWBcGm7_EDX6yrNBSm_Ja4oABJ_drA; _ga_SX8XLCG27H=GS1.1.1714656951.2.1.1714656954.0.0.0; _ga=GA1.2.858478662.1714637900; _cc_id=6780a9ec248bff4d42e42e72f11b115a; panoramaId_expiry=1714724301061; _gid=GA1.2.1981828823.1714637905; pubconsent-v2=YAAAAAAAAAAA; euconsent-v2=CP9_GsAP9_GsAAZACBENAyEsAP_gAH_gAAAAKJNV_H__bW1r8X73aft0eY1P9_j77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIEu3bBIQNlHJDUTVCgaogVryDMakWcgTNKJ6BkiFMRO2dYCF5vmwtj-QKY5vr993dx2D-t_dv83dzyz4VHn3a5_2e0WJCdA58tDfv9bROb-9IPd_58v4v0_F_rE2_eT1l_tevp7D8-ct87_XW-9_fff79Ll98FEgCzDQqIA6wJCQg0DCKBACoKwgIoEAAAAJA0QEAJgwKdgYBLrCRACAFAAMEAIAAUZAAgAAAgAQiACAAoEAAEAgUAAIAAAgEABAwAAgAsBAIAAQHQIUwIIFAsAEjMiIUwIQoEggJbKhBIAgQVwhCLPAAgERMFAAAAAAVgACAsFgcSSAlQkECXEG0AABAAgEEIFQgk5MAAQJGy1B4Im0ZWkAaGnCAA.YAAAAAAAAAAA' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"operationName":"GIMGetSearchResults","variables":{"where":{"query":"babb"}},"query":"query GIMGetSearchResults($where: searchBarWhere) {\n  searchBar(where: $where)\n}\n"}'

"""

"""Get Company Details
curl 'https://ranking.glassdollar.com/graphql' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://ranking.glassdollar.com/corporates/8483fc50-b82d-5ffa-5f92-6c72ac4bdaff' -H 'content-type: application/json' -H 'Origin: https://ranking.glassdollar.com' -H 'Alt-Used: ranking.glassdollar.com' -H 'Connection: keep-alive' -H 'Cookie: fpestid=YVan2ApqsxuXoRoEgkz-9EwdCIS2dt5s1QC40RfHoWBcGm7_EDX6yrNBSm_Ja4oABJ_drA; _ga_SX8XLCG27H=GS1.1.1714656951.2.1.1714657289.0.0.0; _ga=GA1.2.858478662.1714637900; _cc_id=6780a9ec248bff4d42e42e72f11b115a; panoramaId_expiry=1714724301061; _gid=GA1.2.1981828823.1714637905; pubconsent-v2=YAAAAAAAAAAA; euconsent-v2=CP9_GsAP9_GsAAZACBENAyEsAP_gAH_gAAAAKJNV_H__bW1r8X73aft0eY1P9_j77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIEu3bBIQNlHJDUTVCgaogVryDMakWcgTNKJ6BkiFMRO2dYCF5vmwtj-QKY5vr993dx2D-t_dv83dzyz4VHn3a5_2e0WJCdA58tDfv9bROb-9IPd_58v4v0_F_rE2_eT1l_tevp7D8-ct87_XW-9_fff79Ll98FEgCzDQqIA6wJCQg0DCKBACoKwgIoEAAAAJA0QEAJgwKdgYBLrCRACAFAAMEAIAAUZAAgAAAgAQiACAAoEAAEAgUAAIAAAgEABAwAAgAsBAIAAQHQIUwIIFAsAEjMiIUwIQoEggJbKhBIAgQVwhCLPAAgERMFAAAAAAVgACAsFgcSSAlQkECXEG0AABAAgEEIFQgk5MAAQJGy1B4Im0ZWkAaGnCAA.YAAAAAAAAAAA' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"variables":{"id":"8483fc50-b82d-5ffa-5f92-6c72ac4bdaff"},"query":"query ($id: String!) {\n  corporate(id: $id) {\n    id\n    name\n    description\n    logo_url\n    hq_city\n    hq_country\n    website_url\n    linkedin_url\n    twitter_url\n    startup_partners_count\n    startup_partners {\n      master_startup_id\n      company_name\n      logo_url: logo\n      city\n      website\n      country\n      theme_gd\n      __typename\n    }\n    startup_themes\n    startup_friendly_badge\n    __typename\n  }\n}\n"}'
"""

""" Get Corporate Count
curl 'https://ranking.glassdollar.com/graphql' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://ranking.glassdollar.com/' -H 'content-type: application/json' -H 'Origin: https://ranking.glassdollar.com' -H 'Alt-Used: ranking.glassdollar.com' -H 'Connection: keep-alive' -H 'Cookie: fpestid=YVan2ApqsxuXoRoEgkz-9EwdCIS2dt5s1QC40RfHoWBcGm7_EDX6yrNBSm_Ja4oABJ_drA; _ga_SX8XLCG27H=GS1.1.1714661337.3.0.1714661337.0.0.0; _ga=GA1.2.858478662.1714637900; _cc_id=6780a9ec248bff4d42e42e72f11b115a; panoramaId_expiry=1714724301061; _gid=GA1.2.1981828823.1714637905; pubconsent-v2=YAAAAAAAAAAA; euconsent-v2=CP9_GsAP9_GsAAZACBENAyEsAP_gAH_gAAAAKJNV_H__bW1r8X73aft0eY1P9_j77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIEu3bBIQNlHJDUTVCgaogVryDMakWcgTNKJ6BkiFMRO2dYCF5vmwtj-QKY5vr993dx2D-t_dv83dzyz4VHn3a5_2e0WJCdA58tDfv9bROb-9IPd_58v4v0_F_rE2_eT1l_tevp7D8-ct87_XW-9_fff79Ll98FEgCzDQqIA6wJCQg0DCKBACoKwgIoEAAAAJA0QEAJgwKdgYBLrCRACAFAAMEAIAAUZAAgAAAgAQiACAAoEAAEAgUAAIAAAgEABAwAAgAsBAIAAQHQIUwIIFAsAEjMiIUwIQoEggJbKhBIAgQVwhCLPAAgERMFAAAAAAVgACAsFgcSSAlQkECXEG0AABAAgEEIFQgk5MAAQJGy1B4Im0ZWkAaGnCAA.YAAAAAAAAAAA' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"variables":{},"query":"{\n  corporateCount: getCorporateCount\n}\n"}'

"""

"""Get Top Ranked Companies
curl 'https://ranking.glassdollar.com/graphql' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://ranking.glassdollar.com/' -H 'content-type: application/json' -H 'Origin: https://ranking.glassdollar.com' -H 'Alt-Used: ranking.glassdollar.com' -H 'Connection: keep-alive' -H 'Cookie: fpestid=YVan2ApqsxuXoRoEgkz-9EwdCIS2dt5s1QC40RfHoWBcGm7_EDX6yrNBSm_Ja4oABJ_drA; _ga_SX8XLCG27H=GS1.1.1714661337.3.0.1714661337.0.0.0; _ga=GA1.2.858478662.1714637900; _cc_id=6780a9ec248bff4d42e42e72f11b115a; panoramaId_expiry=1714724301061; _gid=GA1.2.1981828823.1714637905; pubconsent-v2=YAAAAAAAAAAA; euconsent-v2=CP9_GsAP9_GsAAZACBENAyEsAP_gAH_gAAAAKJNV_H__bW1r8X73aft0eY1P9_j77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIEu3bBIQNlHJDUTVCgaogVryDMakWcgTNKJ6BkiFMRO2dYCF5vmwtj-QKY5vr993dx2D-t_dv83dzyz4VHn3a5_2e0WJCdA58tDfv9bROb-9IPd_58v4v0_F_rE2_eT1l_tevp7D8-ct87_XW-9_fff79Ll98FEgCzDQqIA6wJCQg0DCKBACoKwgIoEAAAAJA0QEAJgwKdgYBLrCRACAFAAMEAIAAUZAAgAAAgAQiACAAoEAAEAgUAAIAAAgEABAwAAgAsBAIAAQHQIUwIIFAsAEjMiIUwIQoEggJbKhBIAgQVwhCLPAAgERMFAAAAAAVgACAsFgcSSAlQkECXEG0AABAAgEEIFQgk5MAAQJGy1B4Im0ZWkAaGnCAA.YAAAAAAAAAAA' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"operationName":"TopRankedCorporates","variables":{},"query":"query TopRankedCorporates {\n  topRankedCorporates {\n    id\n    name\n    logo_url\n    industry\n    hq_city\n    startup_partners {\n      company_name\n      logo_url: logo\n      __typename\n    }\n    startup_friendly_badge\n    __typename\n  }\n}\n"}'

"""

gql_url = "https://ranking.glassdollar.com/graphql"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",  # , br",
    "Referer": "https://ranking.glassdollar.com/",
    "content-type": "application/json",
    "Origin": "https://ranking.glassdollar.com",
    "Connection": "keep-alive",
    # "Cookie": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}


def get_graph():
    """
    Query __schema to list all types defined in the schema and get details about each

    result: {"__schema": {"types": [{"name": "Query", "kind": "OBJECT", "description": null, "fields": [{"name": "corporates"}, {"name": "corporate"}, {"name": "topRankedCorporates"}, {"name": "getCorporateCities"}, {"name": "getCorporateIndustries"}, {"name": "getCorporateCount"}, {"name": "searchBar"}]}, {"name": "CorporatesType", "kind": "OBJECT", "description": null, "fields": [{"name": "rows"}, {"name": "count"}]}, {"name": "CorporateRowType", "kind": "OBJECT", "description": null, "fields": [{"name": "id"}, {"name": "name"}, {"name": "description"}, {"name": "logo_url"}, {"name": "website_url"}, {"name": "linkedin_url"}, {"name": "twitter_url"}, {"name": "industry"}, {"name": "hq_city"}, {"name": "hq_country"}, {"name": "startup_friendly_badge"}, {"name": "startup_partners_count"}]}, {"name": "ID", "kind": "SCALAR", "description": "The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `\"4\"`) or integer (such as `4`) input value will be accepted as an ID.", "fields": null}, {"name": "String", "kind": "SCALAR", "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.", "fields": null}, {"name": "Int", "kind": "SCALAR", "description": "The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.", "fields": null}, {"name": "Float", "kind": "SCALAR", "description": "The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).", "fields": null}, {"name": "CorporateFilters", "kind": "INPUT_OBJECT", "description": null, "fields": null}, {"name": "CorporateDetailsType", "kind": "OBJECT", "description": null, "fields": [{"name": "id"}, {"name": "name"}, {"name": "description"}, {"name": "logo_url"}, {"name": "website_url"}, {"name": "linkedin_url"}, {"name": "twitter_url"}, {"name": "industry"}, {"name": "hq_city"}, {"name": "hq_country"}, {"name": "startup_friendly_badge"}, {"name": "startup_partners_count"}, {"name": "startup_partners"}, {"name": "startup_themes"}]}, {"name": "Company", "kind": "OBJECT", "description": null, "fields": [{"name": "master_startup_id"}, {"name": "company_name"}, {"name": "website"}, {"name": "city"}, {"name": "country"}, {"name": "logo"}, {"name": "insert_time"}, {"name": "update_time"}, {"name": "theme_gd"}, {"name": "is_hidden"}, {"name": "is_startup"}, {"name": "is_dead"}, {"name": "is_no_startup_why"}, {"name": "corporate_partners"}]}, {"name": "DateTime", "kind": "SCALAR", "description": "The javascript `Date` as string. Type represents date and time as the ISO Date string.", "fields": null}, {"name": "Boolean", "kind": "SCALAR", "description": "The `Boolean` scalar type represents `true` or `false`.", "fields": null}, {"name": "CorporateBaseType", "kind": "OBJECT", "description": null, "fields": [{"name": "id"}, {"name": "name"}, {"name": "description"}, {"name": "logo_url"}, {"name": "website_url"}, {"name": "linkedin_url"}, {"name": "twitter_url"}, {"name": "industry"}, {"name": "hq_city"}, {"name": "hq_country"}, {"name": "startup_friendly_badge"}]}, {"name": "CorporateTopRankedType", "kind": "OBJECT", "description": null, "fields": [{"name": "id"}, {"name": "name"}, {"name": "description"}, {"name": "logo_url"}, {"name": "website_url"}, {"name": "linkedin_url"}, {"name": "twitter_url"}, {"name": "industry"}, {"name": "hq_city"}, {"name": "hq_country"}, {"name": "startup_friendly_badge"}, {"name": "startup_partners_count"}, {"name": "startup_partners"}]}, {"name": "JSONObject", "kind": "SCALAR", "description": "The `JSONObject` scalar type represents JSON objects as specified by [ECMA-404](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf).", "fields": null}, {"name": "searchBarWhere", "kind": "INPUT_OBJECT", "description": null, "fields": null}, {"name": "Mutation", "kind": "OBJECT", "description": null, "fields": [{"name": "toplistSubscribe"}]}, {"name": "ToplistSubscribeStatus", "kind": "OBJECT", "description": null, "fields": [{"name": "ok"}]}, {"name": "__Schema", "kind": "OBJECT", "description": "A GraphQL Schema defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, as well as the entry points for query, mutation, and subscription operations.", "fields": [{"name": "description"}, {"name": "types"}, {"name": "queryType"}, {"name": "mutationType"}, {"name": "subscriptionType"}, {"name": "directives"}]}, {"name": "__Type", "kind": "OBJECT", "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByUrl`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.", "fields": [{"name": "kind"}, {"name": "name"}, {"name": "description"}, {"name": "specifiedByUrl"}, {"name": "fields"}, {"name": "interfaces"}, {"name": "possibleTypes"}, {"name": "enumValues"}, {"name": "inputFields"}, {"name": "ofType"}]}, {"name": "__TypeKind", "kind": "ENUM", "description": "An enum describing what kind of type a given `__Type` is.", "fields": null}, {"name": "__Field", "kind": "OBJECT", "description": "Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type.", "fields": [{"name": "name"}, {"name": "description"}, {"name": "args"}, {"name": "type"}, {"name": "isDeprecated"}, {"name": "deprecationReason"}]}, {"name": "__InputValue", "kind": "OBJECT", "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.", "fields": [{"name": "name"}, {"name": "description"}, {"name": "type"}, {"name": "defaultValue"}, {"name": "isDeprecated"}, {"name": "deprecationReason"}]}, {"name": "__EnumValue", "kind": "OBJECT", "description": "One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string.", "fields": [{"name": "name"}, {"name": "description"}, {"name": "isDeprecated"}, {"name": "deprecationReason"}]}, {"name": "__Directive", "kind": "OBJECT", "description": "A Directive provides a way to describe alternate runtime execution and type validation behavior in a GraphQL document.\n\nIn some cases, you need to provide options to alter GraphQL's execution behavior in ways field arguments will not suffice, such as conditionally including or skipping a field. Directives provide this by describing additional information to the executor.", "fields": [{"name": "name"}, {"name": "description"}, {"name": "isRepeatable"}, {"name": "locations"}, {"name": "args"}]}, {"name": "__DirectiveLocation", "kind": "ENUM", "description": "A Directive can be adjacent to many parts of the GraphQL language, a __DirectiveLocation describes one such possible adjacencies.", "fields": null}]}}
    """
    data = {
        "variables": {},
        "query": """
        query {
  __schema {
    types {
      name
      kind
      description
      fields {
        name
      }
    }
  }
}        
        """
    }
    response = requests.post(gql_url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()['data']
        return data
    else:
        raise Exception('request failed', response)


def get_top_ranked_companies() -> List[Corporate]:
    data = {
        "operationName": "TopRankedCorporates",
        "variables": {},
        "query": """
        query TopRankedCorporates {
          topRankedCorporates {
            id
            name
            description
            logo_url
            industry
            hq_city
            hq_country
            website_url
            linkedin_url
            twitter_url
            startup_partners_count
            startup_partners {
              company_name
              logo_url: logo
              city
              website
              country
              theme_gd
              __typename
            }
            startup_friendly_badge
            __typename
          }
        }
        """
    }
    response = requests.post(gql_url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()['data']['topRankedCorporates']
        return [Corporate(**item) for item in data]
    else:
        raise Exception('request failed', response)


def get_company_ids(page: int) -> Dict[str, str | int]:
    assert page > 0, 'page should be greater than 0'
    data = {
        "variables": {
            "page": page,
            "sortBy": "asc",
            "filters": {
                "industry": [],
                "hq_city": []
            }
        },
        "query": """
           query ExampleQuery($page: Int, $sortBy: String, $filters: CorporateFilters) {
  corporates(page: $page, sortBy: $sortBy, filters: $filters) {
    count
    rows {
      id
    }
  }
}
           """
    }
    response = requests.post(gql_url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()['data']
        max_count = data['corporates']['count']
        ids = list(map(lambda row: row['id'], data['corporates']['rows']))
        return {
            'count': max_count,
            'ids': ids
        }
    else:
        raise Exception('request failed', response)


def get_company_by_id(id: str) -> Corporate:
    data = {
        "variables": {
            "corporateId": id
        },
        "query": """
          query Query($corporateId: String) {
  corporate(id: $corporateId) {
    description
    hq_city
    hq_country
    id
    industry
    linkedin_url
    logo_url
    name
    startup_friendly_badge
    startup_partners_count
    twitter_url
    website_url
    startup_partners {
      city
      company_name
      country
      logo_url: logo
      master_startup_id
      theme_gd
      website
    }
  }
}
           """
    }

    response = requests.post(gql_url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()['data']
        return Corporate(**data['corporate'])
    else:
        raise Exception('request failed', response)


if __name__ == '__main__':
    query_schema_result = get_graph()
    with open('query_schema_result.json', 'w', encoding='utf-8') as f:
        json.dump(query_schema_result,
                  f,
                  ensure_ascii=False,
                  indent=4)

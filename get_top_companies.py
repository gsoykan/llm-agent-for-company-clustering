import json

from pydantic.json import pydantic_encoder

from glassdollar_repo import get_top_ranked_companies


def main():
    top_companies = get_top_ranked_companies()
    with open('top_companies.json', 'w', encoding='utf-8') as f:
        json.dump(top_companies,
                  f,
                  ensure_ascii=False,
                  indent=4,
                  default=pydantic_encoder)


if __name__ == '__main__':
    main()

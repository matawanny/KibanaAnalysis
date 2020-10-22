from sys import argv
from src.parkingviolations.api import Service
from os import environ
from elasticsearch import Elasticsearch
from datetime import datetime

def create_and_update_index(index_name, doc_type):
    es = Elasticsearch()
    try:
        es.indices.create(index=index_name)
    except Exception:
        pass

    es.indices.put_mapping(
        index=index_name,
        doc_type=doc_type,
        body={
                doc_type: {
                    "properties": {
                        "amount_due": {
                        "type": "float"
                        },
                        "fine_amount": {
                        "type": "float"
                        },
                        "interest_amount": {
                        "type": "float"
                        },
                        "payment_amount": {
                        "type": "float"
                        },
                        "penalty_amount": {
                        "type": "float"
                        },
                        "reduction_amount": {
                        "type": "float"
                        },
                    }
                }
            }
        )
    return es

def insert_into_es(tickets, es):
    for ticket in tickets:
        ticket['issue_date'] = datetime.strptime(
            ticket['issue_date'],
            '%m/%d/%Y',
        )
        res = es.index(index='violation-parking-index', doc_type='vehicle', body=ticket, )
        print(res['result'])


if __name__ == "__main__":
    app_key = environ.get("APP_KEY")
    if not app_key:
        app_key = 'gugOZ4hl1StXpGcH5DKjtLZiB'

    es = create_and_update_index('violation-parking-index', 'vehicle')

    # print("APP_KEY={}".format(app_key))
    page_size = None
    num_pages = None

    if len(argv) == 3:
        page_size_str = argv[1]
        page_size = int(page_size_str.split('=')[1])
        num_pages = int(argv[2].split('=')[1])
    elif len(argv) == 2:
        page_size_str = argv[1]
        page_size = int(page_size_str.split('=')[1])
    else:
        raise Exception("Must provide parameter: --page_size=? ")

    # print(f"page_size={page_size}, num_pages={num_pages}")

    es = Elasticsearch()
    location = 'nc67-uf89'

    with Service(app_key) as service:
        if num_pages is None:
            tickets = service.get_info(location, page_size)
            insert_into_es(tickets, es)
        else:
            limit_size = int(page_size / num_pages)
            total_size = service.get_size(location)
            # print(f"total_size={total_size}")
            tickets = service.get_info(location, limit_size)
            insert_into_es(tickets, es)
            offset = 0
            for i in range(num_pages-1):
                offset += limit_size
                if offset >= total_size:
                    break;
                tickets = service.get_next_info(location, limit_size, offset)
                insert_into_es(tickets, es)

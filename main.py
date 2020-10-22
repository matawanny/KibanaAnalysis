from sys import argv
from src.parkingviolations.api import Service
from os import environ

if __name__ == "__main__":
    app_key = environ.get("APP_KEY")
    # print("APP_KEY={}".format(app_key))
    page_size = None
    num_pages = None
    output = None

    if len(argv) >= 4:
        page_size_str = argv[1]
        page_size = int(page_size_str.split('=')[1])
        num_pages_str = argv[2]
        num_pages = int(num_pages_str.split('=')[1])
        output_str = argv[3]
        output = output_str.split('=')[1]
    elif len(argv) == 3:
        page_size_str = argv[1]
        page_size = int(page_size_str.split('=')[1])
        if argv[2].split('=')[0] == '--num_pages':
            num_pages = int(argv[2].split('=')[1])
        else:
            output = argv[2].split('=')[1]
    elif len(argv) == 2:
        page_size_str = argv[1]
        page_size = int(page_size_str.split('=')[1])
    else:
        raise Exception("Must provide parameter: --page_size=? ")

    # print(f"page_size={page_size}, num_pages={num_pages}")

    location = 'nc67-uf89'

    if output is None:
        with Service(app_key) as service:
            if num_pages is None:
                print(service.get_info(location, page_size))
            else:
                limit_size = int(page_size / num_pages)
                total_size = service.get_size(location)
                # print(f"total_size={total_size}")
                print(service.get_info(location, limit_size))
                offset = 0
                for i in range(num_pages-1):
                    offset += limit_size
                    if offset >= total_size:
                        break;
                    print(service.get_next_info(location, limit_size, offset))
    else:
        with Service(app_key) as service, open(output, "w") as fw:
            if num_pages is None:
                fw.write(f"{service.get_info(location, page_size)}\n")
            else:
                limit_size = int(page_size / num_pages)
                total_size = service.get_size(location)
                fw.write(f"{service.get_info(location, limit_size)}\n")
                offset = 0
                for i in range(num_pages-1):
                    offset += limit_size
                    if offset >= total_size:
                        break;
                    fw.write(f"{service.get_next_info(location, limit_size, offset)}\n")
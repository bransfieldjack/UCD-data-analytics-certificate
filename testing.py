import requests, json


def main():

    headers = {
        "Content-type": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
    }

    data = {
        "method": "GET",
        "responseType": "blob",
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json;charset=UTF-8",
        },
        "data": {"dataset_id": "7241"},
    }

    r = requests.get("https://api.github.com/users/octocat/orgs", headers=headers)
    print(r)


if __name__ == "__main__":
    main()

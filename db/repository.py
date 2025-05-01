from db import connection

db = None          # DB 이름
collection = None  # Collection 이름

def set_collection(client):
    db = client["sample_db"]
    collection = db["sample_collection"]
    return collection

def find_content(requset_param):
    client = connection.connect()

    # 사용할 DB와 Collection 선택
    try:
        collection = set_collection(client)

        condition = {
            "date" : requset_param
        }

        result = collection.find_one(condition)
        return result
        
    except Exception as e:
        print(f"MongoDB find failed: {e}")


    connection.disconnect()

def save_content(data):
    client = connection.connect()

    # 사용할 DB와 Collection 선택
    try:
        collection = set_collection(client)

        # 저장
        result = collection.insert_one(data)

        # 결과 출력
        print("Inserted ID:", result.inserted_id)
        
    except Exception as e:
        print(f"MongoDB save failed: {e}")

    connection.disconnect()


def update_content(date, data):
    client = connection.connect()

    try:
        collection = set_collection(client)

        # update 실행 (date 기준으로 갱신)
        result = collection.update_one(
            {"date": date},      # 조건
            {"$set": data},      # 갱신 내용
            upsert=True          # 없으면 새로 삽입 (선택사항)
        )

        if result.matched_count:
            print("updated")
        elif result.upserted_id:
            print(f"not updated, saved (ID: {result.upserted_id})")
        else:
            print("not updated")

    except Exception as e:
        print(f"MongoDB update failed: {e}")

    connection.disconnect()
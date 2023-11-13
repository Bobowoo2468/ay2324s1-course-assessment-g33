from model.question_status import QuestionStatus
from mongodb import AsyncIOMotorClient
from config import get_config
from constant import QUESTION_STATUS

config = get_config

COLLECTION_NAME = "question_status"

async def get_question_status(client:AsyncIOMotorClient, userID: str):
    return client[COLLECTION_NAME].find_one({"userID": userID})

async def get_question_status_list(client:AsyncIOMotorClient, userID: str):
    statusList = []
    cursor = client[COLLECTION_NAME].find({"userID": userID})
    async for document in cursor:
        statusList.append(QuestionStatus(**document))
    return statusList

async def update_question_status(client: AsyncIOMotorClient, status: QuestionStatus):
    newStatus = QUESTION_STATUS.ATTEMPTED
    if status.description == "Completed":
        newStatus = QUESTION_STATUS.COMPLETED
    await client[COLLECTION_NAME].update_one({"userID": status.userID, 
                                              "titleSlug": status.titleSlug}, 
                                              {"$set": {"description": newStatus}})
    return True

async def add_question_status(client: AsyncIOMotorClient, status: QuestionStatus):
    await client[COLLECTION_NAME].insert_one(status)
    return True

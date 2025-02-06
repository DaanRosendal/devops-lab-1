import os
from pymongo import MongoClient, ReturnDocument

# Establish connection to MongoDB using the MONGO_URI from environment
# variables.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["student_db"]
students_coll = db["students"]


def get_next_sequence_value(sequence_name, db):
    """
    Generate an auto-incrementing student_id using a counters collection.
    """
    ret = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return ret["sequence_value"]


def add(student=None):
    # Check if a student with the same first name and last name already exists.
    existing_student = students_coll.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )
    if existing_student:
        return "already exists", 409

    # Generate a new sequential student_id.
    new_id = get_next_sequence_value("studentid", db)
    student_data = student.to_dict()
    student_data["student_id"] = new_id
    students_coll.insert_one(student_data)
    student.student_id = new_id
    return new_id


def get_by_id(student_id=None, subject=None):
    # Find a student using the integer student_id.
    student = students_coll.find_one({"student_id": int(student_id)})
    if not student:
        return "not found", 404
    # Remove the internal MongoDB '_id' field.
    if "_id" in student:
        del student["_id"]
    student["student_id"] = int(student["student_id"])
    print(student)
    return student


def delete(student_id=None):
    # Verify the student exists.
    student = students_coll.find_one({"student_id": int(student_id)})
    if not student:
        return "not found", 404
    students_coll.delete_one({"student_id": int(student_id)})
    return student_id

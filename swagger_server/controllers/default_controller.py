import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response404 import InlineResponse404  # noqa: E501
from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util
from swagger_server.service.student_service import add, get_by_id, delete


def add_student(body):  # noqa: E501
    """Add a new student

    Adds a student to the system # noqa: E501

    :param body: Student object to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())  # noqa: E501
        return add(body)
    return 500, "Internal Server Error"


def delete_student(student_id):  # noqa: E501
    """Deletes a student

    Deletes a single student based on the provided student_id.  # noqa: E501

    :param student_id: The unique student id
    :type student_id: float

    :rtype: InlineResponse200
    """
    return delete(student_id)


def get_student_by_id(student_id):  # noqa: E501
    """Gets a student

    Returns a single student # noqa: E501

    :param student_id: The unique student id
    :type student_id: float

    :rtype: Student
    """
    return get_by_id(student_id)

import re
from todoist_api_python.api import TodoistAPI
from modules.file_utils import text_file_to_string, save_object, load_object
from datetime import datetime, date

from modules.gui import GUI


# If set to True, the data will be loaded from the pickle files.
# If set to False, the data will be loaded from the Todoist API.
# This allows for faster testing.
LOAD_FROM_PICKLE = True

# The API key is stored in a text file to keep it secret from the git
# repository.
API_TEXT_FILE = "secrets/api_key.txt"
API_KEY = text_file_to_string(API_TEXT_FILE)

# Create an instance of the Todoist API.
api = TodoistAPI(API_KEY)


def format_task_name(task_name):

    # Remove the asterisk and space from the task name.
    if task_name.startswith("*"):
        task_name = task_name[2:]

    # Remove the markdown link from the task name.
    task_name = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"\1", task_name)

    return task_name


def get_data():
    if LOAD_FROM_PICKLE:
        all_tasks = load_object("secrets/tasks.pickle")
        all_labels = load_object("secrets/labels.pickle")
        all_projects = load_object("secrets/projects.pickle")

    else:
        all_tasks = api.get_tasks()
        all_labels = api.get_labels()
        all_projects = api.get_projects()

        save_object(all_tasks, "secrets/tasks.pickle")
        save_object(all_labels, "secrets/labels.pickle")
        save_object(all_projects, "secrets/projects.pickle")

    # Create a dictionary of project names.

    # This was the name of a project can be found by its ID.
    project_name_dict = {}

    for project in all_projects:
        project_name_dict[project.id] = project.name

    # Filter the tasks that have a deadline.
    task_with_deadlines = [task for task in all_tasks if task.due is not None]

    # Create a list to hold the tasks.
    list_of_tasks = []

    # Loop through the tasks with deadlines.
    for task in task_with_deadlines:

        # Create a dictionary to hold the task name and the number of days until
        # the deadline.
        tasks_element = {}

        due = task.due

        # Skip recurring tasks.
        if due.is_recurring:
            continue

        project_name = project_name_dict[task.project_id]

        # Skip any tasks in the Incubator project.
        if project_name == "Incubator":
            continue

        # Get the date of the deadline as a string.
        deadline_string = due.date

        # Convert the string to a date object.
        deadline_date = datetime.strptime(deadline_string, "%Y-%m-%d").date()

        # Get the number of days until the deadline as an integer.
        days_until_deadline = (deadline_date - date.today()).days

        # Format the task name.
        task_name = format_task_name(task.content)

        tasks_element["name"] = task_name
        tasks_element["days"] = days_until_deadline
        tasks_element["project"] = project_name

        list_of_tasks.append(tasks_element)

    list_of_tasks.sort(key=lambda x: x["days"])

    return list_of_tasks


gui = GUI(get_data)

gui.run()

from todoist_api_python.api import TodoistAPI
from modules.file_utils import text_file_to_string, save_object, load_object
from datetime import datetime, date


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

# print(str(all_tasks[0]).replace(",", "\n"))
# print()

# Filter the tasks that have a deadline.
task_with_deadlines = [task for task in all_tasks if task.due is not None]

# Create a dictionary with the task content as the key and the days until the
# deadline as the value.
tasks_and_days_remaining = {}

# Loop through the tasks with deadlines.
for task in task_with_deadlines:

    # Get the date of the deadline as a string.
    deadline_string = task.due.date

    # Convert the string to a date object.
    deadline_date = datetime.strptime(deadline_string, "%Y-%m-%d").date()

    # Get the number of days until the deadline as an integer.
    days_until_deadline = (deadline_date - date.today()).days

    # Add the task content and days until the deadline to the dictionary.
    tasks_and_days_remaining[task.content] = days_until_deadline

# Sort the dictionary by the number of days remaining.
tasks_and_days_remaining = dict(
    sorted(tasks_and_days_remaining.items(), key=lambda item: item[1])
)

# Print the tasks and days remaining.
for task, days in tasks_and_days_remaining.items():
    print(f"{task}: {days} days remaining")

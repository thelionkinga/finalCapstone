import os
from datetime import datetime

# Define the format string for date and time
DATETIME_STRING_FORMAT = "%d-%m-%Y"


def read_task_file():
    """
    Reads task details from a text file named 'tasks.txt' and returns a list of dictionaries.

    Each dictionary represents a task with attributes like username, title, description,
    due date, assigned date, and completion status.
    """
    with open("tasks.txt", "r", encoding="utf-8") as file:
        tasks = []
        for line in file:
            # Splitting the line into different attributes based on the comma separator
            line_split = line.strip().split(",")

            # Check if the line has the expected number of elements
            if len(line_split) == 6:
                user_dict = {
                    "username": line_split[0],
                    "title": line_split[1],
                    "description": line_split[2],
                    "due_date": datetime.strptime(line_split[3], "%d-%m-%Y"),
                    "assigned_date": datetime.strptime(line_split[4], "%d-%m-%Y"),
                    "completed": line_split[5] == "Yes"
                }
                tasks.append(user_dict)
            else:
                # Print a warning and skip the line if the format is unexpected
                print(f"Warning: Skipping line due to unexpected format: {line}")

        return tasks


def reg_user():
    """
    Registers a new user by prompting for a new username and password.
    This function also checks if the username already exists, prompts for a new password,
    and adds the new user to the 'user.txt' file if the password is confirmed.
    """
    print("_" * 80)
    print("\n\t\t\033[4mREGISTER A NEW USER\033[0m")
    print()
    while True:
        # Prompt for new username
        new_username = input("\nNew Username:\t\t ")

        # Check if the username already exist
        if not new_username or new_username in username_password:
            print("\nSorry, username already in use. Please enter a unique username ")
        else:
            break

    while True:
        # Prompt for a new password
        new_password = input("\nNew Password:\t\t ")

        # Check if the password is empty
        if not new_password:
            print("Invalid password. Please enter a non-empty password.")
        else:
            confirm_password = input("Confirm Password:\t ")

            # Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # Add the new user to the user.txt file (overwriting existing contents)
                print(f"\n\033[1m{new_username}\033[0m has been added as a new user.")
                print("_" * 80)
                username_password[new_username] = new_password

                with open("user.txt", "w", encoding="utf-8") as out_file:
                    # Prepare data for writing to the user.txt file
                    user_data_list = [f"{key};{value}" for key, value in username_password.items()]
                    out_file.write("\n".join(user_data_list))
                break
            else:
                print("\nPasswords do no match.")


def add_task():
    """
    The `add_task` function prompts the user to input details of a task, validates the input,
    and adds the task to a list and a text file.

    Input:
    - User assigned to the task
    - Title of the task
    - Description of the task
    - Due date of the task (in DD-MM-YYYY format)

    Output:
    - Updates the task_list and tasks.txt file with the new task information.

    Raises:
    - ValueError: If the due date input is not in the specified DD-MM-YYYY format.
    """

    print("_" * 80)
    print("\n\t\t\033[4mADD A TASK\033[0m")
    print()

    # Get the username for the task
    while True:
        task_username = input("\nUser assigned to task:\t\t ")
        if task_username in username_password:
            break
        print("\nUser does not exist. Please enter a valid username")

    # Get the title for the task
    while True:
        task_title = input("Title of Task:\t\t\t ")
        if not task_title:
            print("\nPlease enter a title for the task.\n")
            continue
        else:
            break

    # Get the description for the task
    while True:
        task_description = input("Description of Task:\t\t ")
        if not task_description:
            print("\nPlease enter a description.\n")
            continue
        else:
            break

    # Get the due date for the task with proper validation
    while True:
        try:
            task_due_date = input("Due date of task (DD-MM-YYYY):\t ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current date and time
    curr_date = datetime.now()

    # Create a new task dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Append the new task to the task_list
    task_list.append(new_task)

    # Update the tasks.txt file with the new task information
    with open("tasks.txt", "a", encoding="utf-8") as task_file:
        task_file.write(
            f"{new_task['username']}, {new_task['title']}, {new_task['description']}, "
            f"{new_task['due_date'].strftime(DATETIME_STRING_FORMAT)}, "
            f"{new_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}, "
            f"{'Yes' if new_task['completed'] else 'No'}\n"
        )

    print("\nTask has been successfully added.")
    print("_" * 80)


def view_all_tasks():
    """
    Displays all tasks stored in the tasks.txt file.
    """
    print("_" * 80)
    print("\n\t\t\033[4mVIEW ALL TASKS\033[0m")
    print()

    tasks = read_task_file()

    if not tasks:
        print("No tasks found.")
    else:
        for index, task in enumerate(tasks, start=1):
            print(f"Task ID: {index}")
            print(f"Assigned to: {task['username']}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
            print("-" * 40)

    print("_" * 80)


def main():
    """
    The main function for the Task Manager program.
    """
    # Read existing user credentials
    global username_password
    username_password = {}

    with open("user.txt", "r", encoding="utf-8") as user_file:
        for line in user_file:
            user, password = line.strip().split(";")
            username_password[user] = password

    # Initialize task list
    global task_list
    task_list = []

    while True:
        print("_" * 80)
        print("\n\t\t\t\033[4mTASK MANAGER\033[0m")
        print("\n\t1. Register User\n\t2. Add Task\n\t3. View All Tasks\n\t4. Exit")

        choice = input("\nEnter your choice (1-4):\t")

        if choice == "1":
            reg_user()
        elif choice == "2":
            add_task()
        elif choice == "3":
            view_all_tasks()
        elif choice == "4":
            print("\nExiting Task Manager. Have a great day!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()


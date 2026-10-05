import text_to_speech
import datetime
import webbrowser
import weather
import ai
import urllib.parse
import subprocess
import shutil
import json
import os


# =========================================================
# FILE PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEMORY_FILE = os.path.join(
    BASE_DIR,
    "memory.json"
)

CONVERSATION_FILE = os.path.join(
    BASE_DIR,
    "conversation.json"
)

TASKS_FILE = os.path.join(
    BASE_DIR,
    "tasks.json"
)


# =========================================================
# MEMORY FUNCTIONS
# =========================================================

def load_memory():

    default_memory = {
        "name": "",
        "college": "",
        "skills": [],
        "projects": [],
        "goals": [],
        "other": []
    }

    try:

        if not os.path.exists(MEMORY_FILE):

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    default_memory,
                    file,
                    indent=4
                )

            return default_memory

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory = json.load(file)

        if not isinstance(memory, dict):
            memory = default_memory

        for key, value in default_memory.items():

            if key not in memory:
                memory[key] = value

        return memory

    except Exception as e:

        print("Memory load error:", e)

        return default_memory


def save_memory(memory):

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("Memory saved successfully!")
        print("Memory file:", MEMORY_FILE)

    except Exception as e:

        print("Memory save error:", e)


# =========================================================
# CONVERSATION FUNCTIONS
# =========================================================

def load_conversation():

    try:

        if not os.path.exists(CONVERSATION_FILE):

            with open(
                CONVERSATION_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

            return []

        with open(
            CONVERSATION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            conversation = json.load(file)

        if isinstance(conversation, list):
            return conversation

        return []

    except Exception as e:

        print("Conversation load error:", e)

        return []


def save_conversation(conversation):

    try:

        with open(
            CONVERSATION_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                conversation,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        print("Conversation save error:", e)


# =========================================================
# TASK FUNCTIONS
# =========================================================

def load_tasks():
    try:
        if not os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
            return []

        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        return tasks if isinstance(tasks, list) else []

    except Exception as e:
        print("Task load error:", e)
        return []


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print("Task save error:", e)


# =========================================================
# TEXT TO SPEECH
# =========================================================

def speak_and_return(message):

    text_to_speech.text_to_speech(message)

    return message


# =========================================================
# AI + CONVERSATION HELPER
# =========================================================

def ask_ai_with_context(user_val):

    # Load personal memory
    memory = load_memory()

    memory_context = json.dumps(
        memory,
        indent=2,
        ensure_ascii=False
    )


    # Load conversation
    conversation = load_conversation()


    # Get last 10 conversations
    conversation_context = ""

    for item in conversation[-10:]:

        if (
            isinstance(item, dict)
            and "user" in item
            and "jarvis" in item
        ):

            conversation_context += (
                f"User: {item['user']}\n"
                f"Jarvis: {item['jarvis']}\n"
            )


    # Combine memory + conversation
    full_context = (
        "PERSONAL MEMORY:\n"
        + memory_context
        + "\n\n"
        + "RECENT CONVERSATION:\n"
        + conversation_context
    )


    # Ask AI
    answer = ai.ask_ai(
        user_val,
        full_context
    )


    # Save conversation
    conversation.append({
        "user": user_val,
        "jarvis": answer
    })


    # Keep latest 50 conversations
    conversation = conversation[-50:]


    save_conversation(
        conversation
    )


    # Speak answer
    text_to_speech.text_to_speech(
        answer
    )


    return answer


# =========================================================
# MAIN ACTION FUNCTION
# =========================================================

def Action(user_val):

    if not user_val:

        return speak_and_return(
            "Sorry sir, I could not understand that."
        )


    user_data = user_val.lower().strip()


    # =====================================================
    # GREETING
    # =====================================================

    if user_data in [
        "hello",
        "hi",
        "hey",
        "hye"
    ]:

        return speak_and_return(
            "Hello sir. How can I help you?"
        )


    # =====================================================
    # JARVIS NAME
    # =====================================================

    elif (
        "what is your name" in user_data
        or "who are you" in user_data
    ):

        return speak_and_return(
            "I am Jarvis, your AI assistant."
        )


    # =====================================================
    # GOOD MORNING
    # =====================================================

    elif "good morning" in user_data:

        return speak_and_return(
            "Good morning sir. Have a great day!"
        )


    # =====================================================
    # TIME
    # =====================================================

    elif user_data in [
        "time",
        "what is the time",
        "what time is it"
    ]:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return speak_and_return(
            f"Sir, the current time is {current_time}."
        )


    # =====================================================
    # DATE
    # =====================================================

    elif (
        "today's date" in user_data
        or "what is the date" in user_data
        or user_data == "date"
    ):

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        return speak_and_return(
            f"Today's date is {current_date}."
        )


    # =====================================================
    # OPEN GOOGLE
    # =====================================================

    elif "open google" in user_data:

        webbrowser.open(
            "https://www.google.com"
        )

        return speak_and_return(
            "Google is ready for you sir."
        )


    # =====================================================
    # OPEN YOUTUBE
    # =====================================================

    elif (
        "open youtube" in user_data
        or user_data == "youtube"
    ):

        webbrowser.open(
            "https://www.youtube.com"
        )

        return speak_and_return(
            "YouTube is ready for you sir."
        )


    # =====================================================
    # PLAY MUSIC
    # =====================================================

    elif "play music" in user_data:

        webbrowser.open(
            "https://gaana.com/"
        )

        return speak_and_return(
            "Music is ready for you sir."
        )


    # =====================================================
    # OPEN CHROME
    # =====================================================

    elif "open chrome" in user_data:

        try:

            chrome_paths = [

                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",

                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

            ]

            chrome_found = False

            for chrome_path in chrome_paths:

                if os.path.exists(chrome_path):

                    subprocess.Popen(
                        [chrome_path]
                    )

                    chrome_found = True

                    break


            if chrome_found:

                return speak_and_return(
                    "Chrome is opening sir."
                )

            else:

                webbrowser.open(
                    "https://www.google.com"
                )

                return speak_and_return(
                    "Chrome was not found, so I opened Google instead."
                )


        except Exception as e:

            print("Chrome error:", e)

            return speak_and_return(
                "I could not open Chrome sir."
            )


    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

    elif user_data.startswith("search "):

        search_query = user_data.replace(
            "search ",
            "",
            1
        ).strip()


        if not search_query:

            return speak_and_return(
                "What should I search for sir?"
            )


        encoded_query = urllib.parse.quote(
            search_query
        )


        webbrowser.open(
            f"https://www.google.com/search?q={encoded_query}"
        )


        return speak_and_return(
            f"Searching Google for {search_query}."
        )


    # =====================================================
    # WEATHER
    # =====================================================

    elif "weather" in user_data:

        try:

            ans = weather.weather()

            return speak_and_return(
                ans
            )

        except Exception as e:

            print("Weather error:", e)

            return speak_and_return(
                "Sorry sir, I could not get the weather."
            )


    # =====================================================
    # MOTIVATION
    # =====================================================

    elif (
        "motivate me" in user_data
        or "motivation" in user_data
    ):

        return speak_and_return(
            "Keep learning and keep building, sir. "
            "Small progress every day becomes a big achievement."
        )


    # =====================================================
    # OPEN NOTEPAD
    # =====================================================

    elif "open notepad" in user_data:

        os.system(
            "notepad.exe"
        )

        return speak_and_return(
            "Notepad is opening sir."
        )


    # =====================================================
    # OPEN CALCULATOR
    # =====================================================

    elif "open calculator" in user_data:

        os.system(
            "calc.exe"
        )

        return speak_and_return(
            "Calculator is opening sir."
        )


    # =====================================================
    # OPEN COMMAND PROMPT
    # =====================================================

    elif (
        "open command prompt" in user_data
        or "open cmd" in user_data
    ):

        subprocess.Popen(
            "cmd.exe"
        )

        return speak_and_return(
            "Command Prompt is opening sir."
        )


    # =====================================================
    # OPEN DOWNLOADS
    # =====================================================

    elif "open downloads" in user_data:

        downloads_path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )


        if os.path.exists(downloads_path):

            os.startfile(
                downloads_path
            )

            return speak_and_return(
                "Downloads folder is opening sir."
            )


        return speak_and_return(
            "I could not find the Downloads folder."
        )


    # =====================================================
    # OPEN DESKTOP
    # =====================================================

    elif "open desktop" in user_data:

        desktop_path = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )


        if os.path.exists(desktop_path):

            os.startfile(
                desktop_path
            )

            return speak_and_return(
                "Desktop is opening sir."
            )


        return speak_and_return(
            "I could not find the Desktop folder."
        )


    # =====================================================
    # GENERAL OPEN APPLICATION
    # =====================================================

    elif user_data.startswith("open "):

        app_name = user_data.replace(
            "open ",
            "",
            1
        ).strip()


        app_path = shutil.which(
            app_name
        )


        if app_path:

            os.startfile(
                app_path
            )

            return speak_and_return(
                f"{app_name} is opening sir."
            )


        return speak_and_return(
            f"Sorry sir, I could not find {app_name} on this computer."
        )


    # =====================================================
    # REMEMBER NAME
    # =====================================================

    elif user_data.startswith(
        "remember my name is "
    ):

        name = user_data.replace(
            "remember my name is ",
            "",
            1
        ).strip()


        memory = load_memory()

        memory["name"] = name

        save_memory(
            memory
        )


        return speak_and_return(
            f"Okay sir, I will remember your name is {name}."
        )


    # =====================================================
    # REMEMBER STUDY
    # =====================================================

    elif user_data.startswith(
        "remember i study "
    ):

        college = user_data.replace(
            "remember i study ",
            "",
            1
        ).strip()


        memory = load_memory()

        memory["college"] = college

        save_memory(
            memory
        )


        return speak_and_return(
            f"Okay sir, I will remember that you study {college}."
        )


    # =====================================================
    # REMEMBER SKILL
    # =====================================================

    elif user_data.startswith(
        "remember my skill is "
    ):

        skill = user_data.replace(
            "remember my skill is ",
            "",
            1
        ).strip()


        memory = load_memory()


        if skill not in memory["skills"]:

            memory["skills"].append(
                skill
            )


        save_memory(
            memory
        )


        return speak_and_return(
            f"Okay sir, I remembered that your skill is {skill}."
        )


    # =====================================================
    # REMEMBER PROJECT
    # =====================================================

    elif user_data.startswith(
        "remember my project is "
    ):

        project = user_data.replace(
            "remember my project is ",
            "",
            1
        ).strip()


        memory = load_memory()


        if project not in memory["projects"]:

            memory["projects"].append(
                project
            )


        save_memory(
            memory
        )


        return speak_and_return(
            f"Okay sir, I remembered your project is {project}."
        )


    # =====================================================
    # REMEMBER GOAL
    # =====================================================

    elif user_data.startswith(
        "remember my goal is "
    ):

        goal = user_data.replace(
            "remember my goal is ",
            "",
            1
        ).strip()


        memory = load_memory()


        if goal not in memory["goals"]:

            memory["goals"].append(
                goal
            )


        save_memory(
            memory
        )


        return speak_and_return(
            f"Okay sir, I remembered your goal is {goal}."
        )


    # =====================================================
    # WHAT IS MY NAME
    # =====================================================

    elif "what is my name" in user_data:

        memory = load_memory()


        if memory.get("name"):

            return speak_and_return(
                f"Your name is {memory['name']}."
            )


        return speak_and_return(
            "You have not told me your name yet sir."
        )


    # =====================================================
    # WHAT DO YOU REMEMBER
    # =====================================================

    elif "what do you remember about me" in user_data:

        memory = load_memory()


        answer = (
            "Here is what I remember about you, sir. "
        )


        if memory.get("name"):

            answer += (
                f"Your name is {memory['name']}. "
            )


        if memory.get("college"):

            answer += (
                f"You study {memory['college']}. "
            )


        if memory.get("skills"):

            answer += (
                "Your skills are "
                + ", ".join(memory["skills"])
                + ". "
            )


        if memory.get("projects"):

            answer += (
                "Your projects are "
                + ", ".join(memory["projects"])
                + ". "
            )


        if memory.get("goals"):

            answer += (
                "Your goals are "
                + ", ".join(memory["goals"])
                + "."
            )


        return speak_and_return(
            answer
        )


    # =====================================================
    # CLEAR MEMORY
    # =====================================================

    elif "clear memory" in user_data:

        save_memory({

            "name": "",

            "college": "",

            "skills": [],

            "projects": [],

            "goals": [],

            "other": []

        })


        return speak_and_return(
            "Okay sir, I cleared all my memory."
        )


    # =====================================================
    # =====================================================
    # TASK COMMANDS
    # =====================================================

    elif user_data.startswith("add task "):

        task = user_data.replace("add task ", "", 1).strip()

        if not task:
            return speak_and_return("What task should I add sir?")

        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)

        return speak_and_return(
            f"Okay sir, I added the task: {task}."
        )


    elif user_data in ["show my tasks", "show tasks", "my tasks"]:

        tasks = load_tasks()

        if not tasks:
            return speak_and_return(
                "You have no tasks right now sir."
            )

        answer = "Your tasks are: "

        for i, task in enumerate(tasks, 1):
            answer += f"Task {i}: {task}. "

        return speak_and_return(answer)


    elif user_data.startswith("remove task "):

        task = user_data.replace("remove task ", "", 1).strip()
        tasks = load_tasks()
        matching_index = None

        for i, existing_task in enumerate(tasks):
            if existing_task.lower() == task.lower():
                matching_index = i
                break

        if matching_index is None:
            return speak_and_return(
                "I could not find that task sir."
            )

        removed_task = tasks.pop(matching_index)
        save_tasks(tasks)

        return speak_and_return(
            f"Okay sir, I removed the task: {removed_task}."
        )


    elif user_data in ["clear all tasks", "clear tasks"]:

        save_tasks([])

        return speak_and_return(
            "Okay sir, I cleared all your tasks."
        )


    # STUDENT MODE
    # =====================================================

    elif "explain python" in user_data:

        student_prompt = (
            "Explain Python to a diploma Computer Science "
            "student in simple language with one easy example."
        )

        return ask_ai_with_context(
            student_prompt
        )


    elif "explain java" in user_data:

        student_prompt = (
            "Explain Java to a diploma Computer Science "
            "student in simple language with one easy example."
        )

        return ask_ai_with_context(
            student_prompt
        )


    elif "explain recursion" in user_data:

        student_prompt = (
            "Explain recursion in programming in very simple "
            "language with a Python example."
        )

        return ask_ai_with_context(
            student_prompt
        )


    elif "study plan" in user_data:

        student_prompt = (
            "Create a practical study plan for a diploma "
            "Computer Science student learning Python, Java, "
            "DSA and AI/ML."
        )

        return ask_ai_with_context(
            student_prompt
        )


    # =====================================================
    # AI FALLBACK
    # =====================================================

    else:

        return ask_ai_with_context(
            user_val
        )
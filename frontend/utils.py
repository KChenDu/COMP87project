from gradio import update


def disable_submit_button():
    return update(value='Generating...', interactive=False)


def submit(message, history):
    if message is None:
        return None, history
    message = message.strip()
    if message == "":
        return None, history
    return None, history + [(message, None)]


def enable_submit_button():
    return update(value='Submit', interactive=True)

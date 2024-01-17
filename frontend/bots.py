import time


def streaming_bot(history):
    if history[-1][0] is None or history[-1][0].strip() == "":
        yield history[:-1]
        return
    bot_message = "むかし、むかし、あるところに、おじいさんとおばあさんがありました。まいにち、おじいさんは山へしば刈りに、おばあさんは川へ洗濯に行きました。ある日、おばあさんが、川のそばで、せっせと洗濯をしていますと、川上から、大きな桃が一つ、\n&nbsp;「ドンブラコッコ、スッコッコ。\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ドンブラコッコ、スッコッコ。」\nと流れて来ました。"
    history[-1][-1] = ""
    for character in bot_message:
        history[-1][-1] += character
        time.sleep(0.01)
        yield history


import os
import math
import random
import numpy as np

from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    afx,
)

# ---------------- CONFIGURATION ----------------

W, H = 1280, 720
FPS = 24

# Six scenes, each 2 minutes = 12 minutes total
SCENE_DURATION = 120
TOTAL_DURATION = SCENE_DURATION * 6

OUTPUT = "little_star_bedtime.mp4"
NARRATION_FILE = "hindi_narration.mp3"

# Optional background music file.
# Place a soft lullaby MP3 in this folder and enter its name here.
MUSIC_FILE = "lullaby.mp3"

# Font: Windows Hindi font
FONT_PATH = r"C:\Windows\Fonts\Nirmala.ttf"

if not os.path.exists(FONT_PATH):
    FONT_PATH = r"C:\Windows\Fonts\NirmalaUI.ttf"

# ---------------- HINDI STORY NARRATION ----------------

story = [
    """
    एक सुंदर रात थी। आसमान गहरे नीले रंग का था।
    लाखों छोटे छोटे तारे चमक रहे थे।
    उनमें एक नन्हा तारा था, जिसका नाम टिमटिम था।

    टिमटिम बहुत प्यारा था। उसकी सुनहरी रोशनी
    पूरे आसमान में फैलती थी। लेकिन आज टिमटिम
    बहुत परेशान था। वह सोना चाहता था,
    मगर उसे नींद नहीं आ रही थी।

    वह कभी दाईं ओर घूमता, कभी बाईं ओर।
    कभी अपनी आँखें बंद करता और कभी उन्हें खोल देता।
    उसने चाँद से पूछा, चाँद मामा,
    मुझे नींद क्यों नहीं आ रही?

    चाँद ने प्यार से मुस्कुराकर कहा,
    प्यारे टिमटिम, कभी कभी मन में बहुत सारे
    विचार होते हैं। तुम थोड़ा आराम करो।
    """
    ,
    """
    तभी एक मुलायम सफेद बादल धीरे धीरे
    टिमटिम के पास आया। उसका नाम था पफी।

    पफी ने कहा, प्यारे दोस्त, क्या बात है?
    टिमटिम बोला, मैं सो नहीं पा रहा हूँ।

    पफी ने उसे प्यार से अपने पास बैठाया।
    उसने कहा, चलो एक छोटा सा अभ्यास करते हैं।
    अपनी आँखें धीरे से बंद करो।
    अब धीरे धीरे साँस अंदर लो।
    और फिर बहुत आराम से साँस बाहर छोड़ो।

    टिमटिम ने वैसा ही किया।
    उसने एक बार साँस ली, फिर दूसरी बार।
    धीरे धीरे उसकी चमक शांत होने लगी।

    पफी बोला, बहुत अच्छा।
    जब हम आराम से साँस लेते हैं,
    तो हमारा मन भी थोड़ा शांत हो जाता है।
    """
    ,
    """
    कुछ देर बाद एक प्यारा भूरा उल्लू आया।
    उसका नाम ओलिवर था।
    वह बड़े गोल चश्मे पहनता था
    और बहुत समझदार था।

    ओलिवर ने कहा, टिमटिम, क्या तुमने
    आज की कोई अच्छी बात याद की?

    टिमटिम सोचने लगा।
    उसे याद आया कि सुबह एक छोटे फूल ने
    सूरज की रोशनी में अपना चेहरा खोला था।
    उसे याद आया कि उसने एक छोटे तारे को
    रास्ता दिखाया था।
    उसे याद आया कि चाँद ने उसे मुस्कुराकर देखा था।

    टिमटिम के चेहरे पर प्यारी सी मुस्कान आ गई।
    ओलिवर बोला, अच्छी यादें मन को
    गर्म और शांत बना सकती हैं।
    """
    ,
    """
    नीचे धरती पर एक छोटी बच्ची रहती थी।
    उसका नाम लिली था।
    लिली ने गुलाबी रंग का पायजामा पहना था।
    वह अपने बिस्तर पर मुलायम कंबल ओढ़कर लेटी थी।

    उसकी खिड़की से चाँद की रोशनी आ रही थी।
    लिली ने अपनी आँखें बंद कीं।
    उसने अपने प्यारे खिलौने को गले लगाया
    और धीरे धीरे सो गई।

    टिमटिम ने लिली को देखा।
    वह बोला, देखो पफी, लिली कितनी शांति से सो रही है।

    पफी ने कहा, हर किसी को आराम की जरूरत होती है।
    रात हमें आराम करने और नए दिन के लिए
    तैयार होने का समय देती है।

    टिमटिम ने आसमान की ओर देखा।
    अब उसे थोड़ा अच्छा महसूस हो रहा था।
    """
    ,
    """
    फिर टिमटिम को अपनी छोटी छोटी चिंताएँ याद आईं।
    उसे लगा कि कल उसे बहुत सारे काम करने होंगे।

    ओलिवर ने कहा, प्यारे दोस्त,
    कल्पना करो कि तुम्हारी चिंताएँ छोटे छोटे
    चमकदार बुलबुले हैं।

    टिमटिम ने अपनी आँखें बंद कीं।
    उसने एक बुलबुला देखा।
    उसमें उसकी एक चिंता थी।
    बुलबुला धीरे धीरे ऊपर उड़ने लगा।

    फिर दूसरा बुलबुला आया।
    वह भी हवा में ऊपर उठ गया।
    सारे बुलबुले आसमान में तैरते हुए
    धीरे धीरे दूर चले गए।

    टिमटिम ने कहा, अब मेरा मन हल्का लग रहा है।
    पफी मुस्कुराया और बोला,
    बहुत अच्छा। अब आराम का समय है।
    """
    ,
    """
    अब रात और भी शांत हो गई थी।
    चाँद धीरे धीरे बादलों के पीछे से चमक रहा था।
    टिमटिम पफी के पास आराम से लेट गया।

    ओलिवर ने अपने पंख समेट लिए।
    सारे छोटे तारे धीरे धीरे चमकने लगे।
    टिमटिम ने एक लंबी, आरामदायक साँस ली।

    उसने अपनी आँखें बंद कर लीं।
    अब उसे नींद आ रही थी।
    वह एक सुंदर सपना देखने लगा।

    चाँद ने प्यार से कहा,
    शुभ रात्रि, प्यारे टिमटिम।

    और आसमान में सब कुछ शांत हो गया।

    शुभ रात्रि, प्यारे बच्चों।
    मीठे सपने देखो।
    """
]

# ---------------- DRAWING HELPERS ----------------

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def gradient_background():
    """Create a deep-blue night sky."""
    img = Image.new("RGB", (W, H))
    pixels = img.load()

    for y in range(H):
        t = y / H
        r = int(15 + 15 * t)
        g = int(20 + 20 * t)
        b = int(55 + 50 * t)

        for x in range(W):
            pixels[x, y] = (r, g, b)

    return img


def draw_star(draw, x, y, size, color):
    points = []

    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = size if i % 2 == 0 else size * 0.45

        points.append((
            x + math.cos(angle) * radius,
            y + math.sin(angle) * radius
        ))

    draw.polygon(points, fill=color)


def draw_character_star(draw, x, y, size=65):
    draw_star(draw, x, y, size, "#FFD75E")

    # Face
    draw.ellipse((x - 23, y - 8, x - 10, y + 7), fill="#46354C")
    draw.ellipse((x + 10, y - 8, x + 23, y + 7), fill="#46354C")

    draw.arc(
        (x - 18, y + 1, x + 18, y + 28),
        start=0,
        end=180,
        fill="#46354C",
        width=3
    )


def draw_cloud(draw, x, y, scale=1):
    color = "#F5F3FF"

    draw.ellipse(
        (x, y + 20 * scale,
         x + 110 * scale, y + 80 * scale),
        fill=color
    )

    draw.ellipse(
        (x + 15 * scale, y,
         x + 65 * scale, y + 65 * scale),
        fill=color
    )

    draw.ellipse(
        (x + 45 * scale, y - 15 * scale,
         x + 100 * scale, y + 65 * scale),
        fill=color
    )


def draw_owl(draw, x, y):
    draw.ellipse((x, y, x + 100, y + 120), fill="#9B6544")
    draw.ellipse((x + 10, y + 15, x + 50, y + 65), fill="#FFF4D5")
    draw.ellipse((x + 50, y + 15, x + 90, y + 65), fill="#FFF4D5")

    # Glasses
    draw.ellipse(
        (x + 12, y + 18, x + 48, y + 55),
        outline="#513D32", width=4
    )
    draw.ellipse(
        (x + 52, y + 18, x + 88, y + 55),
        outline="#513D32", width=4
    )

    draw.ellipse((x + 25, y + 30, x + 36, y + 43), fill="black")
    draw.ellipse((x + 63, y + 30, x + 74, y + 43), fill="black")

    draw.polygon(
        [(x + 45, y + 55), (x + 55, y + 55), (x + 50, y + 65)],
        fill="#FFCC66"
    )


def draw_moon(draw, x, y):
    draw.ellipse((x, y, x + 180, y + 180), fill="#FFE9A6")
    draw.ellipse((x + 55, y - 15, x + 205, y + 155), fill="#10183E")

    draw.ellipse((x + 30, y + 65, x + 45, y + 80), fill="#A9854B")
    draw.ellipse((x + 110, y + 65, x + 125, y + 80), fill="#A9854B")

    draw.arc(
        (x + 45, y + 70, x + 140, y + 125),
        start=0, end=180,
        fill="#A9854B", width=4
    )


def draw_lily(draw, x, y):
    # Bed
    draw.rounded_rectangle(
        (x - 70, y + 105, x + 250, y + 230),
        radius=25, fill="#DDAACB"
    )

    # Blanket
    draw.rounded_rectangle(
        (x + 15, y + 95, x + 240, y + 210),
        radius=25, fill="#F5BBD7"
    )

    # Head
    draw.ellipse((x - 10, y, x + 95, y + 105), fill="#F5C49B")

    # Hair
    draw.pieslice(
        (x - 15, y - 10, x + 105, y + 110),
        start=180, end=360, fill="#39252A"
    )

    # Closed eyes
    draw.arc((x + 15, y + 45, x + 40, y + 60),
             0, 180, fill="#39252A", width=3)
    draw.arc((x + 55, y + 45, x + 80, y + 60),
             0, 180, fill="#39252A", width=3)


# ---------------- CREATE SCENE IMAGES ----------------

def create_scene(scene_number):
    img = gradient_background()
    draw = ImageDraw.Draw(img)

    random.seed(scene_number + 10)

    # Background stars
    for _ in range(100):
        x = random.randint(0, W)
        y = random.randint(0, H - 150)
        radius = random.randint(1, 3)

        draw.ellipse(
            (x, y, x + radius, y + radius),
            fill="#E7E6FF"
        )

    draw_moon(draw, 980, 60)

    # Scene-specific illustration
    if scene_number == 0:
        draw_character_star(draw, 480, 350, 90)
        draw_cloud(draw, 700, 500, 1.3)

    elif scene_number == 1:
        draw_cloud(draw, 400, 370, 1.7)
        draw_character_star(draw, 550, 310, 75)

    elif scene_number == 2:
        draw_cloud(draw, 400, 390, 1.5)
        draw_character_star(draw, 550, 300, 75)
        draw_owl(draw, 750, 350)

    elif scene_number == 3:
        draw_lily(draw, 420, 380)
        draw_character_star(draw, 830, 270, 60)

    elif scene_number == 4:
        draw_cloud(draw, 380, 390, 1.6)
        draw_character_star(draw, 550, 310, 75)
        draw_owl(draw, 750, 370)

        # Worry bubbles
        for i in range(6):
            x = 350 + i * 110
            y = 170 - i * 15
            draw.ellipse(
                (x, y, x + 35, y + 35),
                outline="#C6D8FF", width=3
            )

    elif scene_number == 5:
        draw_cloud(draw, 420, 400, 1.7)
        draw_character_star(draw, 550, 320, 75)
        draw_owl(draw, 750, 390)

    return img


# ---------------- CREATE HINDI NARRATION ----------------

def create_narration():
    full_text = " ".join(story)

    tts = gTTS(
        text=full_text,
        lang="hi",
        slow=True
    )

    tts.save(NARRATION_FILE)
    print("Hindi narration created.")


# ---------------- ANIMATE SCENES ----------------

def create_animated_scene(scene_number):
    base_img = create_scene(scene_number)

    # Slight movement using a slow zoom
    clip = ImageClip(np.array(base_img)).with_duration(
        SCENE_DURATION
    )

    # Gentle fade in/out
    clip = clip.with_effects([
        afx.FadeIn(2),
        afx.FadeOut(2)
    ])

    return clip


# ---------------- ADD AUDIO ----------------

def add_audio(video):
    narration = AudioFileClip(NARRATION_FILE)

    # Fit video to total duration
    video = video.with_duration(TOTAL_DURATION)

    # Narration is slowed by gTTS but is not artificially stretched.
    # If narration is shorter, the remaining video is silent
    # unless background music is supplied.
    audio_layers = []

    narration = narration.with_start(0)
    audio_layers.append(narration)

    if os.path.exists(MUSIC_FILE):
        music = AudioFileClip(MUSIC_FILE)

        music = music.with_effects([
            afx.AudioLoop(duration=TOTAL_DURATION),
            afx.MultiplyVolume(0.12)
        ])

        audio_layers.append(music)

    from moviepy import CompositeAudioClip

    final_audio = CompositeAudioClip(audio_layers)

    return video.with_audio(final_audio)


# ---------------- MAIN VIDEO ----------------

def main():
    print("Creating Hindi narration...")
    create_narration()

    print("Creating animated scenes...")

    scenes = []

    for i in range(6):
        print(f"Rendering scene {i + 1}/6")
        scenes.append(create_animated_scene(i))

    video = concatenate_videoclips(
        scenes,
        method="compose"
    )

    # Ensure final video is 12 minutes
    video = video.with_duration(TOTAL_DURATION)

    # Add narration and optional music
    video = add_audio(video)

    print("Exporting MP4...")

    video.write_videofile(
        OUTPUT,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="5000k"
    )

    print(f"Video saved as: {OUTPUT}")


if __name__ == "__main__":
    main()

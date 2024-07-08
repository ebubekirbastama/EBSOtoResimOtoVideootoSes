from moviepy.editor import *
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os

# Soru ve resim dosya yollarını içeren metin dosyasının yolu
questions_file = "questions.txt"

# Çıkış dizini
output_dir = "output_videos"
os.makedirs(output_dir, exist_ok=True)

def create_image_with_text(text, output_path):
    # Beyaz arka plan oluşturma
    background = Image.new('RGB', (720, 1280), (255, 255, 255))
    draw = ImageDraw.Draw(background)
    
    # Yazı tipi ve boyutunu belirleme
    font = ImageFont.truetype("arial.ttf", 24)
    
    # Metni arka plana yazma
    text_position = (50, 100)  # Metnin başlangıç konumu
    draw.text(text_position, text, fill="black", font=font)
    
    # Görseli kaydetme
    background.save(output_path)

def create_audio_from_text(text, output_path):
    tts = gTTS(text=text, lang='tr', slow=False)
    tts.save(output_path)

def create_video(image_path, audio_path, output_path):
    # Görsel ve ses dosyalarını yükleme
    video_clip = ImageClip(image_path).set_duration(10)
    audio_clip = AudioFileClip(audio_path)
    
    # Ses klibini video klip ile birleştirme
    final_clip = video_clip.set_audio(audio_clip)
    
    # Video dosyasını kaydetme
    final_clip.write_videofile(output_path, fps=24)

# Metin dosyasını okuma ve soruları listeye ekleme
questions = []
with open(questions_file, "r", encoding="utf-8") as file:
    for line in file:
        question_text = line.strip()
        if question_text:
            questions.append(question_text)

# Tüm sorular için videoları oluşturma
for i, question_text in enumerate(questions):
    # Dosya yolları
    image_path = f"{output_dir}/question_image_{i+1}.jpg"
    audio_path = f"{output_dir}/question_audio_{i+1}.mp3"
    video_path = f"{output_dir}/question_video_{i+1}.mp4"
    
    # Adımları gerçekleştirme
    create_image_with_text(question_text, image_path)
    create_audio_from_text(question_text, audio_path)
    create_video(image_path, audio_path, video_path)
    
    print(f"{i+1}. video oluşturuldu: {video_path}")

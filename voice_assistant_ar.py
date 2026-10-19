# -*- coding: utf-8 -*-
"""المساعد الصوتي لذوي الاعاقة - فتح مواقع التواصل بالصوت."""
import webbrowser
import threading
import time

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    sr = None
    HAS_SR = False

try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    pyttsx3 = None
    HAS_TTS = False

try:
    import tkinter as tk
    from tkinter import scrolledtext
    HAS_TK = True
except ImportError:
    tk = None
    HAS_TK = False

SOCIAL_SITES = {
    "facebook": {
        "names_ar": "فيسبوك",
        "keywords": ["فيسبوك", "فيس", "فيس بوك", "facebook", "face"],
        "url": "https://www.facebook.com",
        "label": "فيسبوك  Facebook",
        "emoji": "FB",
    },
    "youtube": {
        "names_ar": "يوتيوب",
        "keywords": ["يوتيوب", "يوتوب", "youtube"],
        "url": "https://www.youtube.com",
        "label": "يوتيوب  YouTube",
        "emoji": "YT",
    },
    "twitter": {
        "names_ar": "تويتر اكس",
        "keywords": ["تويتر", "اكس", "twitter", "x"],
        "url": "https://x.com",
        "label": "تويتر (X)",
        "emoji": "X",
    },
    "instagram": {
        "names_ar": "انستغرام",
        "keywords": ["انستغرام", "انستا", "instagram", "insta"],
        "url": "https://www.instagram.com",
        "label": "انستغرام  Instagram",
        "emoji": "IG",
    },
    "tiktok": {
        "names_ar": "تيك توك",
        "keywords": ["تيك توك", "تك توك", "tiktok"],
        "url": "https://www.tiktok.com",
        "label": "تيك توك  TikTok",
        "emoji": "TT",
    },
    "whatsapp": {
        "names_ar": "واتساب",
        "keywords": ["واتساب", "واتس اب", "whatsapp", "واتس"],
        "url": "https://web.whatsapp.com",
        "label": "واتساب  WhatsApp",
        "emoji": "WA",
    },
    "telegram": {
        "names_ar": "تيليغرام",
        "keywords": ["تيليغرام", "تليغرام", "telegram"],
        "url": "https://web.telegram.org",
        "label": "تيليغرام  Telegram",
        "emoji": "TG",
    },
    "snapchat": {
        "names_ar": "سناب شات",
        "keywords": ["سناب", "snapchat"],
        "url": "https://web.snapchat.com",
        "label": "سناب شات  Snapchat",
        "emoji": "SC",
    },
    "linkedin": {
        "names_ar": "لينكدإن",
        "keywords": ["لينكد", "linkedin"],
        "url": "https://www.linkedin.com",
        "label": "لينكدإن  LinkedIn",
        "emoji": "IN",
    },
    "google": {
        "names_ar": "جوجل",
        "keywords": ["جوجل", "بحث", "google"],
        "url": "https://www.google.com",
        "label": "جوجل  Google",
        "emoji": "G",
    },
    "gmail": {
        "names_ar": "جيميل",
        "keywords": ["جيميل", "ايميل", "البريد", "gmail", "email"],
        "url": "https://mail.google.com",
        "label": "جيميل  Gmail",
        "emoji": "M",
    },
}

EXIT_WORDS = ["خروج", "اقفل", "توقف", "exit", "quit", "stop"]
HELP_WORDS = ["مساعدة", "مساعده", "تعليمات", "help", "اوامر"]


class Speaker:
    def __init__(self, log_func=None):
        self.log_func = log_func or print
        self.engine = None
        if HAS_TTS:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 150)
                self.engine.setProperty("volume", 1.0)
                try:
                    voices = self.engine.getProperty("voices")
                    for v in voices:
                        nm = (v.name or "").lower()
                        vi = (v.id or "").lower()
                        if "arab" in nm or "arab" in vi or "ar-" in vi:
                            self.engine.setProperty("voice", v.id)
                            break
                except Exception:
                    pass
            except Exception as e:
                self.log_func("تحذير: تعذر تشغيل النطق: %s" % e)
                self.engine = None

    def speak(self, text):
        self.log_func(">> " + text)
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.log_func("خطأ في النطق: %s" % e)


def find_site(command):
    cmd = command.strip().lower()
    for key, info in SOCIAL_SITES.items():
        for kw in info["keywords"]:
            if kw.lower() in cmd:
                return key, info
    return None, None


def is_exit_command(command):
    cmd = command.strip().lower()
    return any(w in cmd for w in EXIT_WORDS)


def is_help_command(command):
    cmd = command.strip().lower()
    return any(w in cmd for w in HELP_WORDS)


def open_site(key, info, speaker):
    try:
        webbrowser.open(info["url"])
        speaker.speak("تم فتح " + info["names_ar"])
        return True
    except Exception as e:
        speaker.speak("عذرا، تعذر فتح " + info["names_ar"])
        print("خطأ: %s" % e)
        return False


def handle_command(command, speaker):
    if not command or not command.strip():
        return True
    command = command.strip()
    print("الامر المستلم: " + command)
    if is_exit_command(command):
        speaker.speak("الى اللقاء! يتم اغلاق البرنامج.")
        return False
    if is_help_command(command):
        speaker.speak("قل: افتح فيسبوك، افتح يوتيوب، افتح تويتر، "
                      "افتح انستغرام، افتح تيك توك، افتح واتساب، "
                      "افتح تيليغرام. او قل خروج للاغلاق.")
        return True
    key, info = find_site(command)
    if info:
        open_site(key, info, speaker)
    else:
        speaker.speak("لم افهم الامر. قل مساعدة لسماع الاوامر.")
        print("جرب: افتح فيسبوك | افتح يوتيوب | مساعدة | خروج")
    return True


def listen_once(speaker, timeout=6, phrase_limit=6):
    if not HAS_SR:
        speaker.speak("مكتبة التعرف الصوتي غير مثبتة. استخدم الازرار او اكتب الامر.")
        return ""
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    try:
        with sr.Microphone() as source:
            print("تكلم الان...")
            r.adjust_for_ambient_noise(source, duration=0.6)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        print("جار فهم الكلام...")
        try:
            return r.recognize_google(audio, language="ar-SA")
        except Exception:
            return r.recognize_google(audio, language="en-US")
    except Exception as e:
        print("خطأ في الاستماع: %s (تأكد من المايكروفون والانترنت)" % e)
        speaker.speak("لم اسمعك جيدا، حاول مرة اخرى.")
        return ""


class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("المساعد الصوتي لذوي الاعاقة")
        self.root.geometry("540x700")
        self.root.configure(bg="#1a1a2e")
        self.speaker = Speaker(log_func=self.log)
        self.listening_continuous = False

        title = tk.Label(root, text="المساعد الصوتي\nلذوي الاعاقة",
                         font=("Arial", 22, "bold"),
                         bg="#1a1a2e", fg="#ffffff")
        title.pack(pady=12)
        sub = tk.Label(root, text="قل: افتح فيسبوك - او اضغط اي زر",
                       font=("Arial", 13), bg="#1a1a2e", fg="#aaaaff")
        sub.pack(pady=4)

        self.btn_listen = tk.Button(
            root, text="اضغط وتكلم", font=("Arial", 20, "bold"),
            bg="#00b894", fg="white", height=2, width=16,
            cursor="hand2", command=self.on_listen_once)
        self.btn_listen.pack(pady=10)

        fr = tk.Frame(root, bg="#1a1a2e")
        fr.pack(pady=4)
        tk.Button(fr, text="استماع مستمر", font=("Arial", 12, "bold"),
                  bg="#0984e3", fg="white", width=13, cursor="hand2",
                  command=self.start_continuous).pack(side="left", padx=6)
        tk.Button(fr, text="ايقاف", font=("Arial", 12, "bold"),
                  bg="#d63031", fg="white", width=9, cursor="hand2",
                  command=self.stop_continuous).pack(side="left", padx=6)

        st = []
        st.append("الصوت OK" if HAS_SR else "الصوت: ثبت SpeechRecognition")
        st.append("النطق OK" if HAS_TTS else "النطق: ثبت pyttsx3")
        tk.Label(root, text=" | ".join(st), font=("Arial", 10),
                 bg="#1a1a2e", fg="#888888").pack(pady=4)
        tk.Label(root, text="-- او اضغط الموقع مباشرة --",
                 font=("Arial", 12), bg="#1a1a2e",
                 fg="#dfe6e9").pack(pady=6)

        grid = tk.Frame(root, bg="#1a1a2e")
        grid.pack(pady=4)
        for i, (key, info) in enumerate(SOCIAL_SITES.items()):
            b = tk.Button(grid, text=info["label"],
                          font=("Arial", 13, "bold"),
                          bg="#2d3436", fg="white",
                          width=19, height=2, cursor="hand2",
                          command=lambda k=key: self.open_by_key(k))
            b.grid(row=i // 2, column=i % 2, padx=6, pady=5)

        tk.Label(root, text="او اكتب الامر هنا:",
                 font=("Arial", 12), bg="#1a1a2e",
                 fg="#dfe6e9").pack(pady=(10, 2))
        ef = tk.Frame(root, bg="#1a1a2e")
        ef.pack(pady=2)
        self.entry = tk.Entry(ef, font=("Arial", 14), width=22,
                              justify="center")
        self.entry.pack(side="left", padx=6)
        self.entry.bind("<Return>", lambda e: self.on_text_command())
        tk.Button(ef, text="تنفيذ", font=("Arial", 12, "bold"),
                  bg="#6c5ce7", fg="white", cursor="hand2",
                  command=self.on_text_command).pack(side="left")

        tk.Label(root, text="السجل:", font=("Arial", 11),
                 bg="#1a1a2e", fg="#dfe6e9").pack(pady=(8, 0))
        self.log_box = scrolledtext.ScrolledText(
            root, height=6, width=60, font=("Arial", 10),
            bg="#0f0f1e", fg="#00ffcc")
        self.log_box.pack(padx=12, pady=6, fill="both", expand=True)
        self.log("اهلا بك! اضغط (اضغط وتكلم) ثم قل: افتح فيسبوك")
        self.speaker.speak("اهلا بك! اضغط زر التكلم ثم قل اسم الموقع.")

    def log(self, msg):
        print(msg)
        try:
            self.log_box.insert(tk.END, msg + "\n")
            self.log_box.see(tk.END)
        except Exception:
            pass

    def open_by_key(self, key):
        info = SOCIAL_SITES[key]
        self.log("زر: " + info["label"])
        open_site(key, info, self.speaker)

    def on_text_command(self):
        cmd = self.entry.get().strip()
        if cmd:
            self.log("كتابة: " + cmd)
            handle_command(cmd, self.speaker)
            self.entry.delete(0, tk.END)

    def on_listen_once(self):
        def _work():
            self.btn_listen.config(state="disabled", text="استمع...")
            cmd = listen_once(self.speaker)
            if cmd:
                self.log("سمعت: " + cmd)
                handle_command(cmd, self.speaker)
            self.btn_listen.config(state="normal", text="اضغط وتكلم")
        threading.Thread(target=_work, daemon=True).start()

    def start_continuous(self):
        if self.listening_continuous:
            return
        self.listening_continuous = True
        self.log("بدأ الاستماع المستمر... قل (خروج) للايقاف")
        self.speaker.speak("الاستماع المستمر يعمل الان.")

        def _loop():
            while self.listening_continuous:
                cmd = listen_once(self.speaker)
                if cmd:
                    self.log("سمعت: " + cmd)
                    keep = handle_command(cmd, self.speaker)
                    if not keep:
                        self.listening_continuous = False
                        break
                time.sleep(0.4)
        threading.Thread(target=_loop, daemon=True).start()

    def stop_continuous(self):
        self.listening_continuous = False
        self.log("تم ايقاف الاستماع.")
        self.speaker.speak("تم الايقاف.")


def run_console_mode():
    speaker = Speaker()
    speaker.speak("وضع الاوامر النصية والصوتية. اكتب الامر او قل مساعدة.")
    print("=" * 55)
    print("  المساعد الصوتي - وضع سطر الاوامر")
    print("  اكتب اسم الموقع (افتح فيسبوك) او (صوت) للاستماع بالمايك")
    print("  الاوامر: مساعدة | خروج")
    print("=" * 55)
    while True:
        try:
            cmd = input("\nالامر (او 'صوت' للاستماع): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nالى اللقاء!")
            break
        if cmd in ("صوت", "مايك", "تكلم", "voice"):
            cmd = listen_once(speaker)
            if not cmd:
                continue
            print("سمعت: " + cmd)
        if not handle_command(cmd, speaker):
            break


def main():
    import argparse
    parser = argparse.ArgumentParser(description="المساعد الصوتي لذوي الاعاقة")
    parser.add_argument("--console", action="store_true",
                        help="تشغيل بدون واجهة رسومية")
    args = parser.parse_args()
    if args.console or not HAS_TK:
        if not HAS_TK:
            print("مكتبة tkinter غير متوفرة، سيعمل وضع سطر الاوامر.")
        run_console_mode()
    else:
        root = tk.Tk()
        VoiceAssistantGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()




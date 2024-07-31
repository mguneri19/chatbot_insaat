# Gerekli modülleri ve fonksiyonları içe aktar
from openai import OpenAI
import time
import os
from dotenv import load_dotenv

# .env dosyasındaki çevresel değişkenleri yükle
load_dotenv()

# OpenAI API anahtarını al ve my_key_openai değişkenine ata
my_key_openai = os.getenv("OPENAI_API_KEY")

# OpenAI istemcisini API anahtarı ile başlat
client = OpenAI(api_key=my_key_openai)

# Asistan kimliğini belirle
assistant_id = "YOUR ASSISSTANT ID"  # İnşaat A.Ş. Sohbet Botu ID

# Yeni bir iş parçacığı başlatma fonksiyonu
def start_new_thread():
    try:
        # Yeni iş parçacığı oluştur ve iş parçacığı kimliğini ata
        thread = client.beta.threads.create()
        thread_id = thread.id
        return thread_id
    except Exception as e:
        print(f"Error creating a new thread: {e}")
        return None

# Bir iş parçacığına mesaj ekleme fonksiyonu
def add_message_to_thread(thread_id, prompt):
    try:
        # Kullanıcı mesajını belirli iş parçacığına ekle
        message = client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=prompt,
                )
    except Exception as e:
        print(f"Error adding message to thread {thread_id}: {e}")

# Bir iş parçacığında çalıştırma döngüsünü başlatma fonksiyonu
def execute_run_cycle(thread_id):
    try:
        # Yeni bir çalışma döngüsü başlat ve çalıştırma kimliğini al
        run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

        # Çalıştırma tamamlanana kadar döngüde kal
        while True:
            # Çalıştırma durumunu kontrol et
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            # Çalıştırma tamamlandıysa döngüden çık
            if run.completed_at:
                # Geçen süreyi hesapla ve formatla
                elapsed = run.completed_at - run.created_at
                elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                print(f"Run completed in {elapsed}")
                print("-" * 100)
                break

            # Bir süre bekle ve tekrar kontrol et
            time.sleep(1)
        
        # İş parçacığındaki mesajları listele ve son mesajı al
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        last_message = messages.data[0]

        # Son mesajın içeriğini al
        AI_Response = last_message.content[0].text.value

        return AI_Response
    except Exception as e:
        print(f"Error executing run cycle for thread {thread_id}: {e}")
        return None

# Örnek kullanım
if __name__ == "__main__":
    thread_id = start_new_thread()
    if thread_id:
        add_message_to_thread(thread_id, "Merhaba, bugün hangi projeler üzerinde çalışıyoruz?")
        response = execute_run_cycle(thread_id)
        if response:
            print(f"AI Response: {response}")

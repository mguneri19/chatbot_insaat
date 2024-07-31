
import streamlit as st
import assistant_helper

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.thread_id = None

st.set_page_config(page_title="İnşaat A.Ş. Müşteri Temsilcisi", page_icon=":speech_balloon:")
st.image('./image/construction.jpg', use_column_width=True)
st.title("💬 İnşaat A.Ş. Sohbet Botu")
st.caption("🚀 İnşaat A.Ş. - Chatbot by Muhammet Güneri")
st.divider()


# session_state'deki tüm mesajları döngüyle geçir ve her biri için chat_message bloğu oluştur
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcının chat_input ile mesaj girmesini bekle ve mesajı "prompt" değişkenine ata
if prompt := st.chat_input("Mesajınızı yazınız"):

    # Kullanıcının mesajını "user" rolüyle chat_message bloğu içinde göster
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt oluşturulurken bir yüklenme çarkı göster
    with st.spinner("Yanıt oluşturuluyor..."):
        # Eğer thread_id daha önce başlatılmamışsa, yeni bir thread başlat ve thread_id'yi ata
        if st.session_state.thread_id is None:
            st.session_state.thread_id = assistant_helper.start_new_thread()
        
        # Kullanıcı mesajını thread'e ekle
        assistant_helper.add_message_to_thread(thread_id=st.session_state.thread_id, prompt=prompt)

        # Asistanın yanıtını çalıştır ve AI_Response değişkenine ata
        AI_Response = assistant_helper.execute_run_cycle(thread_id=st.session_state.thread_id)

        # Asistanın yanıtını "assistant" rolüyle chat_message bloğu içinde göster
        with st.chat_message("assistant"):
            st.markdown(AI_Response)
    
    # Kullanıcı mesajını ve asistanın yanıtını session_state'deki mesajlar listesine ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": AI_Response})

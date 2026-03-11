import streamlit as st
import random
import streamlit.components.v1 as components

# 0. 페이지 설정
st.set_page_config(page_title="오늘의 주인공은?", layout="wide")

# 1. 디자인 (CSS)
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    h1 { text-align: center; color: #ff4b4b; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 오늘의 주인공 뽑기")

# 화면 분할
col_results, col_setup = st.columns([1.5, 1])

with col_setup:
    st.subheader("📋 참여자 명단")
    name_input = st.text_area("이름 입력창", 
                             value="학생1\n학생2\n학생3\n학생4\n학생5\n학생6\n학생7", 
                             height=450)

with col_results:
    st.subheader("🎯 당첨자 발표")
    
    names = [n.strip() for n in name_input.split('\n') if n.strip()]
    
    if not names:
        st.warning("오른쪽 명단에 이름을 먼저 입력해 주세요!")
    else:
        winner = random.choice(names)
        names_json = str(names).replace("'", '"')

        # --- [마법의 HTML/JS 코드] ---
        # 소리 파일은 구글과 공신력 있는 서버의 효과음을 사용합니다.
        js_code = f"""
        <div id="container" style="text-align:center; font-family: sans-serif;">
            
            <button id="play-btn" style="
                width: 100%; height: 70px; font-size: 24px; font-weight: bold;
                background: linear-gradient(45deg, #ff4b4b, #ff7e5f);
                color: white; border: none; border-radius: 15px; cursor: pointer;
                box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3); margin-bottom: 25px;
            ">✨ 행운의 주인공 뽑기 시작! ✨</button>

            <div id="board" style="
                background: #ffffff; padding:60px 20px; border-radius:25px; 
                text-align:center; color:#333; border: 4px solid #eee;
                min-height: 200px; display: flex; flex-direction: column; 
                justify-content: center; transition: 0.3s;
            ">
                <h2 id="status" style="margin:0; color: #aaa;">준비 완료!</h2>
                <h1 id="name" style="font-size:75px; margin:20px 0; color: #ddd;">???</h1>
            </div>

            <audio id="shuffleSound" loop preload="auto">
                <source src="https://actions.google.com/sounds/v1/tools/clock_ticking.ogg" type="audio/ogg">
                <source src="https://www.soundjay.com/buttons/button-20.mp3" type="audio/mp3">
            </audio>
            <audio id="victorySound" preload="auto">
                <source src="https://www.myinstants.com/media/sounds/tada.mp3" type="audio/mp3">
            </audio>
        </div>

        <script>
            var names = {names_json};
            var winner = "{winner}";
            
            var btn = document.getElementById("play-btn");
            var board = document.getElementById("board");
            var nameBox = document.getElementById("name");
            var statusText = document.getElementById("status");
            
            var sfxShuffle = document.getElementById("shuffleSound");
            var sfxVictory = document.getElementById("victorySound");

            btn.onclick = function() {{
                // [필살기] 클릭하자마자 무조건 소리부터 재생!
                sfxShuffle.play().catch(function(error) {{
                    console.log("소리 재생 실패:", error);
                }});
                
                btn.disabled = true;
                btn.style.opacity = "0.5";
                btn.innerText = "두구두구두구...";

                statusText.innerText = "🎲 명단 섞는 중...";
                board.style.background = "#fff3f0";
                nameBox.style.color = "#ff4b4b";

                var count = 0;
                var timer = setInterval(function() {{
                    nameBox.innerText = names[Math.floor(Math.random() * names.length)];
                    count++;

                    if (count >= 25) {{
                        clearInterval(timer);
                        
                        // 셔플 소리 끄고 당첨 소리 재생
                        sfxShuffle.pause();
                        sfxShuffle.currentTime = 0;
                        sfxVictory.play();

                        // 결과 발표
                        nameBox.innerText = winner;
                        statusText.innerText = "🎊 오늘의 주인공! 🎊";
                        board.style.background = "linear-gradient(135deg, #ee0979 0%, #ff6a00 100%)";
                        nameBox.style.color = "white";
                        statusText.style.color = "white";
                        nameBox.style.fontSize = "95px";
                        
                        btn.disabled = false;
                        btn.style.opacity = "1";
                        btn.innerText = "✨ 다시 뽑기 ✨";
                    }}
                }}, 80);
            }};
        </script>
        """

        components.html(js_code, height=550)

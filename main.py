import streamlit as st
from utilities import generate_script

with st.sidebar:
    api_key = st.text_input("请输入Groq API密钥：",type="password")
    link_text = "获取Groq API密钥"
    link_url = "https://console.groq.com/keys"
    st.markdown(f'[{link_text}]({link_url})')

st.write("# 🎬影视Script生成器")
subject = st.text_input("请输入视频的主题：")
video_length = st.number_input("请输入视频的大致时长（单位：分钟）",min_value=1,max_value=10,step=1)
script_language = st.selectbox("请选择视频的脚本语言：",["中文","英文","日文"],index=0)
creativity = st.slider("请输入视频的创意程度（0.5-1.2）",min_value=0.5,max_value=1.2,value=1.0)
submit = st.button("生成脚本")

if submit and not api_key:
    st.info("请输入你的Groq API密钥")
    st.stop()
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length>1:
    st.info("视频长度不能小于1分钟")
    st.stop()
if submit:
    with st.spinner("正在生成脚本，请稍等..."):
        search_results, title, prompt = generate_script(subject, video_length, script_language, creativity, api_key)
    st.success("脚本生成成功！")
    st.write("### 视频标题")
    st.write(title)
    st.write("### 视频脚本")
    st.write(prompt)
    st.expander("### 搜索结果")
    st.write(search_results)
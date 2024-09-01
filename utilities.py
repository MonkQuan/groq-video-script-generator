from langchain_groq import chat_models
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper

def generate_script(subject, video_length, script_language, creativity, api_key):

    subject_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请根据 {subject} 构建一个引人入胜的视频标题"),
        ]
    )

    script_template = ChatPromptTemplate.from_messages(
        [
            ("human", """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。请使用{script_language}进行输出。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```"""),
        ]
    )

    model = chat_models.ChatGroq(
        model="llama3-8b-8192",
        api_key=api_key,
        temperature=creativity,
    )

    title_chain = subject_template | model
    script_chain = script_template | model

    title = title_chain.invoke(
        {"subject": subject}
    ).content

    wikipedia_search = WikipediaAPIWrapper(language="zh-cn")
    search_results = wikipedia_search.run(subject)

    script= script_chain.invoke(
        {
            "title": title,
            "duration": video_length,
            "script_language": script_language,
            "wikipedia_search": search_results
        }
    ).content

    return search_results, title, script
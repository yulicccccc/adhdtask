import streamlit as st

# 初始化页面配置
st.set_page_config(page_title="ADHD 极简行动台", page_icon="🎯", layout="centered")

# 初始化 session state 用于保存数据
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'brain_dump' not in st.session_state:
    st.session_state.brain_dump = []

# --- 界面划分 ---
st.title("🎯 ADHD 行动与闪念台")
st.markdown("---")

# 1. 脑洞倾倒区 (Brain Dump)
st.subheader("1. 🧠 大脑垃圾桶 (Brain Dump)")
st.caption("脑子乱的时候，把所有乱七八糟的想法直接扔在这里，先清空大脑！")

with st.form("dump_form", clear_on_submit=True):
    dump_text = st.text_area("你想 dump 些什么？", height=100)
    dump_submitted = st.form_submit_button("一键倾倒 🗑️")
    
    if dump_submitted and dump_text:
        ideas = [idea.strip() for idea in dump_text.split('\n') if idea.strip()]
        st.session_state.brain_dump.extend(ideas)
        st.success("✅ 大脑已清空！负荷减轻。")

if st.session_state.brain_dump:
    with st.expander("👀 查看我倾倒在垃圾桶里的想法"):
        for i, idea in enumerate(st.session_state.brain_dump):
            col1, col2 = st.columns([8, 1])
            col1.write(f"- {idea}")
            if col2.button("❌", key=f"del_{i}"):
                st.session_state.brain_dump.pop(i)
                st.rerun()

st.markdown("---")

# 2. 任务录入区 (需要执行时再来拆解)
st.subheader("2. 拆解原子任务")
with st.form("add_task_form", clear_on_submit=True):
    task_name = st.text_input("从垃圾桶里挑一件事，或者写个新任务：")
    atomic_step = st.text_input("第一步极小动作是什么？(2分钟内能做完的)")
    submitted = st.form_submit_button("加入执行队列")
    
    if submitted and task_name and atomic_step:
        st.session_state.tasks.append({
            "task": task_name,
            "step": atomic_step,
            "done": False
        })
        st.success("✅ 拆解完毕，进入单线程模式。")

st.markdown("---")

# 3. 专注执行区（核心：只显示一件事）
st.subheader("3. 你现在【唯一】需要做的事")

pending_tasks = [t for t in st.session_state.tasks if not t['done']]

if pending_tasks:
    current_task = pending_tasks[0]
    
    st.info(f"**终极目标：** {current_task['task']}")
    st.error(f"🚀 **立刻去执行：** {current_task['step']}")
    
    if st.button("🎉 我做完了！"):
        for t in st.session_state.tasks:
            if t['task'] == current_task['task'] and t['step'] == current_task['step']:
                t['done'] = True
        st.balloons()
        st.rerun()
else:
    st.success("☕ 目前没有待办任务。脑子乱了就往上翻，去倾倒垃圾桶！")
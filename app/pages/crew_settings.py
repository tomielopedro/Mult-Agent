import streamlit as st
from myagent.crew import MyAgent

my_agent = MyAgent().crew()

agents, tasks, crew = st.tabs(['Agents', 'Tasks', 'Crew'])

with agents:
    with st.container(height=600):
        agents = my_agent.agents
        for agent in agents:
            st.subheader(agent.role)
            st.write(agent)

with tasks:
    with st.container(height=600):
        tasks = my_agent.tasks
        for task in tasks:
            st.subheader(task.name)
            st.write(task)

with crew:
    with st.container(height=600):
        st.write(my_agent)

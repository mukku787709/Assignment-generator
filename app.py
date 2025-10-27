import streamlit as st
import openai
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Academic Assignment Generator", page_icon="🎓", layout="wide")

# Title and description
st.title("🎓 Academic Assignment Generator")
st.markdown("""
Welcome to the AI-powered Academic Assignment Generator! This tool helps students create professional, structured academic assignments in seconds.

**Features:**
- Generates well-organized, plagiarism-free assignments
- Includes Introduction, Main Discussion (with subheadings), and Conclusion
- Focuses on clarity, precision, and formal English
- Perfect for learning academic writing structure

*Note: This tool is designed for educational purposes to help students learn proper academic writing, not for cheating.*
""")

# Sidebar for API key input
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)
        st.success("API Key configured!")
    else:
        st.warning("Please enter your OpenAI API Key to proceed.")

# Main content
st.header("📝 Generate Your Assignment")

# Input form
with st.form("assignment_form"):
    topic = st.text_input("Enter the assignment topic:", placeholder="e.g., The Impact of Climate Change on Global Economy")
    word_count = st.slider("Approximate word count:", min_value=500, max_value=3000, value=1000, step=100)
    academic_level = st.selectbox("Academic level:", ["Undergraduate", "Graduate", "PhD"])
    subject_area = st.text_input("Subject area:", placeholder="e.g., Economics, History, Science")

    submitted = st.form_submit_button("Generate Assignment")

if submitted:
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    elif not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating your assignment... This may take a few moments."):
            try:
                # Construct the prompt
                prompt = f"""
Write a structured academic assignment on the topic: "{topic}"

Requirements:
- Academic level: {academic_level}
- Subject area: {subject_area}
- Approximate word count: {word_count}
- Structure: Introduction, Main Discussion (with subheadings and explanations), Conclusion
- Style: Formal English, plagiarism-free, research-oriented
- Focus: Clarity, precision, and professional academic tone

Please ensure the assignment is well-organized, includes relevant examples or evidence, and demonstrates critical thinking.
"""

                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert academic writer helping students create high-quality assignments."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.7
                )

                assignment = response.choices[0].message.content

                # Display the generated assignment
                st.success("Assignment generated successfully!")
                st.subheader("📄 Your Generated Assignment")
                st.markdown(assignment)

                # Download button
                st.download_button(
                    label="📥 Download Assignment",
                    data=assignment,
                    file_name=f"{topic.replace(' ', '_')}_assignment.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Developed by Muhammad Haseeb** - Made to support students in their assignments and research writing 🎯")

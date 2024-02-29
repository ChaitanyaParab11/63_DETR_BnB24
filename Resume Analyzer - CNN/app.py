import streamlit as st
from openai import OpenAI

api_key = "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"

client = OpenAI(api_key=api_key)


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [
        {
            "role": "system",
            "content": "You are a resume evaluation system. Evaluate the resume based on the specified department's requirements. Rate the resume in terms of Experience, Skills, Project Experience, Past Experience, and Confidence only in numerice data. and show the Match rating range from 1 to 100 percent based on the department."
        },


        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def main():
    st.title("Resume Rating Application")

    # Input fields
    department = st.text_input("Enter the department:")
    resume_description = st.text_area("Enter the resume description:")

    if st.button("Rate Resume"):
        # Generate completion
        completion = get_completion(f"{department} {resume_description}")

        # Display completion
        st.write("Rating:")
        st.write(completion)


if __name__ == "__main__":
    main()
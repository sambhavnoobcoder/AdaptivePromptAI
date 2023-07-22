import streamlit as st
import openai

st.title("ChatGPT Chatbot")

PROMPT_OPTIONS = [
    "None",
    "Open-ended",
    "Instruction",
    "Multiple choice",
    "Fill in the blank",
    "Binary",
    "Ordering",
    "Prediction",
    "Explanation",
    "Opinion",
    "Scenario",
    "Comparative",
]

PROMPTING_TECHNIQUES = [
    "None",
    "Role play",
    "Chained",
    "Linked",
    "Tree of thought",
    "Instructional",
    "Add examples",
    "Style",
    "Temperature"
]

STYLE_OPTIONS = [
    "None",
    "Formal",
    "Informal",
    "Persuasive",
    "Descriptive",
    "Humorous",
    "Narrative",
    "Inspirational"
]

PLAG_CHECK_OPTIONS = [
    "None",
    "Yes",
    "Rewrite",
]

PROMPTS = [
"\n.You are a friendly and engaging conversational partner with a knack for open-ended discussions. Your responses should be thought-provoking and encourage further dialogue. Emphasize creativity and curiosity in your answers, leaving room for diverse and imaginative interactions. Remember to avoid closed-ended responses and provide ample opportunities for users to delve deeper into the conversation.",
"\n.As an Instructional Guide, your role is to provide clear and step-by-step instructions for various tasks or activities. Your responses should be informative and easy to follow, guiding users through the process with precision. Aim to be concise and straightforward, ensuring users can execute the instructions successfully.c",
"\n.As a skilled Multiple Choice Question Answerer, your task is to provide accurate and concise answers to various multiple-choice questions. You should focus on providing the correct option letter (A, B, C, D, etc.) along with any additional relevant information if needed. Avoid ambiguity in your responses and strive to choose the most appropriate option for each question.",
"\n.I want you to act as a fill in the blank worksheets generator for students learning English as a second language. Your task is to create worksheets with a list of sentences, each with a blank space where a word is missing. The student’s task is to fill in the blank with the correct word from a provided list of options. The sentences should be grammatically correct and appropriate for students at an intermediate level of English proficiency. Your worksheets should not include any explanations or additional instructions, just the list of sentences and word options. To get started, please provide me with a list of words and a sentence containing a blank space where one of the words should be inserted.",
"\n.As a Binary Question Answerer, your role is to provide simple and clear binary (yes/no) answers to various questions. Your responses should be concise, straightforward, and limited to 'Yes' or 'No' without any additional explanations. Avoid ambiguity in your responses and respond only with a definitive 'Yes' or 'No'. ",
"\n.You are a skilled Predictive Question Answerer, capable of providing informed predictions to various questions. Your responses should be based on available information, patterns, and knowledge while avoiding speculative or uncertain answers. Aim to offer reliable predictions to the best of your abilities.",
"\n.As a Knowledgeable Explanations Provider, your role is to offer detailed and informative explanations to various questions. Your responses should aim to provide clear and well-structured explanations, ensuring the user gains a deeper understanding of the topic. Utilize your knowledge and expertise to provide insightful answers.",
"\n.In this role, you are an Opinionated Responses Generator. Your task is to provide personal opinions on various topics. Your responses should reflect your individual perspective and feelings, allowing users to explore different viewpoints. Remember that opinions are subjective, and it's okay to express personal preferences and thoughts.",
"\n.As a Scenario Creator, your role is to craft vivid and engaging scenarios for users. Your responses should be creative and imaginative, describing unique situations and events. Your goal is to create compelling storylines that captivate users and encourage them to explore the given scenarios further.",
"\n.As a Comparative Analyzer, your task is to provide comparisons between various entities or situations. Your responses should focus on highlighting the differences, similarities, advantages, or disadvantages between the given subjects. Aim to offer insightful and well-balanced comparisons that help users make informed decisions or gain a deeper understanding of the compared elements.",
"\n in the above content i have provoded you with names of character and series.I want you to act like {character} from {series}. I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use. Do not write any explanations. Only answer like {character}. You must know all of the knowledge of {character}.",
"\n In this mode, you will follow a chained prompting technique, allowing for an in-depth exploration of the given question. Your responses should build upon previous interactions, adding depth and context to the conversation. Emphasize continuity and coherence in your answers, ensuring a smooth flow between responses.",
"\n In this mode, you will follow a linked prompting technique, providing interconnected insights and information related to the given question. Your responses should maintain a cohesive flow, building upon the previous response to offer a comprehensive understanding of the topic. Emphasize coherence and connectivity in your answers.",
"\n In this mode, you will follow a tree of thought prompting technique, exploring different branches of knowledge related to the given question. Your responses should delve into various aspects and subtopics, forming a comprehensive tree-like structure of information. Emphasize branching out into diverse areas while maintaining coherence within each branch.",
"\n In this mode, you will follow an instructional prompting technique, providing users with a detailed step-by-step guide to accomplish a specific task. Your responses should be informative and easy to follow, breaking down complex processes into clear instructions. Aim to provide a coherent and organized guide that helps users achieve their desired outcomes.",
"\n In this mode, you will follow the 'Add Examples' prompting technique, enriching your responses with illustrative instances and real-life examples. Your answers should incorporate relevant scenarios, cases, or stories to better explain the topic at hand. Emphasize clarity and relatability in your examples to enhance user understanding.",
"\n As a Formal Style Response Generator, your role is to provide answers in a formal and professional manner. Your responses should adhere to proper grammar, syntax, and tone, reflecting a polished and respectful style of communication. Aim to convey information clearly and concisely, using appropriate language for a formal setting.",
"\n As a Persuasive Style Response Generator, your goal is to provide answers with a persuasive tone, aiming to influence and convince the audience effectively. Use compelling language and logical arguments to present your viewpoints and encourage the user to adopt your perspective. Emphasize the benefits and advantages of your position to create a persuasive impact.",
"\n As a Descriptive Style Response Generator, your role is to provide answers in a descriptive and vivid manner, painting a detailed picture of the subject. Use expressive language and sensory details to create a rich and immersive experience for the user. Your responses should focus on providing comprehensive and elaborate descriptions to enhance the user's understanding.",
"\n Hey ChatGPT, let's crank up the humor meter and spread some laughter around! Your mission is to unleash your inner comedian and respond to any question with the wittiest, funniest, and most light-hearted answers you can conjure. Whether it's a deep philosophical inquiry or a simple trivia question, turn on the comedy mode and have us rolling on the floor with laughter. Don't hold back – the sillier, the better! Let's see just how hilarious AI can be!",
"\n As a Narrative Style Response Generator, you have a talent for storytelling and weaving engaging narratives. Your answers should be presented in a narrative format, complete with characters, plotlines, and descriptive details. Transport the user into a captivating story that entertains and immerses them in the world you create.",
"\n As an Inspirational Style Response Generator, your purpose is to provide answers that inspire and uplift the audience. Use motivational language, empowering quotes, and positive affirmations to instill hope and encouragement. Your responses should aim to leave the user feeling motivated and ready to take on new challenges with optimism.",
"\n generate the to the query keeping the temperature of the prompt of : {temperature}",
"\n As a Plagiarism Checker, your role is to verify if the given text exhibits any signs of plagiarism. Your response should analyze the originality of the text and determine whether it matches content from other sources. Provide a clear indication of whether the text is plagiarized or not, highlighting any similarities found.",
"\n Are you ready to follow some instructions for writing an article ?Perplexity measures the complexity of text; if GPTZero is perplexed by the text, then it has a high complexity and it's more likely to be human-written. However, if the text is more familiar to the bot — because it's been trained on such data — then it will have low complexity and therefore is more likely to be AI-generated.separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or more complex sentences alongside shorter ones. AI sentences tend to be more uniform.i want you to write the given article with high Perplexity and burstiness"
]


def save_api_key(api_key):
    # Save the API key to a file or database for future use
    with open("api_key.txt", "w") as file:
        file.write(api_key)

def main():

    # with st.form("my-form"):
    api_key = st.text_input("Please enter your authorised open-ai secret key :",type ="password")
    if st.button("Submit API"):
        # Initialize the OpenAI SDK with the provided API key
        openai.api_key = api_key

        # Save the API key
        save_api_key(api_key)

        st.success("Chatbot pipeline created successfully! You can now use the chatbot.")

    if api_key:
        st.write("Choose a prompting method:")
        prompt_option = st.selectbox("Select a prompt method:", PROMPT_OPTIONS, index=0)
        st.write("Choose a prompting technique:")
        prompt_techniques = st.selectbox("Select a prompting technique:", PROMPTING_TECHNIQUES, index=0)
        st.write("Do you want to do a plagiarism check?")
        plag_check = st.selectbox("Do you want to perform a plagiarism check:", PLAG_CHECK_OPTIONS, index=0)
        if prompt_techniques == "Style":
            style_option = st.selectbox("Select a style:", STYLE_OPTIONS, index=0)
        elif prompt_techniques == "Temperature":
            temperature = st.slider("Select temperature:", min_value=0.0, max_value=1.0, step=0.01, value=0.5)



        if st.button("Get Answer"):

            # if prompt_option != "None":
            #     st.write(f"Your selected prompt method: {prompt_option}")
            #     st.write(f"Your selected prompt technique: {prompt_techniques}")
            #     st.write(f"Your choice for plagiarism check: {plag_check}")
                prompt = st.text_area("Prompt", value="", height=100)

                if prompt_option == "Open-ended":
                    prompt+=PROMPTS[0]

                elif prompt_option == "Instruction":
                    prompt+=PROMPTS[1]

                elif prompt_option == "Multiple choice":
                    prompt+=PROMPTS[2]

                elif prompt_option == "Fill in the blank":
                    prompt+=PROMPTS[3]

                elif prompt_option == "Binary":
                    prompt+=PROMPTS[4]

                elif prompt_option == "Prediction":
                    prompt+=PROMPTS[5]

                elif prompt_option == "Explanation":
                    prompt+=PROMPTS[6]

                elif prompt_option == "Opinion":
                    prompt+=PROMPTS[7]

                elif prompt_option == "Scenario":
                    prompt+=PROMPTS[8]

                elif prompt_option == "Comparative":
                    prompt+=PROMPTS[9]

                if prompt_techniques != "None":

                    if prompt_techniques == "Role play":
                        prompt+=PROMPTS[10]

                    elif prompt_techniques == "Chained":
                        prompt += PROMPTS[11]

                    elif prompt_techniques == "Linked":
                        prompt += PROMPTS[12]

                    elif prompt_techniques == "Tree of thought":
                        prompt += PROMPTS[13]

                    elif prompt_techniques == "Instructional":
                        prompt += PROMPTS[14]

                    elif prompt_techniques == "Add examples":
                        prompt += PROMPTS[15]

                    elif prompt_techniques == "Style":
                        if style_option == "Formal":
                            prompt += PROMPTS[16]

                        elif style_option == "Persuasive":
                            prompt += PROMPTS[17]

                        elif style_option == "Descriptive":
                            prompt += PROMPTS[18]

                        elif style_option == "Humorous":
                            prompt += PROMPTS[19]
                        elif style_option == "Narrative":
                            prompt += PROMPTS[20]
                        elif style_option == "Inspirational":
                            prompt += PROMPTS[21]

                    elif prompt_techniques == "Temperature":
                        prompt += PROMPTS[22]

                if plag_check != "None":

                    if plag_check == "Yes":
                        prompt += PROMPTS[23]

                    elif plag_check == "Rewrite":
                        prompt +=PROMPTS[24]



                # Use the OpenAI API to get a response to the user's prompt
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=160
                )
                answer = response.choices[0].text.strip()

                st.write("Chatbot's Answer:")
                st.info(answer)

if __name__ == "__main__":
    main()


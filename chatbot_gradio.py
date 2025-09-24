import gradio as gr
import pickle


with open("stream_selection_model.pkl", "rb") as f:
    model, feature_names = pickle.load(f)

subjects = ["Maths", "Science", "English", "Sinhala", "ICT", "History", "Commerce", "Buddhism"]
interest_options = ["Science", "Maths", "Commerce", "Arts", "Technology"]


def recommend_stream(*ratings_and_interest):
    ratings = ratings_and_interest[:-1]
    interest = ratings_and_interest[-1]

   
    input_dict = {f: 0 for f in feature_names}
    for i, sub in enumerate(subjects):
        input_dict[sub] = ratings[i] * 20
    interest_col = "Interest_" + interest
    if interest_col in input_dict:
        input_dict[interest_col] = 1
    input_data = [input_dict[f] for f in feature_names]

    
    prediction = model.predict([input_data])[0]
    return f"🎓 Based on your answers, we recommend: **{prediction} Stream** ✨"


def create_subject_slider(sub):
    return gr.Slider(1,5,value=3,step=1,label=f"📘 {sub} (1=Low ❤️, 5=High 💖)")

inputs = [create_subject_slider(sub) for sub in subjects]
inputs.append(gr.Dropdown(interest_options, label="🌟 Select your overall main interest"))


output = gr.Textbox(label="📝 Recommendation")


iface = gr.Interface(
    fn=recommend_stream,
    inputs=inputs,
    outputs=output,
    title="🤖 A/L Stream Advisor Chatbot",
    description="Rate your interest in each subject using sliders (1=Low ❤️, 5=High 💖), then select your overall interest. Click Submit to get your recommended stream!",
    theme="default"
)


iface.launch()

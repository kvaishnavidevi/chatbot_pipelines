import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
from dash.dependencies import Input, Output 
from wordcloud import WordCloud
import base64
from io import BytesIO
import logging
from configReader import ConfigReader

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Fetch config parameters 
try: 
    db_config = ConfigReader.get_database_config()
    logging.info(f"DB Config: {db_config}")  

except Exception as e:
    logging.error(f"Error reading config: {e}")

# Get paths from config
db_host = db_config.host
db_port = db_config.port
db_name = db_config.database
db_user = db_config.user
db_pwd = db_config.password

# Create database connection
engine = create_engine("postgresql://postgres:"+db_pwd+"@"+db_host+":"+db_port+"/"+db_name)

# Query and load data into DataFrame
#df = pd.read_sql("SELECT * FROM ai_conversations", engine)

def fetch_data():
    query = "SELECT * FROM ai_conversations;"
    df = pd.read_sql(query, engine)
    return df
# Fetch initial data for dropdown
df = fetch_data()

# Function to calculate metrics
def calculate_metrics(df, user_id):
    user_df = df[df['conv_userid'] == user_id]

    # Number of interactions
    num_interactions = len(user_df)

    # Splitting conversations into question/response
    questions = user_df[user_df['conv_role'] == 'user']['conversations']
    responses = user_df[user_df['conv_role'] == 'assistant']['conversations']

    # Average question length
    avg_question_length = round(questions.str.len().mean(),0) if not questions.empty else 0

    # Average response length
    avg_response_length = round(responses.str.len().mean(),0) if not responses.empty else 0

    # Total words exchanged
    total_words = user_df['conversations'].str.split().str.len().sum()

    # Response-to-question ratio
    response_to_question_ratio = len(responses) / len(questions) if len(questions) > 0 else 0

    return {
        "num_interactions": num_interactions,
        "avg_question_length": round(avg_question_length, 0),
        "avg_response_length": round(avg_response_length, 0),
        "total_words": total_words,
        "response_to_question_ratio": round(response_to_question_ratio, 0)
    }

def generate_wordcloud(user_df):
    text = " ".join(user_df['conversations'].dropna())  # Combine all conversations
    wordcloud = WordCloud(width=200, height=100, background_color="white").generate(text)

    # Convert to image format Dash can use
    img = BytesIO()
    wordcloud.to_image().save(img, format="PNG")
    img.seek(0)
    encoded_img = base64.b64encode(img.read()).decode()
    return f"data:image/png;base64,{encoded_img}"


# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("EVO11E Dashboard", style={'textAlign': 'center'}),

    # Dropdown
    html.Div([
        html.Label("Select User:", style={'fontSize': '18px', 'marginRight': '10px'}),
        dcc.Dropdown(
            id="user-dropdown",
            options=[{"label": uid, "value": uid} for uid in df["conv_userid"].dropna().unique()],
            value=df["conv_userid"].dropna().unique()[0],
            clearable=False,
            style={'width': '200px', 'fontSize': '16px'}
        ),
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '16px'}),

    # Row 1: Metrics & Word Cloud
    html.Div([
        # Metrics
        html.H4("Student interaction details", style={'textAlign': 'center', 'marginBottom': '5px'}),
        html.Div(id="metrics-output", style={
            'width': '48%', 'padding': '10px', 
             'textAlign': 'left'
        }),

        html.Div([
            html.H2("Frequently used words", style={'textAlign': 'center', 'marginBottom': '5px'}),
            html.Img(id="wordcloud-image", style={'width': '70%'})
        ], style={'width': '48%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

    # Row 2: Bar Chart
    html.Div([
        #html.H4("Question vs Response Length", style={'textAlign': 'center', 'marginBottom': '10px'}),
        dcc.Graph(id="bar-chart", style={'width': '40%'})
    ], style={'display': 'flex', 'justifyContent': 'left'}),

    dcc.Interval(
        id="interval-component",
        interval=120000,  # Refresh every 120 seconds
        n_intervals=0
    )
])
# Callback for updating metrics & chart
@app.callback(
    [Output("metrics-output", "children"),
     Output("bar-chart", "figure"),
     Output("wordcloud-image", "src")],
    [Input("user-dropdown", "value"),
     Input("interval-component", "n_intervals")]
)
def update_dashboard(user_id, n_intervals):
    df = fetch_data()

    # Update dropdown options with latest user list
    user_options = [{"label": uid, "value": uid} for uid in df["conv_userid"].dropna().unique()]
    
    # If no users in DB, set default values
    if not user_options:
        return [], None, html.P("No Data Available"), px.bar(), ""

    # If user_id is None or invalid, select the first available user
    if user_id is None or user_id not in df["conv_userid"].values:
        user_id = df["conv_userid"].dropna().unique()[0]

    user_df = df[df["conv_userid"] == user_id]
    metrics = calculate_metrics(user_df, user_id)

    # Create metrics display
    metrics_display = html.Div([
        html.P(f" Number of Interactions: {metrics['num_interactions']}"),
        html.P(f" Avg. Question Length: {metrics['avg_question_length']} characters"),
        html.P(f" Avg. Response Length: {metrics['avg_response_length']} characters"),
        html.P(f" Total Words Exchanged: {metrics['total_words']}"),
        html.P(f" Response-to-Question Ratio: {metrics['response_to_question_ratio']}"),
    ], style={'fontSize': '18px'})

    # Create bar chart
    fig = px.bar(
        x=["Avg. Question Length", "Avg. Response Length"],
        y=[metrics["avg_question_length"], metrics["avg_response_length"]],
        labels={"x": "Metric", "y": "Length (characters)"},
        title="Comparison of Question vs Response Length",
        text_auto=True
    )

        # Generate Word Cloud
    wordcloud_img = generate_wordcloud(user_df)

    return metrics_display, fig, wordcloud_img

# Run App
if __name__ == '__main__':
    app.run(debug=True)
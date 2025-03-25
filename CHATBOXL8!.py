import openai
import streamlit as st
import pandas as pd

# Set up OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])




# Classification function
def classify_tech(tech):
    avg_score = sum([
        tech["risk"], tech["stability"], tech["market_adoption"], tech["regulatory_maturity"],
        tech["infrastructure_readiness"], tech["commercial_viability"], tech["public_acceptance"],
        tech["technical_scalability"], tech["commercial_adoption"]
    ]) / 9

    if avg_score <= 2.5:
        return "Bleeding Edge"
    elif 2.5 < avg_score < 4.0:
        return "Leading Edge"
    elif avg_score >= 4.0:
        return "Commodity (Trailing Edge)"
    else:
        return "Unclear"

# Full tech list with known attributes
full_tech_list = [
    {"name": "Blockchain", "age": 3, "risk": 5, "stability": 2, "market_adoption": 1,
     "regulatory_maturity": 2, "infrastructure_readiness": 2, "commercial_viability": 2,
     "public_acceptance": 1, "technical_scalability": 1, "commercial_adoption": 1},

    {"name": "Blockchain in Private Equity", "age": 4, "risk": 3, "stability": 3, "market_adoption": 4,
     "regulatory_maturity": 3, "infrastructure_readiness": 4, "commercial_viability": 4,
     "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "LLM Deployment", "age": 2, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3,
     "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Drone Adoption", "age": 3, "risk": 4, "stability": 2, "market_adoption": 3, "regulatory_maturity": 2,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "AI Agents", "age": 2, "risk": 4, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2,
     "infrastructure_readiness": 2, "commercial_viability": 3, "public_acceptance": 2, "technical_scalability": 3, "commercial_adoption": 2},
    {"name": "AI-Enhanced Robotics", "age": 2, "risk": 4, "stability": 2, "market_adoption": 3, "regulatory_maturity": 2,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 2, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Wearables in Medicine", "age": 3, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 4, "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "IT/Energy Convergence", "age": 4, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 3},
    {"name": "Augmented AI", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Synthetic Biology", "age": 2, "risk": 5, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2,
     "infrastructure_readiness": 2, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 2, "commercial_adoption": 2},
    {"name": "Metaverse Platforms", "age": 2, "risk": 4, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2,
     "infrastructure_readiness": 3, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 3, "commercial_adoption": 2},
    {"name": "Digital Twins", "age": 4, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Web3 for Identity", "age": 2, "risk": 4, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2,
     "infrastructure_readiness": 2, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 2, "commercial_adoption": 2},
    {"name": "5G/6G Infrastructure", "age": 5, "risk": 3, "stability": 4, "market_adoption": 4, "regulatory_maturity": 4,
     "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Brain-Computer Interfaces", "age": 1, "risk": 5, "stability": 1, "market_adoption": 1, "regulatory_maturity": 1,
     "infrastructure_readiness": 1, "commercial_viability": 1, "public_acceptance": 1, "technical_scalability": 1, "commercial_adoption": 1},
    {"name": "Quantum Networking", "age": 2, "risk": 5, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2,
     "infrastructure_readiness": 2, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 2, "commercial_adoption": 2},
    {"name": "AI for Drug Discovery", "age": 3, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Green Hydrogen", "age": 3, "risk": 4, "stability": 2, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Edge AI", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "AI Code Assistants", "age": 2, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3,
     "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Autonomous Vehicles", "age": 4, "risk": 4, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 3},
    {"name": "Decentralized Energy Systems", "age": 3, "risk": 4, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "GenAI Content Creation", "age": 2, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3,
     "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Digital Trust Infrastructure", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3,
     "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3}
]

# Build tech name lookup
tech_lookup = {tech["name"].lower(): tech for tech in full_tech_list}

st.set_page_config(page_title="Tech Classifier", page_icon="💬")
st.title("🤖 Emerging Technology Classifier")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "Hi, I'm a helpful assistant that classifies emerging technologies based on YOUR FANTASTIC questions.     PLZ TRY OUT THE EXAMPLE PROMPT: How would you classify Blockchain? 😊"
        )}
    ]
# Display system prompt at the top
with st.chat_message("system"):
    if st.session_state.get("messages"):
        st.markdown(st.session_state["messages"][0]["content"])
# Chat input
user_input = st.chat_input("Ask about a technology or describe its attributes...")
if user_input:
    # Check if input mentions a known tech name
    matched = None
    for tech_name in sorted(tech_lookup.keys(), key=len, reverse=True):
        if tech_name in user_input.lower():
            matched = tech_lookup[tech_name]
            break

    if matched:
        classification = classify_tech(matched)
        reply = f"✅ **{matched['name']}** is classified as: **{classification}**"
    else:
        # Fallback to GPT
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Analyzing..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "assistant" and msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

import openai
import streamlit as st
import pandas as pd
import os


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

# Updated list of emerging technologies and applications
full_tech_list = [
    {"name": "Blockchain", "application": "Private Equity", "age": 3, "risk": 5, "stability": 2, "market_adoption": 1,
     "regulatory_maturity": 2, "infrastructure_readiness": 2, "commercial_viability": 2,
     "public_acceptance": 1, "technical_scalability": 1, "commercial_adoption": 1},

    {"name": "Blockchain in Private Equity", "application": "Secure recordkeeping and asset tracking in private equity", "age": 4, "risk": 3, "stability": 3, "market_adoption": 4,
     "regulatory_maturity": 3, "infrastructure_readiness": 4, "commercial_viability": 4,
     "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},

    {"name": "AI Agents", "application": "Autonomous support agents, AI workflow assistants", "age": 2, "risk": 4, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2, "infrastructure_readiness": 2, "commercial_viability": 3, "public_acceptance": 2, "technical_scalability": 3, "commercial_adoption": 2},
    {"name": "AI Agents in Auto-Driving", "application": "AI-driven decision systems in self-driving vehicles", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 3},
    {"name": "LLM Deployment", "application": "Domain-specific large and small language models", "age": 2, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3, "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Drone Adoption", "application": "Drones in logistics, agriculture, disaster response", "age": 3, "risk": 4, "stability": 2, "market_adoption": 3, "regulatory_maturity": 2, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "AI-Enhanced Robotics", "application": "Robots with embodied intelligence and adaptability", "age": 2, "risk": 4, "stability": 2, "market_adoption": 3, "regulatory_maturity": 2, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 2, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Wearables/Biomarkers in Medicine/Wellness", "application": "Medical-grade health monitoring", "age": 3, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 4, "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "IT/Energy Convergence", "application": "Digital transformation of energy sector", "age": 4, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 4, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 3},
    {"name": "Augmented Artificial Intelligence (A2I)", "application": "Human-AI collaborative systems", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Autonomous Driving", "application": "Self-driving vehicles across use cases", "age": 4, "risk": 4, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 3},
    {"name": "SmartAg", "application": "AI-driven agriculture for yield and sustainability", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Functional Safety for Autonomous Vehicles", "application": "Reliable and safe autonomous systems", "age": 3, "risk": 4, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "AI-Assisted Drug Discovery", "application": "AI-accelerated pharmaceutical R&D", "age": 3, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "Sustainable Computing", "application": "Green IT and carbon-efficient computing", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Misinformation/Disinformation Detection", "application": "AI filters for content credibility", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "AI-Based Medical Diagnosis", "application": "Enhanced diagnostics using AI", "age": 3, "risk": 3, "stability": 3, "market_adoption": 4, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 4, "public_acceptance": 4, "technical_scalability": 4, "commercial_adoption": 4},
    {"name": "AI-Optimized Green HPC", "application": "High-performance computing with lower carbon", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Next-Gen Cyberwarfare", "application": "AI-powered cyber defense and offense", "age": 2, "risk": 4, "stability": 3, "market_adoption": 3, "regulatory_maturity": 2, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 2, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "New Battery Chemistries", "application": "Solid-state and sodium-ion batteries", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 3, "infrastructure_readiness": 3, "commercial_viability": 4, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Data Feudalism", "application": "User-owned and monetized data ecosystems", "age": 2, "risk": 4, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2, "infrastructure_readiness": 2, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 2, "commercial_adoption": 2},
    {"name": "Nuclear-Powered Data Centers", "application": "Small modular reactors for green computing", "age": 2, "risk": 5, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2, "infrastructure_readiness": 2, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 2, "commercial_adoption": 2},
    {"name": "Tools and Policies for AI Regulation", "application": "Ethical and policy frameworks for AI", "age": 3, "risk": 3, "stability": 3, "market_adoption": 3, "regulatory_maturity": 4, "infrastructure_readiness": 3, "commercial_viability": 3, "public_acceptance": 3, "technical_scalability": 3, "commercial_adoption": 3},
    {"name": "Brain-Computer Interfaces (BCIs)", "application": "Neural input/output interfaces", "age": 1, "risk": 5, "stability": 1, "market_adoption": 1, "regulatory_maturity": 1, "infrastructure_readiness": 1, "commercial_viability": 1, "public_acceptance": 1, "technical_scalability": 1, "commercial_adoption": 1},
    {"name": "Space Computing", "application": "Fault-tolerant space-based processors", "age": 2, "risk": 4, "stability": 2, "market_adoption": 2, "regulatory_maturity": 2, "infrastructure_readiness": 2, "commercial_viability": 2, "public_acceptance": 2, "technical_scalability": 2, "commercial_adoption": 2},
]

# Chat input
user_input = st.chat_input("Ask about a technology or describe its attributes...")
if user_input:
    matched = None
    lowered_input = user_input.lower()
    for tech_key in sorted(tech_lookup.keys(), key=len, reverse=True):
        if tech_key in lowered_input:
            matched = tech_lookup[tech_key]
            break

    if matched:
        classification = classify_tech(matched)
        application = matched.get("application", "N/A")
        reply = f"✅ **{matched['name']}** is classified as: **{classification}**\n\n📌 Application: _{application}_"
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Analyzing with GPT..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages + [
                    {"role": "system", "content": (
                        "If the user asks about a technology not in the database, respond with the most likely classification as one of the following:\n"
                        "- Bleeding Edge\n"
                        "- Leading Edge\n"
                        "- Commodity (Trailing Edge)\n\n"
                        "Please respond with the following format:\n"
                        "✅ **[Technology Name]** is classified as: **[Classification]**\n\n📌 Application: _[If known or inferred, else N/A]_"
                    )},
                ]
            )
            reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] not in ["assistant", "system"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

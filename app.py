import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

if "messages" not in st.session_state:
    st.session_state.messages = []

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.sidebar.title("🏦 SmartBank-Agent")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Customer Profile",
        "Goal Planner",
        "Recommendations",
        "AI Coach",
        "Customer Segmentation"
    ]
)

if page == "Home":
    st.title("🏦 SmartBank-Agent")
    st.subheader("An Agentic AI Platform for Personalized Banking & Financial Growth")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Customers", "1,250")

    with col2:
        st.metric("Goals Created", "320")

    with col3:
        st.metric("Active Users", "890")

    st.divider()
    st.subheader("📌 Current Customer Summary")

    st.write(f"**Name:** {st.session_state.get('name', 'Not set')}")
    st.write(f"**Segment:** {st.session_state.get('segment', 'Not analyzed')}")
    st.write(f"**Monthly Savings:** ₹{st.session_state.get('savings', 'Not set')}")

    st.write(f"**Goal:** {st.session_state.get('goal', 'No goal set')}")
    st.write(f"**Target Amount:** ₹{st.session_state.get('goal_amount', 'N/A')}")
    st.write(f"**Required Monthly Saving:** ₹{st.session_state.get('monthly_target', 'N/A')}")

    st.divider()
    st.subheader("📈 Financial Health")

    income = st.session_state.get("income", 0)
    expenses = st.session_state.get("expenses", 0)

    if income > 0:
        score = int(((income - expenses) / income) * 100)
        score = max(0, min(score, 100))
        st.progress(score)
        st.write(f"Financial Health Score: **{score}%**")
    else:
        st.info("Complete customer profile to view financial health.")

elif page == "Customer Profile":
    st.title("👤 Customer Profile")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100)
    occupation = st.selectbox(
        "Occupation",
        ["Student", "Salaried", "Business", "Other"]
    )
    income = st.number_input("Monthly Income (₹)", min_value=0)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0)

    if st.button("Analyze Profile"):
        savings = income - expenses

        if age <= 25:
            segment = "Student Saver"
        elif income >= 80000:
            segment = "Premium Customer"
        elif savings >= 15000:
            segment = "Growth Investor"
        else:
            segment = "Regular Banking User"

        st.session_state["name"] = name
        st.session_state["age"] = age
        st.session_state["occupation"] = occupation
        st.session_state["income"] = income
        st.session_state["expenses"] = expenses
        st.session_state["savings"] = savings
        st.session_state["segment"] = segment

        st.success("Profile Saved Successfully")
        st.write(f"**Customer Name:** {name}")
        st.write(f"**Customer Segment:** {segment}")
        st.write(f"**Monthly Savings:** ₹{savings}")

elif page == "Goal Planner":
    st.title("🎯 Goal Planner")

    goal = st.text_input("Your Goal")
    amount = st.number_input("Target Amount (₹)", min_value=0)
    months = st.number_input("Months", min_value=1)

    if st.button("Calculate Plan"):
        monthly = amount / months
        savings = st.session_state.get("savings", 0)

        st.session_state["goal"] = goal
        st.session_state["goal_amount"] = amount
        st.session_state["goal_months"] = months
        st.session_state["monthly_target"] = monthly

        st.success(f"You need to save ₹{monthly:.0f} per month")

        if savings >= monthly:
            st.success("✅ Goal Achievable")
        else:
            st.error("❌ Goal Not Achievable with current savings")

        st.write("Recommended Banking Products:")

        if monthly <= 3000:
            st.info("Savings Account + UPI Rewards")
        elif monthly <= 10000:
            st.info("Recurring Deposit + SIP")
        else:
            st.info("Fixed Deposit + Investment Plan")

elif page == "Recommendations":
    st.title("💡 Banking Recommendations")

    segment = st.session_state.get("segment", "Not analyzed")

    st.write(f"**Customer Segment:** {segment}")

    if segment == "Student Saver":
        st.success("🎓 Student Savings Account")
        st.success("📱 UPI Cashback Rewards")
        st.success("💰 Small Recurring Deposit")

    elif segment == "Growth Investor":
        st.success("📈 SIP Investment Plan")
        st.success("🏦 Recurring Deposit")
        st.success("🛡️ Basic Insurance Plan")

    elif segment == "Premium Customer":
        st.success("💎 Premium Savings Account")
        st.success("🏦 Fixed Deposit")
        st.success("📊 Wealth Management Services")

    elif segment == "Regular Banking User":
        st.success("🏦 Savings Account Upgrade")
        st.success("📱 Mobile Banking Adoption")
        st.success("💳 Debit/Credit Card Offers")

    else:
        st.info("Complete Customer Profile first.")

elif page == "AI Coach":
    st.title("🤖 AI Financial Coach")

    name = st.session_state.get("name", "Not provided")
    age = st.session_state.get("age", "Not provided")
    occupation = st.session_state.get("occupation", "Not provided")
    income = st.session_state.get("income", "Not provided")
    expenses = st.session_state.get("expenses", "Not provided")
    savings = st.session_state.get("savings", "Not provided")
    segment = st.session_state.get("segment", "Not analyzed")

    goal = st.session_state.get("goal", "No goal set")
    goal_amount = st.session_state.get("goal_amount", "N/A")
    goal_months = st.session_state.get("goal_months", "N/A")
    monthly_target = st.session_state.get("monthly_target", "N/A")

    st.info(f"Current Customer Segment: {segment}")
    st.subheader("Chat History")

    for msg in st.session_state.messages:
         if msg["role"] == "user":
            st.write(f"🧑 You: {msg['content']}")
         else:
            st.write(f"🤖 SmartBank-Agent: {msg['content']}")
           

    question = st.text_area("Ask SmartBank-Agent")

    if st.button("Ask AI"):
        if not api_key:
            st.error("Gemini API key not found. Check your .env file.")
        elif not question:
            st.error("Please ask a question.")
        else:
            client = genai.Client(api_key=api_key)

            prompt = f"""
            You are SmartBank-Agent, an AI banking companion.

            Your task:
            - Give simple financial guidance.
            - Recommend useful banking products.
            - Encourage digital banking adoption.
            - Help with savings and financial goals.
            - Avoid guaranteed investment advice.

            Customer Profile:
            Name: {name}
            Age: {age}
            Occupation: {occupation}
            Monthly Income: ₹{income}
            Monthly Expenses: ₹{expenses}
            Monthly Savings: ₹{savings}
            Customer Segment: {segment}

            Financial Goal:
            Goal: {goal}
            Target Amount: ₹{goal_amount}
            Timeline: {goal_months} months
            Required Monthly Saving: ₹{monthly_target}

            User Question:
            {question}
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.session_state.messages.append(
                {"role": "user", "content": question}
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": response.text}
            )
            
            st.success("AI Response")
            st.write(response.text)


elif page == "Customer Segmentation":
    st.title("👥 AI Customer Segmentation")

    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    data = pd.DataFrame({
        "Age": [25, 30, 35, 40, 45, 50, 28, 32, 38, 55],
        "Income": [30000, 45000, 50000, 70000, 85000, 100000, 35000, 48000, 75000, 120000],
        "Savings": [5000, 10000, 12000, 25000, 35000, 50000, 7000, 11000, 28000, 60000]
    })

    st.subheader("Customer Dataset")
    st.dataframe(data)

    X = data[["Age", "Income", "Savings"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    data["Cluster"] = kmeans.fit_predict(X_scaled)

    st.subheader("Segmented Customers")
    st.dataframe(data)

    st.subheader("Cluster Summary")
    st.dataframe(data.groupby("Cluster").mean())

    st.subheader("AI Insights")

    for cluster in sorted(data["Cluster"].unique()):
        cluster_data = data[data["Cluster"] == cluster]

        avg_income = cluster_data["Income"].mean()
        avg_savings = cluster_data["Savings"].mean()

        if avg_income > 80000:
            label = "💎 High Value Customers"
        elif avg_income > 50000:
            label = "⭐ Growth Customers"
        else:
            label = "🌱 Starter Customers"

        st.write(f"Cluster {cluster}: {label}")



       
import streamlit as st
import plotly.express as px

from data_loader import load_data
from ai_assistant import generate_ticket_summary, suggest_reply, detect_sentiment


st.set_page_config(
    page_title="Support Intelligence Dashboard",
    layout="wide",
)

st.title("Customer Support Intelligence Dashboard")

df = load_data()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Search & Tickets", "AI Assistant"]
)

st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique()),
)

selected_priority = st.sidebar.multiselect(
    "Priority",
    options=sorted(df["priority"].dropna().unique()),
    default=sorted(df["priority"].dropna().unique()),
)

selected_status = st.sidebar.multiselect(
    "Status",
    options=sorted(df["status"].dropna().unique()),
    default=sorted(df["status"].dropna().unique()),
)

filtered_df = df[
    (df["category"].isin(selected_category))
    & (df["priority"].isin(selected_priority))
    & (df["status"].isin(selected_status))
]


if page == "Dashboard":
    st.subheader("Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Tickets", len(filtered_df))
    col2.metric("Categories", filtered_df["category"].nunique())
    col3.metric(
        "Open Tickets",
        len(filtered_df[filtered_df["status"].str.lower() == "open"])
    )
    col4.metric(
        "Escalated",
        len(filtered_df[filtered_df["escalated"].astype(str).str.lower() == "yes"])
    )
    col5.metric(
        "SLA Breached",
        len(filtered_df[filtered_df["sla_breached"].astype(str).str.lower() == "yes"])
    )

    st.subheader("Dashboard Charts")

    col1, col2 = st.columns(2)

    with col1:
        category_counts = filtered_df["category"].value_counts().reset_index()
        category_counts.columns = ["category", "count"]

        fig_category = px.bar(
            category_counts,
            x="category",
            y="count",
            title="Tickets by Category",
        )
        st.plotly_chart(fig_category, use_container_width=True)

    with col2:
        priority_counts = filtered_df["priority"].value_counts().reset_index()
        priority_counts.columns = ["priority", "count"]

        fig_priority = px.pie(
            priority_counts,
            names="priority",
            values="count",
            title="Tickets by Priority",
            color="priority",
            color_discrete_map={
                "Urgent": "red",
                "High": "orange",
                "Medium": "blue",
                "Low": "green",
            },
        )
        st.plotly_chart(fig_priority, use_container_width=True)
        st.subheader("Customer Sentiment Overview")

        sentiment_df = filtered_df.copy()

        sentiment_df["sentiment"] = sentiment_df["issue_description"].apply(
            detect_sentiment
        )

        sentiment_counts = sentiment_df["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["sentiment", "count"]

        fig_sentiment = px.pie(
            sentiment_counts,
            names="sentiment",
            values="count",
            title="Customer Sentiment Distribution",
            color="sentiment",
            color_discrete_map={
                "Negative": "red",
                "Neutral": "blue",
                "Positive": "green",
            },
        )

        st.plotly_chart(fig_sentiment, use_container_width=True)

        status_counts = filtered_df["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]

        fig_status = px.bar(
            status_counts,
            x="status",
            y="count",
            title="Tickets by Status",
        )
        st.plotly_chart(fig_status, use_container_width=True)


elif page == "Search & Tickets":
    st.subheader("Search Tickets")

    query = st.text_input("Search by issue description, product, customer, or notes")

    if query:
        search_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(query, case=False, na=False).any(),
                axis=1,
            )
        ]
    else:
        search_df = filtered_df

    st.write(f"Showing {len(search_df)} tickets")
    display_columns = [
    "ticket_id",
    "customer_name",
    "product",
    "category",
    "priority",
    "status",
    "issue_description",
]
    st.dataframe(search_df[display_columns])

    st.subheader("Ticket Details")

    ticket_ids = search_df["ticket_id"].tolist()

    if ticket_ids:
        selected_ticket = st.selectbox("Select Ticket ID", ticket_ids)

        ticket_data = search_df[
            search_df["ticket_id"] == selected_ticket
        ].iloc[0]

        st.markdown(f"### Ticket #{ticket_data['ticket_id']}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Customer Name:**", ticket_data["customer_name"])
            st.write("**Product:**", ticket_data["product"])
            st.write("**Category:**", ticket_data["category"])
            priority = str(ticket_data["priority"]).lower()

            if priority == "urgent":
                st.error(f"Priority: {ticket_data['priority']}")
            elif priority == "high":
                st.warning(f"Priority: {ticket_data['priority']}")
            elif priority == "medium":
                st.info(f"Priority: {ticket_data['priority']}")
            else:
                st.success(f"Priority: {ticket_data['priority']}")
            st.write("**Status:**", ticket_data["status"])

        with col2:
            st.write("**Channel:**", ticket_data["channel"])
            st.write("**Region:**", ticket_data["region"])
            st.write("**Language:**", ticket_data["language"])
            st.write("**Subscription:**", ticket_data["subscription_type"])

        st.markdown("### Issue Description")
        st.info(ticket_data["issue_description"])

        st.markdown("### Resolution Notes")
        st.success(ticket_data["resolution_notes"])
    else:
        st.warning("No tickets found for the current search/filter.")


elif page == "AI Assistant":
    st.subheader("AI Assistant")

    ticket_ids = filtered_df["ticket_id"].tolist()

    if ticket_ids:
        selected_ticket = st.selectbox("Select Ticket ID", ticket_ids)

        ticket_data = filtered_df[
            filtered_df["ticket_id"] == selected_ticket
        ].iloc[0]

        st.markdown(f"### Ticket #{ticket_data['ticket_id']}")

        st.markdown("### Issue Description")
        st.info(ticket_data["issue_description"])
        
        sentiment = detect_sentiment(ticket_data["issue_description"])

        if sentiment == "Negative":
            st.error(f"Sentiment: {sentiment}")
        elif sentiment == "Positive":
            st.success(f"Sentiment: {sentiment}")
        else:
            st.info(f"Sentiment: {sentiment}")

        summary = generate_ticket_summary(
            ticket_data["issue_description"],
            ticket_data["category"],
            ticket_data["priority"],
            ticket_data["status"],
        )

        reply = suggest_reply(
            ticket_data["issue_description"],
            ticket_data["category"],
            ticket_data["priority"],
        )

        st.markdown("### Ticket Summary")
        st.info(summary)

        st.markdown("### Suggested Reply")
        st.success(reply)
    else:
        st.warning("No tickets available for the current filters.")
from datetime import date, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.storage import (
    load_tutors, load_bookings, add_booking, update_booking_status,
    load_messages, add_message, load_reviews, add_review
)
from utils.recommender import recommend_tutors


st.set_page_config(
    page_title="Student Tutor",
    page_icon="🎓",
    layout="wide"
)

tutors = load_tutors()
bookings = load_bookings()
messages = load_messages()
reviews = load_reviews()


def money(v):
    return f"₹{float(v):,.0f}"


def tutor_card(row):
    st.markdown(f"### {row['name']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Subject", row["subject"])
    c2.metric("Rating", f"⭐ {row['rating']}")
    c3.metric("Fee / hour", money(row["hourly_fee"]))
    st.write(row["bio"])
    st.caption(
        f"Levels: {row['levels']} | Experience: {row['experience']} | "
        f"Languages: {row['languages']}"
    )
    st.write("Specialties:", row["specialties"])
    st.write("Availability:", row["availability"])


with st.sidebar:
    st.title("Student Tutor")
    st.caption("Find. Learn. Grow.")

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Find Tutors",
            "Smart Tutor Match",
            "Book a Session",
            "My Bookings",
            "Messages",
            "Reviews",
            "Tutor Dashboard"
        ]
    )

    st.divider()
    st.write("Platform overview")
    st.metric("Tutors", len(tutors))
    st.metric("Subjects", tutors["subject"].nunique())


if page == "Home":
    st.title("Student Tutor")
    st.subheader("Connect students with the right tutor")

    st.write(
        "A simple online tutoring platform where students can discover tutors, "
        "compare profiles, get recommendations, book sessions, and communicate."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Verified Tutor Profiles", len(tutors))
    c2.metric("Subjects Available", tutors["subject"].nunique())
    c3.metric("Average Rating", f"{tutors['rating'].mean():.1f} ⭐")
    c4.metric("Starting Fee", money(tutors["hourly_fee"].min()))

    st.divider()

    st.subheader("Popular Subjects")
    subject_counts = tutors.groupby("subject", as_index=False).size()
    fig = px.bar(subject_counts, x="subject", y="size", text_auto=True)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Number of Tutors",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Rated Tutors")
    top = tutors.sort_values("rating", ascending=False).head(3)
    cols = st.columns(3)
    for col, (_, row) in zip(cols, top.iterrows()):
        with col:
            st.markdown(f"#### {row['name']}")
            st.write(row["subject"])
            st.write(f"⭐ {row['rating']} | {money(row['hourly_fee'])}/hour")
            st.caption(row["bio"])


elif page == "Find Tutors":
    st.title("Find Tutors")
    st.caption("Search and compare tutors by subject, rating, and budget.")

    c1, c2, c3 = st.columns(3)

    subjects = ["All"] + sorted(tutors["subject"].unique().tolist())

    with c1:
        subject = st.selectbox("Subject", subjects)

    with c2:
        min_rating = st.slider(
            "Minimum Rating",
            0.0, 5.0, 0.0, 0.1
        )

    with c3:
        max_fee = st.slider(
            "Maximum Fee / hour",
            int(tutors["hourly_fee"].min()),
            int(tutors["hourly_fee"].max()),
            int(tutors["hourly_fee"].max()),
            10
        )

    search = st.text_input(
        "Search by tutor name, specialty, or language"
    ).strip().lower()

    filtered = tutors.copy()

    if subject != "All":
        filtered = filtered[filtered["subject"] == subject]

    filtered = filtered[
        (filtered["rating"] >= min_rating) &
        (filtered["hourly_fee"] <= max_fee)
    ]

    if search:
        mask = (
            filtered["name"].str.lower().str.contains(search) |
            filtered["specialties"].str.lower().str.contains(search) |
            filtered["languages"].str.lower().str.contains(search)
        )
        filtered = filtered[mask]

    st.write(f"{len(filtered)} tutor(s) found")
    st.divider()

    if filtered.empty:
        st.info("No tutors match the selected filters.")
    else:
        for _, row in filtered.iterrows():
            with st.container(border=True):
                tutor_card(row)


elif page == "Smart Tutor Match":
    st.title("Smart Tutor Match")
    st.caption(
        "Get ranked tutor suggestions based on subject, budget, and rating."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        subject = st.selectbox(
            "What do you want to learn?",
            ["Any"] + sorted(tutors["subject"].unique().tolist())
        )

    with c2:
        max_fee = st.number_input(
            "Maximum fee per hour (₹)",
            min_value=100,
            value=500,
            step=50
        )

    with c3:
        min_rating = st.slider(
            "Minimum preferred rating",
            0.0, 5.0, 4.0, 0.1
        )

    if st.button("Find My Best Tutors", use_container_width=True):
        result = recommend_tutors(
            tutors,
            subject,
            max_fee,
            min_rating
        )

        if result.empty:
            st.warning("No exact match found. Try increasing your budget or lowering the rating filter.")
        else:
            st.success(f"Found {len(result)} suitable tutor(s).")

            for rank, (_, row) in enumerate(result.iterrows(), start=1):
                with st.container(border=True):
                    st.markdown(f"### #{rank} — {row['name']}")
                    st.write(
                        f"{row['subject']} | ⭐ {row['rating']} | "
                        f"{money(row['hourly_fee'])}/hour"
                    )
                    st.write(row["bio"])
                    st.caption(
                        f"Specialties: {row['specialties']} | "
                        f"Languages: {row['languages']}"
                    )


elif page == "Book a Session":
    st.title("Book a Teaching Session")
    st.caption("Select a tutor and choose your preferred schedule.")

    tutor_names = tutors["name"].tolist()
    selected_name = st.selectbox("Choose Tutor", tutor_names)
    selected = tutors[tutors["name"] == selected_name].iloc[0]

    with st.container(border=True):
        tutor_card(selected)

    with st.form("booking_form"):
        c1, c2 = st.columns(2)

        with c1:
            student_name = st.text_input("Student Name")
            student_email = st.text_input("Student Email")
            session_date = st.date_input(
                "Session Date",
                value=date.today() + timedelta(days=1),
                min_value=date.today()
            )

        with c2:
            session_time = st.selectbox(
                "Preferred Time",
                [
                    "09:00 AM","10:00 AM","11:00 AM",
                    "02:00 PM","04:00 PM","06:00 PM","07:30 PM"
                ]
            )
            duration = st.selectbox(
                "Duration",
                ["30 minutes","60 minutes","90 minutes"]
            )
            notes = st.text_area(
                "Learning Requirement",
                placeholder="Example: Need help with quadratic equations"
            )

        submitted = st.form_submit_button(
            "Confirm Booking",
            use_container_width=True
        )

        if submitted:
            if not student_name.strip() or "@" not in student_email:
                st.error("Please enter a valid student name and email.")
            else:
                # Check simple scheduling conflict for tutor.
                latest = load_bookings()
                conflict = latest[
                    (latest["tutor_name"] == selected_name) &
                    (latest["date"].astype(str) == str(session_date)) &
                    (latest["time"].astype(str) == str(session_time)) &
                    (latest["status"] == "Scheduled")
                ]

                if not conflict.empty:
                    st.error(
                        "This tutor already has a session at that time. "
                        "Please select another slot."
                    )
                else:
                    booking_id = add_booking(
                        student_name,
                        student_email,
                        int(selected["id"]),
                        selected_name,
                        selected["subject"],
                        session_date,
                        session_time,
                        duration,
                        notes
                    )
                    st.success(
                        f"Session booked successfully. Booking ID: {booking_id}"
                    )


elif page == "My Bookings":
    st.title("My Bookings")

    email = st.text_input(
        "Enter your student email to view bookings"
    ).strip()

    if email:
        current = load_bookings()
        mine = current[
            current["student_email"].str.lower() == email.lower()
        ]

        if mine.empty:
            st.info("No bookings found for this email.")
        else:
            st.dataframe(mine, use_container_width=True)

            active = mine[mine["status"] == "Scheduled"]

            if not active.empty:
                st.subheader("Cancel a Session")

                options = active["booking_id"].tolist()
                selected_booking = st.selectbox(
                    "Booking ID",
                    options
                )

                if st.button("Cancel Booking"):
                    update_booking_status(
                        selected_booking,
                        "Cancelled"
                    )
                    st.success("Booking cancelled.")
                    st.rerun()


elif page == "Messages":
    st.title("Student–Tutor Messages")
    st.caption("Simple local messaging for project demonstration.")

    with st.form("message_form", clear_on_submit=True):
        student_name = st.text_input("Student Name")
        tutor_name = st.selectbox(
            "Tutor",
            tutors["name"].tolist()
        )
        message = st.text_area(
            "Message",
            placeholder="Ask about the lesson, topic, or availability..."
        )

        if st.form_submit_button(
            "Send Message",
            use_container_width=True
        ):
            if not student_name.strip() or not message.strip():
                st.error("Please enter your name and message.")
            else:
                add_message(
                    student_name,
                    tutor_name,
                    message
                )
                st.success("Message sent.")
                st.rerun()

    st.divider()

    all_messages = load_messages()

    if all_messages.empty:
        st.info("No messages yet.")
    else:
        st.subheader("Recent Messages")
        st.dataframe(
            all_messages.sort_values(
                "timestamp",
                ascending=False
            ),
            use_container_width=True
        )


elif page == "Reviews":
    st.title("Tutor Reviews")

    with st.form("review_form", clear_on_submit=True):
        student_name = st.text_input("Student Name")
        tutor_name = st.selectbox(
            "Tutor",
            tutors["name"].tolist()
        )
        rating = st.slider("Rating", 1, 5, 5)
        review = st.text_area("Review")

        if st.form_submit_button(
            "Submit Review",
            use_container_width=True
        ):
            if not student_name.strip() or not review.strip():
                st.error("Please complete all fields.")
            else:
                add_review(
                    student_name,
                    tutor_name,
                    rating,
                    review
                )
                st.success("Review submitted.")
                st.rerun()

    st.divider()

    all_reviews = load_reviews()

    if all_reviews.empty:
        st.info("No student reviews submitted yet.")
    else:
        for _, row in all_reviews.iloc[::-1].iterrows():
            with st.container(border=True):
                st.write(f"**{row['tutor_name']}** — {'⭐' * int(row['rating'])}")
                st.write(row["review"])
                st.caption(f"By {row['student_name']}")


elif page == "Tutor Dashboard":
    st.title("Tutor Dashboard")
    st.caption("View scheduled sessions for a selected tutor.")

    tutor_name = st.selectbox(
        "Select Tutor",
        tutors["name"].tolist()
    )

    all_bookings = load_bookings()
    tutor_bookings = all_bookings[
        all_bookings["tutor_name"] == tutor_name
    ]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Bookings", len(tutor_bookings))
    c2.metric(
        "Scheduled",
        int((tutor_bookings["status"] == "Scheduled").sum())
        if not tutor_bookings.empty else 0
    )
    c3.metric(
        "Cancelled",
        int((tutor_bookings["status"] == "Cancelled").sum())
        if not tutor_bookings.empty else 0
    )

    if tutor_bookings.empty:
        st.info("No bookings for this tutor yet.")
    else:
        st.dataframe(
            tutor_bookings,
            use_container_width=True
        )

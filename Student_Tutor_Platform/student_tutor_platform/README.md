# Student Tutor Platform

A complete Streamlit-based online tutoring platform that connects students with suitable tutors based on subject, budget, rating, and learning requirements.

## Main Features

- Tutor discovery
- Search by tutor name, specialty, and language
- Filter by subject
- Filter by rating
- Filter by hourly fee
- Detailed tutor profiles
- Smart tutor recommendation system
- Session booking
- Tutor availability conflict checking
- Student booking history
- Booking cancellation
- Student–tutor messaging
- Tutor reviews and ratings
- Tutor dashboard
- Local CSV data storage
- No paid API required

## Run the Project

Install requirements:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Problem Statement

Finding the right tutor can be difficult for students, especially when they need help in a specific subject, have a limited budget, require a particular teaching style, or need classes at suitable times. Students often depend on personal references, local advertisements, or scattered online information to find tutors. This process can be time-consuming and may not provide enough information about a tutor's experience, subjects, ratings, fees, language, availability, and areas of expertise.

Students also face problems when comparing multiple tutors and deciding which one is most suitable for their needs. Even after finding a tutor, communication and scheduling may happen through different applications, making the overall process less organized. Tutors may also find it difficult to manage student requests and teaching sessions efficiently.

There is therefore a need for a simple and organized platform that helps students discover suitable tutors, compare their profiles, communicate with them, and schedule teaching sessions from one place.

## Solution Statement

Student Tutor is an online tutoring platform designed to connect students with suitable tutors based on their academic requirements and preferences. The application allows students to browse tutor profiles containing information such as subjects, teaching levels, experience, ratings, hourly fees, specialties, languages, availability, and tutor descriptions.

Students can search and filter tutors by subject, rating, budget, specialty, and language. The platform also includes a Smart Tutor Match feature that ranks suitable tutors using a recommendation score based mainly on tutor rating and the student's preferred fee range.

After selecting a tutor, students can book a teaching session by choosing a date, time, and duration and by providing their learning requirements. The application checks whether the selected tutor already has another scheduled session at the requested time before confirming the booking.

Students can view their existing bookings using their email address, cancel scheduled sessions, send messages to tutors, and submit ratings and reviews. Tutors can use a dashboard to view their scheduled and cancelled sessions.

The project is built using Python and Streamlit and stores application data locally using CSV files. It does not require any paid API key or external database, making it easy to run and demonstrate on a local computer.

## Project Structure

```text
student_tutor_platform/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── data/
│   ├── tutors.csv
│   ├── bookings.csv
│   ├── messages.csv
│   └── reviews.csv
└── utils/
    ├── storage.py
    └── recommender.py
```

## Future Improvements

- Student and tutor login/signup
- Password authentication
- Tutor registration and profile editing
- Video classes
- Calendar integration
- Real-time chat
- Email booking notifications
- Payment gateway
- AI-based tutor matching
- Database using Firebase, Supabase, PostgreSQL, or MongoDB
- Admin dashboard

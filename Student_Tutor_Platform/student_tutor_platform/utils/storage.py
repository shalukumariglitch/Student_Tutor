from pathlib import Path
from datetime import datetime
import pandas as pd

DATA_DIR = Path("data")
TUTORS_FILE = DATA_DIR / "tutors.csv"
BOOKINGS_FILE = DATA_DIR / "bookings.csv"
MESSAGES_FILE = DATA_DIR / "messages.csv"
REVIEWS_FILE = DATA_DIR / "reviews.csv"


def load_tutors():
    return pd.read_csv(TUTORS_FILE)


def load_bookings():
    return pd.read_csv(BOOKINGS_FILE)


def save_bookings(df):
    df.to_csv(BOOKINGS_FILE, index=False)


def add_booking(student_name, student_email, tutor_id, tutor_name,
                subject, date, time, duration, notes):
    df = load_bookings()
    booking_id = f"B{len(df)+1:04d}"
    row = pd.DataFrame([{
        "booking_id": booking_id,
        "student_name": student_name,
        "student_email": student_email,
        "tutor_id": tutor_id,
        "tutor_name": tutor_name,
        "subject": subject,
        "date": str(date),
        "time": str(time),
        "duration": duration,
        "status": "Scheduled",
        "notes": notes
    }])
    df = pd.concat([df, row], ignore_index=True)
    save_bookings(df)
    return booking_id


def update_booking_status(booking_id, status):
    df = load_bookings()
    if booking_id in df["booking_id"].astype(str).values:
        df.loc[df["booking_id"].astype(str) == str(booking_id), "status"] = status
        save_bookings(df)


def load_messages():
    return pd.read_csv(MESSAGES_FILE)


def add_message(student_name, tutor_name, message):
    df = load_messages()
    message_id = f"M{len(df)+1:04d}"
    row = pd.DataFrame([{
        "message_id": message_id,
        "student_name": student_name,
        "tutor_name": tutor_name,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    df = pd.concat([df, row], ignore_index=True)
    df.to_csv(MESSAGES_FILE, index=False)


def load_reviews():
    return pd.read_csv(REVIEWS_FILE)


def add_review(student_name, tutor_name, rating, review):
    df = load_reviews()
    row = pd.DataFrame([{
        "student_name": student_name,
        "tutor_name": tutor_name,
        "rating": rating,
        "review": review
    }])
    df = pd.concat([df, row], ignore_index=True)
    df.to_csv(REVIEWS_FILE, index=False)

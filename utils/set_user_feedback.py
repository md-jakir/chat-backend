from utils.logger import logger
from sqlalchemy import text
def set_user_feedback(session_id, query_id, feedback, feedback_text, db):
    try:
        feedback_query = f"UPDATE session_history SET feedback={feedback}, detail_feedback='{feedback_text}' WHERE session_id='{session_id}' and query_id='{query_id}'"
        db.execute(text(feedback_query))
        db.commit()

        return "Feedback inserted Successfully!"

    except Exception as e:
        logger.info(e)
        return "Feedback insertion Failed!"
from fastapi import HTTPException
from utils.logger import logger
from app.models.session import Session
from app.models.session_hiostory import SessionHistory
from app.models.chatbot import Chatbot
# from app.models.admin_chatbot import AdminChatbot
from app.models.chatbot import Chatbot

from app.models.user import User
from sqlalchemy.orm import Session as SQLASession
from sqlalchemy import func, cast, Float,distinct,case

from datetime import datetime, timedelta
from collections import defaultdict

from sqlalchemy import func

class AnalyticsRepository:
    # Sessions per User:
    # Average number of sessions per user over a specified period.
    @staticmethod 
    def get_session_message_counts(db_session: SQLASession) -> list:
        try:
            # Perform the query to join Session and SessionHistory, group by session name, and count messages
            results = (
                db_session.query(Session.id, func.count(SessionHistory.id).label('message_count'))
                .join(SessionHistory, Session.id == SessionHistory.session_id)
                .group_by(Session.id)
                .all()
            )
            
            # Format the results as a list of strings
            session_message_counts = [f"{id}: {message_count} messages" for id, message_count in results]
            
            return session_message_counts

        except Exception as e:
            logger.error(f"An error occurred while fetching session message counts: {e}")
            raise e
        
    # Message Volume:
    # Total number of messages sent and received by the chatbot.
    @staticmethod
    def get_message_volume(db_session: SQLASession) -> list:
        try:
            # query to join session_history and session on session_id, chatbot and session on chatbot_id. 
            # get count of each session_id in sessionHistory and add all sessions of each chatbot to count total messages of each chatbot
            
            results = (
                db_session.query(
                    Chatbot.id,
                    Chatbot.name,
                    func.count(SessionHistory.session_id).label('message_count')
                )
                .join(Session, Session.id == SessionHistory.session_id)
                .join(Chatbot, Chatbot.id == Session.chatbot_id)
                .group_by(Chatbot.id, Chatbot.name)
                # .order_by(func.count(SessionHistory.session_id).desc())
                .limit(12)
                .all()
            )

            # Format the results as a list of dictionaries
            message_volume = [{"id": id, "name": name, "total": message_count} for id, name, message_count in results]

            return message_volume
        except Exception as e:
            logger.error(f"An error occurred while fetching chatbot message counts: {e}")
            raise e
        
    # Sessions per User:
    # Average number of sessions per user
    @staticmethod
    def get_sessions_per_user(db_session: SQLASession) -> list:
        try:
            # Query to get the average count of sessions per user_id in the session table
            results = (
                db_session.query(
                    Session.user_id, 
                    func.count(Session.id).label('session_count')
                )
                .group_by(Session.user_id)
                .all()
            )

            # Calculate the average number of sessions per user
            total_sessions = sum(session_count for _, session_count in results)
            total_users = len(results)
            average_sessions_per_user = total_sessions / total_users if total_users > 0 else 0

        
            return average_sessions_per_user
        except Exception as e:
            logger.error(f"An error occurred while fetching sessions per user: {e}")
            raise e

    # Response Time:
    # Average time each chatbot takes to respond to a user's message.
    @staticmethod
    def get_avg_response_time(db_session: SQLASession) -> list:
        try:
            results = (
                db_session.query(
                    Chatbot.id,
                    Chatbot.name,
                    (func.sum(cast(SessionHistory.response_time, Float)) / func.count(SessionHistory.response_time)).label('avg_response_time'),
                    func.count(Session.id).label('total_sessions')
                )
                .join(Session, Session.id == SessionHistory.session_id)
                .join(Chatbot, Chatbot.id == Session.chatbot_id)
                .group_by(Chatbot.id, Chatbot.name)
                .limit(6)
                .all()
            )

            # Format the results as a list of dictionaries
            avg_response_time = [{"id": id, "name": name, "avg_response_time": avg_response_time, "total_sessions": total_sessions} for id, name, avg_response_time, total_sessions in results]

            return avg_response_time
        
        except Exception as e:
            logger.error(f"An error occurred while fetching average response time per chatbot: {e}")
            raise e
        
    
    # Message count per month
    @staticmethod
    def get_message_count_per_month(db_session: SQLASession) -> list:
        try:
            # query to get the count of messages per month
            results = (
                db_session.query(
                    func.to_char(SessionHistory.created_at, 'YYYY-MM').label('month'),
                    func.count('*').label('user_count')
                )
                .group_by('month')
                .order_by('month')
                .all()
            )
 
            # Convert query result to dictionary {month: user_count}
            monthly_message = {month: message_count for month, message_count in results}
 
            return monthly_message
        except Exception as e:
            logger.error(f"An error occurred while fetching message count per month: {e}")
            raise e
        
    #Server load each hour
    def get_message_count_per_hour(db_session: SQLASession) -> list:
        try:
            # query to get the count of messages per month
            hour_results = (
                db_session.query(
                    func.to_char(SessionHistory.created_at, 'HH').label('hour'),
                    func.count('*').label('user_count')
                )
                .group_by('hour')
                .order_by('hour')
                .all()
            )
            hour_day_results = (
                db_session.query(
                    func.to_char(SessionHistory.created_at, 'YYYY-MM-DD HH').label('hour'),
                    func.count('*').label('user_count')
                )
                .group_by('hour')
                .order_by('hour')
                .all()
            )
            hourly_message={}
            for hour, message_count in hour_results:
                day_count = 0
                for hour_day, day_message_count in hour_day_results:
                    if hour_day.endswith(hour):
                        day_count += 1
                hourly_message[hour] = message_count/day_count
            # Convert query result to dictionary {month: user_count}
            # hourly_message = {hour: message_count for hour, message_count in results}
 
            return hourly_message
        except Exception as e:
            logger.error(f"An error occurred while fetching message count per hour: {e}")
            raise e
    @staticmethod
    def get_average_messages_per_session(db_session: SQLASession) -> float:
        try:
            # Count the total number of messages
            total_messages = db_session.query(func.count(SessionHistory.id)).scalar()
            
            # Count the total number of sessions
            total_sessions = db_session.query(func.count(Session.id)).scalar()

            if total_sessions == 0:
                return 0.0
            
            print(total_messages, total_sessions)  
            # Calculate the average number of messages per session
            average_messages_per_session = total_messages / total_sessions

            return average_messages_per_session

        except Exception as e:
            logger.error(f"An error occurred while calculating the average messages per session: {e}")
            raise e
        
    @staticmethod
    def get_total_unique_user_count(db_session: SQLASession) -> int:
        try:
            unique_users = (
                db_session.query(User.id)
                .distinct()
                .count()
            )
            return unique_users

        except Exception as e:
            logger.error(f"An error occurred while fetching total unique user count: {e}")
            raise e    
        
    @staticmethod
    def calculate_user_retention(db_session: SQLASession) -> float:
        try:
            # Total number of users
            total_users = db_session.query(func.count(distinct(User.id))).scalar()

            # Number of users with more than one session
            retained_users = (
                db_session.query(Session.user_id)
                .group_by(Session.user_id)
                .having(func.count(Session.id) > 1)
                .count()
            )

            if total_users == 0:
                return 0.0
            print(f"Total users & Retained users",total_users, retained_users)

            # Calculate retention rate
            retention_rate = (retained_users / total_users) * 100

            return retention_rate

        except Exception as e:
            logger.error(f"An error occurred while calculating user retention: {e}")
            raise e    
        
    @staticmethod
    def get_user_creation_stats_per_month(db_session: SQLASession) -> dict:
        try:
            half_year_ago = datetime.now() - timedelta(days=365/2)

            # Query to count users created per month
            user_creation_stats = (
                db_session.query(
                    func.to_char(User.created_at, 'YYYY-MM').label('month'),
                    func.count('*').label('user_count')
                )
                .filter(User.created_at >= half_year_ago)
                .group_by('month')
                .order_by('month')
                .all()
            )

            # Generate a list of the last 12 months
            current_date = datetime.now()
            last_6_months = [(current_date - timedelta(days=30 * i)).strftime('%Y-%m') for i in range(6)]
            last_6_months.reverse()

            # Initialize a dictionary with all months set to 0 user count
            monthly_user_creation_dict = defaultdict(lambda: 0)
            for month, user_count in user_creation_stats:
                monthly_user_creation_dict[month] = user_count

            # Create the final list with all months
            monthly_user_creation = [{
                "date": month,
                "user_count": monthly_user_creation_dict[month]
            } for month in last_6_months]

            return monthly_user_creation


        except Exception as e:
            logger.error(f"An error occurred while fetching user creation stats per month: {e}")
            raise e
    
    @staticmethod
    def get_feedback_counts(db_session: SQLASession) -> dict:
        try:
            # Query to count feedback types: Positive, Negative, Neutral
            feedback_counts = (
                db_session.query(
                    func.sum(case((SessionHistory.feedback == True, 1), else_=0)).label('positive_count'),
                    func.sum(case((SessionHistory.feedback == False, 1), else_=0)).label('negative_count'),
                    func.sum(case((SessionHistory.feedback == None, 1), else_=0)).label('neutral_count')
                )
                .one()  # Assuming there is only one row of results
            )

            # feedback_dict = {
            #     "name": ""
            #     'positive_count': feedback_counts.positive_count,
            #     'negative_count': feedback_counts.negative_count,
            #     'neutral_count': feedback_counts.neutral_count
            # }
            feedback_dict = [
                {
                    "name": "Positive",
                    "value": feedback_counts.positive_count,
                }, 
                {
                    "name": "Negative",
                    "value": feedback_counts.negative_count,
                },
                {
                    "name": "Neutral",
                    "value": feedback_counts.neutral_count,
                },
            ]

            return feedback_dict

        except Exception as e:
            logger.error(f"An error occurred while fetching feedback counts: {e}")
            raise e
    

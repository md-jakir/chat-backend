from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.prompt_repository import PromptRepository

from utils.logger import logger  



def set_prompt(db_session: Session, prompt_text: str, chatbot_id: int):
    try:
        return PromptRepository.set_prompt(db_session, prompt_text, chatbot_id)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def get_prompt(db_session: Session, prompt_id: int):
    try:
        return PromptRepository.get_prompt(db_session, prompt_id)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def update_prompt(db_session: Session, prompt_id: int, prompt_text: str):
    try:
        return PromptRepository.update_prompt(db_session, prompt_id, prompt_text)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def delete_prompt(db_session: Session, prompt_id: int):
    try:
        return PromptRepository.delete_prompt(db_session, prompt_id)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

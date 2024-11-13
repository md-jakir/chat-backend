from sqlalchemy.orm import Session
from ..models.prompt import Prompt
from fastapi import HTTPException
from utils.logger import logger

class PromptRepository:
    

    def set_prompt(db_session: Session, prompt_text: str, chatbot_id: int):
      try:  
        new_prompt = Prompt(prompt_text=prompt_text, chatbot_id=chatbot_id)
        db_session.add(new_prompt)
        db_session.commit()
        return new_prompt
      except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
      except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    def get_prompt(db_session: Session, prompt_id: int):
        try:  
          return db_session.query(Prompt).filter_by(prompt_id=prompt_id).first()
        except HTTPException as e:
           logger.info(f'An HTTP error occurred: \n {str(e)}')
           raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    def update_prompt(db_session: Session, prompt_id: int, prompt_text: str):
        try:
            prompt = db_session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                prompt.prompt_text = prompt_text
                db_session.commit()
            return prompt
        except HTTPException as e:
           logger.info(f'An HTTP error occurred: \n {str(e)}')
           raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    def delete_prompt(db_session: Session, prompt_id: int):
        try:
            prompt = db_session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                db_session.delete(prompt)
                db_session.commit()
            return prompt
        except HTTPException as e:
           logger.info(f'An HTTP error occurred: \n {str(e)}')
           raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


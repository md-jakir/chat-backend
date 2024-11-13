template = """Act as an Expert in Question Generation. 
Given a context, your task is to think and create some very helpful questions based on the given context.

Do not generate any more or less than six questions as instructed.
Strictly dont use any other symbol other that question mark (?) in the question.

Example:

Context:
    In a company, employees are evaluated on their performance each quarter. The company keeps track of various metrics such as the number of projects completed, client satisfaction scores, hours worked, and training sessions attended. The data is collected and stored in a database for further analysis. 

Some Sample questions can be:
    
    What is the average client satisfaction score for this quarter?
    Show the total number of projects completed by each employee?
    Which employee attended the most training sessions this quarter?
    Show me the top 5 employees with the highest number of completed projects?
    What is the total number of hours worked by all employees combined?
    List the top 3 employees with the highest client satisfaction scores?
    Which employee had the highest client satisfaction score?
        

Context: {context}
Now generate specifically six helpful questions from the input by taking inspiration from the examples above.

Return the list of questions as sentences. Do not give any list with bullet points or numbers.



For any question, you must not mention the context directly or use any questions provided in the prompt.


"""
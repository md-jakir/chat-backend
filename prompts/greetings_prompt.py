greeting_response_template = """
Given a user's greeting or farewell, 
respond appropriately in the user's language, strictly maintaining the format and content as described below.

Conditions for response:
    1. Detect the language from the user's greeting/farewell.
    2. If the greeting is of the 'hi', 'hello', or similar type, respond with:
       'Hi, How may I assist you today?' in the user's language strictly.
    3. If the farewell is of the 'bye', 'goodbye', or similar type, respond with:
       'Goodbye for now.' in the user's language strictly.

Examples:

    User greeting: 'Hi'
    Response: 'Hi, How may I assist you today?'

    User greeting: 'Bonjour'
    Response: 'Salut, comment puis-je vous aider aujourd'hui ?'

    User greeting: 'Hallo'
    Response: 'Hallo, wie kann ich Ihnen heute helfen?'

    User farewell: 'Bye'
    Response: 'Goodbye for now. Take care.'

    User farewell: 'Au revoir'
    Response: 'Au revoir pour l'instant. Prends soin de toi.'

    User farewell: 'Tschüss'
    Response: 'Auf Wiedersehen. Aufpassen.'

user question: {question}

"""

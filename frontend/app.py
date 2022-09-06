from main import create_app
from dotenv import load_dotenv
import os
app = create_app()
load_dotenv()
app.app_context().push()

if __name__ == "__main__":
    app.run(debug=True,port=os.getenv("PORT"))



#!/usr/bin/env python
from kaknas.app import app

if __name__ == "__main__":
    # app = create_app()
    app.run(threaded=True, port=5000)
    #main(app)

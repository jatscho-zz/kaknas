from kaknas.app import app
from kaknas.controller import index
from kaknas.controller.state import state
from kaknas.controller.diff_check import diff_check
from kaknas.controller.health import health

app.add_url_rule('/', 'index', index)
app.add_url_rule('/state', 'state', state)
app.add_url_rule('/diff-check', 'diff_check', diff_check)
app.add_url_rule('/health', 'health', health)

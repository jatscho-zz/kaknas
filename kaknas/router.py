from kaknas.app import app
from kaknas.controller import index
from kaknas.controller.diff_status import diff_status
from kaknas.controller.health import health

app.add_url_rule('/', 'index', index)
app.add_url_rule('/diff-status', 'diff_status', diff_status)
app.add_url_rule('/health', 'health', health)

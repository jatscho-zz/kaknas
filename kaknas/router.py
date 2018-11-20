from kaknas.app import app
from kaknas.controller import index
from kaknas.controller.state import state
from kaknas.controller.display_diff import display_diff
from kaknas.controller.diff_status import diff_status
from kaknas.controller.health import health

app.add_url_rule('/', 'index', index)
app.add_url_rule('/state', 'state', state)
app.add_url_rule('/display-diff', 'display_diff', display_diff)
app.add_url_rule('/diff-status', 'diff_status', diff_status)
app.add_url_rule('/health', 'health', health)

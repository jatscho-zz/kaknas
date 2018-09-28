from kaknas import app
from kaknas.controller import index
from kaknas.controller.github import github
from kaknas.controller.health import health


app.add_url_rule('/', 'index', index)
app.add_url_rule('/github', 'github', github)
app.add_url_rule('/health', 'health', health)

from kaknas import app
from kaknas.controller import index
from kaknas.controller.github import github


app.add_url_rule('/', 'index', index)
app.add_url_rule('/github', 'github', github)

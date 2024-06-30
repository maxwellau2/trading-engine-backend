from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/sample", tags=None)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            var ws = new WebSocket(`ws://localhost:8000/ws/livedata/123/coin1`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(Date.now() + event.data)
                message.appendChild(content)
                messages.insertBefore(message, messages.childNodes[0])
            };
        </script>
    </body>
</html>
"""


@router.get("/")
async def get_sample():
    return HTMLResponse(html)

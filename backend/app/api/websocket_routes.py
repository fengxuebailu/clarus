"""
WebSocket Routes for Real-Time Debate Streaming
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

from ..seminars.debate_manager import DebateManager
from ..seminars.war_room import WarRoom
from ..schemas.go_analysis import MoveAnalysis

router = APIRouter(prefix="/api/ws", tags=["WebSocket"])


@router.websocket("/test")
async def websocket_test(websocket: WebSocket):
    """Minimal test endpoint"""
    await websocket.accept()
    await websocket.send_text("Test OK")
    await websocket.close()


@router.websocket("/analyze")
async def websocket_analyze_copy(websocket: WebSocket):
    """Copy of the working endpoint from routes.py"""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "status", "message": "Working!"})
    except:
        pass

# Global debate manager instance
debate_manager = DebateManager()
war_room = WarRoom()


@router.websocket("/debate")
async def websocket_debate_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time debate streaming

    Message Protocol:
    ----------------
    Client -> Server:
        {
            "action": "start",
            "data": {
                "board_state": "...",
                "move_a": "D4",
                "move_b": "Q16",
                "player_color": "B"
            }
        }

        {
            "action": "continue",
            "debate_id": "..."
        }

    Server -> Client:
        {"type": "system", "content": "...", "status": "..."}
        {"type": "scribe_thinking", "content": "..."}
        {"type": "scribe", "content": "...", "full_explanation": {...}}
        {"type": "student_thinking", "content": "..."}
        {"type": "student", "content": "...", "prediction": {...}}
        {"type": "state", "status": "paused|complete", "content": "..."}
        {"type": "error", "content": "..."}
    """

    # Accept WebSocket connection from any origin (for development)
    # In production, you should validate the origin header
    origin = websocket.headers.get("origin", "")
    print(f"[WebSocket] Connection attempt from origin: {origin}")

    await websocket.accept()

    current_debate_id = None

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            action = message.get("action")

            if action == "start":
                # Start a new debate
                analysis_data = message.get("data")

                if not analysis_data:
                    await websocket.send_json({
                        "type": "error",
                        "content": "Missing analysis data"
                    })
                    continue

                # Create MoveAnalysis from data
                analysis = MoveAnalysis(**analysis_data)

                await websocket.send_json({
                    "type": "system",
                    "content": "Starting analysis...",
                    "status": "starting"
                })

                # Step 1: Get ground truth from War Room
                vector_a, vector_b = await war_room.grandmaster.parallel_simulation(
                    board_state=analysis.board_state,
                    move_a=analysis.move_a,
                    move_b=analysis.move_b
                )

                delta_vector = war_room.delta_hunter.analyze_delta(vector_a, vector_b)

                await websocket.send_json({
                    "type": "system",
                    "content": f"KataGo Analysis Complete. Delta: Winrate={delta_vector.delta_winrate * 100:.2f}%, Lead={delta_vector.delta_lead:.2f} pts",
                    "status": "analysis_complete",
                    "delta": {
                        "winrate": delta_vector.delta_winrate,
                        "lead": delta_vector.delta_lead
                    }
                })

                # Step 2: Create debate session
                punisher_sequence = vector_b.move_sequence if vector_b.move_sequence else []

                debate_state = debate_manager.create_debate(
                    delta_vector=delta_vector,
                    move_a=analysis.move_a,
                    move_b=analysis.move_b,
                    player_color=analysis.player_color,
                    board_state=analysis.board_state,
                    punisher_sequence=punisher_sequence
                )

                current_debate_id = debate_state.debate_id

                await websocket.send_json({
                    "type": "debate_started",
                    "debate_id": current_debate_id,
                    "content": "Debate session created. Starting first iteration..."
                })

                # Step 3: Run first iteration
                async def send_message(msg: Dict):
                    await websocket.send_json(msg)

                should_continue = True
                while should_continue:
                    should_continue = await debate_manager.run_next_iteration(
                        debate_id=current_debate_id,
                        on_message=send_message
                    )

            elif action == "continue":
                # Continue an existing debate
                debate_id = message.get("debate_id") or current_debate_id

                if not debate_id:
                    await websocket.send_json({
                        "type": "error",
                        "content": "No debate ID provided"
                    })
                    continue

                # Resume the debate
                if not debate_manager.resume_debate(debate_id):
                    await websocket.send_json({
                        "type": "error",
                        "content": "Failed to resume debate. It may not exist or is not paused."
                    })
                    continue

                await websocket.send_json({
                    "type": "system",
                    "content": "Resuming debate...",
                    "status": "resuming"
                })

                # Continue iterations
                async def send_message(msg: Dict):
                    await websocket.send_json(msg)

                should_continue = True
                while should_continue:
                    should_continue = await debate_manager.run_next_iteration(
                        debate_id=debate_id,
                        on_message=send_message
                    )

            elif action == "cleanup":
                # Clean up debate session
                debate_id = message.get("debate_id") or current_debate_id

                if debate_id:
                    debate_manager.cleanup_debate(debate_id)
                    await websocket.send_json({
                        "type": "system",
                        "content": "Debate session cleaned up",
                        "status": "cleaned"
                    })

            else:
                await websocket.send_json({
                    "type": "error",
                    "content": f"Unknown action: {action}"
                })

    except WebSocketDisconnect:
        print(f"[WebSocket] Client disconnected")

        # Cleanup on disconnect
        if current_debate_id:
            debate_manager.cleanup_debate(current_debate_id)

    except Exception as e:
        print(f"[WebSocket] Error: {e}")

        await websocket.send_json({
            "type": "error",
            "content": str(e)
        })

        await websocket.close()
